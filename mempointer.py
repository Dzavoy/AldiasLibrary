from __future__ import annotations
from typing import Any, Optional
import re
import pymem
from pymem import Pymem

class MemoryPointerError(Exception):
    pass


class MemoryPointer:
    def __init__(self, process: str | Pymem, module: str | Any, address: int = 0) -> None:
        # Resolves process
        if isinstance(process, str):
            try:
                self._process: Pymem = pymem.Pymem(process)
            except Exception as e:
                raise MemoryPointerError(
                    f"Failed to open '{process}' process: {e}"
                ) from e
        else:
            self._process = process

        # Resolves module
        if isinstance(module, str):
            try:
                self._module: Any = pymem.process.module_from_name(
                    self._process.process_handle, module
                )
            except Exception as e:
                raise MemoryPointerError(
                    f"Failed to get '{module}' module: {e}"
                ) from e
        else:
            self._module = module

        self._address: int = address
        self._module_bytes_cache: Optional[bytes] = None # Relocate_pattern cache

    def relocate_pattern(self, regex_pattern: bytes) -> MemoryPointer:
        if self._module_bytes_cache is None:
            self._module_bytes_cache = self._process.read_bytes(
                self._module.lpBaseOfDll, self._module.SizeOfImage
            )

        result = re.search(regex_pattern, self._module_bytes_cache)
        if not result:
            lookup_bytes: bytes = self._process.read_bytes(
                self._module.lpBaseOfDll, self._module.SizeOfImage
            )
            result = re.search(regex_pattern, lookup_bytes) 
            if not result:
                raise MemoryPointerError(
                    f"Pattern {regex_pattern!r} not found in module '{self._module.module_name}'."
                )
            
        return MemoryPointer(self._process, self._module, self._module.lpBaseOfDll + result.start())


    # ================== Basic pointer ops ==================

    # Returns a new MemoryPointer with address plus amount
    def offset(self, amount: int) -> MemoryPointer:
        return MemoryPointer(
            self._process, self._module, self._address + amount
        )

    # Reads an unsigned long at the current address and returns MemoryPointer to that address
    def dereference(self) -> MemoryPointer:
        try:
            new_address: int = self._process.read_ulonglong(self._address)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to dereference address {hex(self._address)}: {e}"
            ) from e
        return MemoryPointer(self._process, self._module, new_address)

    # Do a "pointer walk"
    def pointer_walk(self, *offsets: int) -> MemoryPointer:
        if not offsets:
            return self

        addr: int = self._address + offsets[0]
        for off in offsets[1:]:
            try:
                addr = self._process.read_ulonglong(addr)
            except Exception as e:
                raise MemoryPointerError(
                    f"Failed to read pointer in {hex(addr)}: {e}"
                ) from  e
            addr += off

        return MemoryPointer(self._process, self._module, addr)


    # ================== Read helpers ==================

    # Read raw bytes from memory.
    def read_bytes(self, size: int) -> bytes:
        try:
            return self._process.read_bytes(self._address, size)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to read {size} bytes at {hex(self._address)}: {e}"
            ) from e

    def read_ulonglong(self) -> int:
        try:
            return self._process.read_ulonglong(self._address)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to read ulonglong at {hex(self._address)}: {e}"
            ) from e

    # Read an integer from memory.
    def read_int(self) -> int:
        try:
            return self._process.read_int(self._address)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to read int at {hex(self._address)}: {e}"
            ) from e
    
    # Read a float from memory.
    def read_float(self) -> float:
        try:
            return self._process.read_float(self._address)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to read float at {hex(self._address)}: {e}"
            ) from e

    # Read a string from memory.
    def read_string(self, max_length: int = 256) -> str:
        try:
            return self._process.read_string(self._address)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to read string at {hex(self._address)}: {e}"
            ) from e


    # ================== Write helpers ==================

    # Write raw bytes to memory.
    def write_bytes(self, value: bytes, length: Optional[int]) -> None:
        if length is None:
            length = len(value)
        try:
            self._process.write_bytes(self._address, value, length)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to write bytes at address {hex(self._address)}: {e}"
            ) from e

    # Write an integer to memory.
    def write_int(self, value: int) -> None:
        try:
            self._process.write_int(self._address, value)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to write int at address {hex(self._address)}: {e}"
            ) from e

    # Write a float to memory.
    def write_float(self, value: float) -> None:
        try:
            self._process.write_float(self._address, value)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to write float at address {hex(self._address)}: {e}"
            ) from e

    # Write a string to memory.
    def write_string(self, value: str) -> None:
        try:
            self._process.write_string(self._address, value)
        except Exception as e:
            raise MemoryPointerError(
                f"Failed to write string at address {hex(self._address)}: {e}"
            ) from e


# ================== Utility ==================

    # Return the memory address in hexadecimal format.
    def hex(self) -> str:
        return hex(self._address)

    # Return the memory address as an integer.
    def __int__(self) -> int:
        return self._address

class Utils:
    #@staticmethod
    #def bool_to_bytes(value: bool) -> bytes:
        #return b"\x01" if value else b"\x00"

    def __init__(self, value: Any) -> None:
        self.value: Any = value
        
    def bool_to_bytes(self, value: bool) -> bytes:
        match value:
            case True:
                return b"\x01"
            case False:
                return b"\x00"
        