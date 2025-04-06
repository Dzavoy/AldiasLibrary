import re
import pymem

class MemoryPointer:
    def __init__(self, process, module, address=0):
        self._process = process
        if isinstance(process, str):
            self._process = pymem.Pymem(process)
        
        self._module = module
        if isinstance(module, str):
            self._module = pymem.process.module_from_name(self._process.process_handle, module)
        
        self._address = address
    
    def relocate_pattern(self, regex_pattern):
        lookup_bytes = self._process.read_bytes(self._module.lpBaseOfDll, self._module.SizeOfImage)
        result = re.search(regex_pattern, lookup_bytes)
        if not result:
            raise Exception(f'Failed to find pattern {regex_pattern} in module "{self._module.module_name}".')
        return MemoryPointer(
            self._process, self._module, self._module.lpBaseOfDll + result.start()
        )

    def offset(self, amount):
        return MemoryPointer(
            self._process, self._module, self._address + amount
        )
    
    def pointer_walk(self, *offsets):
        if not offsets:
            return self
        
        new_address = self._address + offsets[0]

        for offset in offsets[1:]:
            new_address = self._process.read_ulonglong(new_address)
            new_address += offset
        
        return MemoryPointer(
            self._process, self._module, new_address
        )

    def dereference(self):
        new_address = self._process.read_ulonglong(self._address)
        return MemoryPointer(
            self._process, self._module, new_address
        )
    
    def read_int(self):
        return self._process.read_int(self._address)
    
    def read_string(self):
        return self._process.read_string(self._address)
    
    def read_float(self):
        return self._process.read_float(self._address)
    
    def read_bytes(self, size):
        return self._process.read_bytes(self._address, size)
    
    def hex(self):
        return hex(self._address)

    def __int__(self):
        return self.address