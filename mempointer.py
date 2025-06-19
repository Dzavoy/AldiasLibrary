from __future__ import annotations
from typing import Any
import re
import pymem
from pymem import Pymem

class MemoryPointer:
    def __init__(self, process: str | Pymem,
        module: str | Any, address: int = 0) -> None:
        self._process: Pymem
        if isinstance(process, str):
            self._process = pymem.Pymem(process)
        else:
            self._process = process

        self._module: Any
        if isinstance(module, str):
            self._module = pymem.process.module_from_name(
                self._process.process_handle, module
            )
        else:
            self._module = module

        self._address: int = address

    def relocate_pattern(self, regex_pattern: bytes) -> MemoryPointer:
        lookup_bytes: bytes = self._process.read_bytes(
            self._module.lpBaseOfDll, self._module.SizeOfImage
        )

        result: re.Match | None = re.search(regex_pattern, lookup_bytes)
        if not result:
            raise Exception(
                f'Failed to find pattern {regex_pattern.decode("utf-8")} in module'
                f'"{self._module.module_name}".'
            )

        return MemoryPointer(
            self._process, self._module,
            self._module.lpBaseOfDll + result.start()
        )

    def offset(self, amount: int) -> MemoryPointer:
        return MemoryPointer(
            self._process, self._module, self._address + amount
        )

    def pointer_walk(self, *offsets: int) -> MemoryPointer:
        if not offsets:
            return self

        new_address: int = self._address + offsets[0]

        for offset in offsets[1:]:
            new_address = self._process.read_ulonglong(new_address)
            new_address += offset

        return MemoryPointer(
            self._process, self._module, new_address
        )

    def dereference(self) -> MemoryPointer:
        new_address: int = self._process.read_ulonglong(self._address)
        return MemoryPointer(
            self._process, self._module, new_address
        )


 # ================== Read Functions ==================

    # Read an integer from memory.
    def read_int(self) -> int:
        return self._process.read_int(self._address)

    # Read a string from memory.
    def read_string(self) -> str:
        return self._process.read_string(self._address)

    # Read a float from memory.
    def read_float(self) -> float:
        return self._process.read_float(self._address)

    # Read raw bytes from memory.
    def read_bytes(self, size: int) -> bytes:
        return self._process.read_bytes(self._address, size)


# ================== Write Functions ==================

    # Write an integer to memory.
    def write_int(self, value: int) -> None:
        self._process.write_int(self._address, value)

    # Write a float to memory.
    def write_float(self, value: float) -> None:
        self._process.write_float(self._address, value)

    # Write a string to memory.
    def write_string(self, value: str) -> None:
        self._process.write_string(self._address, value)

    # Write raw bytes to memory.
    def write_bytes(self, value: bytes, length: int) -> None:
        self._process.write_bytes(self._address, value, length)


# ================== Utility ==================

    # Return the memory address in hexadecimal format.
    def hex(self) -> str:
        return hex(self._address)

    # Return the memory address as an integer.
    def __int__(self) -> int:
        return self._address