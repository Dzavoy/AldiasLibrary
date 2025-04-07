from __future__ import annotations
from typing import Any
import re
import pymem
from pymem import Pymem

class MemoryPointer:
    def __init__(self, process: str | Pymem, module: str | Any, address: int = 0) -> None:
        self._process: Pymem
        if isinstance(process, str):
            self._process = pymem.Pymem(process)
        else: self._process = process
        
        self._module: Any
        if isinstance(module, str):
            self._module = pymem.process.module_from_name(self._process.process_handle, module)
        else:
            self._module = module

        self._address: int = address
    
    def relocate_pattern(self, regex_pattern: bytes) -> MemoryPointer:
        lookup_bytes: bytes = self._process.read_bytes(self._module.lpBaseOfDll, self._module.SizeOfImage)
        result: re.Match | None = re.search(regex_pattern, lookup_bytes)
        if not result:
            raise Exception(f'Failed to find pattern {regex_pattern} in module "{self._module.module_name}".')
        return MemoryPointer(
            self._process, self._module, self._module.lpBaseOfDll + result.start()
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
    
    def read_int(self) -> int:
        return self._process.read_int(self._address)
    
    def read_string(self) -> str:
        return self._process.read_string(self._address)
    
    def read_float(self) -> float:
        return self._process.read_float(self._address)
    
    def read_bytes(self, size: int) -> bytes:
        return self._process.read_bytes(self._address, size)
    
    def hex(self) -> str:
        return hex(self._address)

    def __int__(self) -> int:
        return self.address