from mempointer import MemoryPointer

class BaseCategory:
    def __init__(self, root, pattern):
        base = root.relocate_pattern(pattern)
        offset = base.offset(3).read_int()
        self._base = base.offset(offset + 7).dereference()

class Stats(BaseCategory):
    def __init__(self, root):
        pattern = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

    def player_health(self):
        return self._base.pointer_walk(0xD0, 0x168).read_int()

    def player_max_health(self):
        return self._base.pointer_walk(0xD0, 0x170).read_int()

    def player_name(self):
        return self._base.pointer_walk(0xA8, 0xC0, 0x24).read_bytes(50).decode("utf-16-le")

    def player_steam_id(self):
        return int(self._base.pointer_walk(0xA8, 0xC8, 0x14).read_string()[1:], 16)

class Atributes(BaseCategory):
    def __init__(self, root):
        pattern = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

    def player_level(self):
        return self._base.pointer_walk(0xD0, 0x490, 0xd0).read_int()

    def palyer_vigor(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x8).read_bytes(2),
            byteorder='little'
        )
    
    def palyer_attunement(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0xE).read_bytes(2),
            byteorder='little'
        )

    def palyer_endurance(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0xA).read_bytes(2),
            byteorder='little'
        )

    def palyer_vitality(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0xC).read_bytes(2),
            byteorder='little'
        )

    def palyer_strenght(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x10).read_bytes(2),
            byteorder='little'
        )

    def palyer_dexterity(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x12).read_bytes(2),
            byteorder='little'
        )

    def palyer_adaptability(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x18).read_bytes(2),
            byteorder='little'
        )

    def palyer_intelligence(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x14).read_bytes(2),
            byteorder='little'
        )

    def palyer_faith(self, root):
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x16).read_bytes(2),
            byteorder='little'
        )

class Covenant:
    def __init__(self, base, points_path, rank_path):
        self._base = base
        self.points_path = points_path
        self.rank_path = rank_path
    
    def points(self):
        return self._base.pointer_walk(*self.points_path).read_int()
    
    def rank(self):
        return self._base.pointer_walk(*self.rank_path).read_int()

class Covenants(BaseCategory):
    def __init__(self, root):
        pattern = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

    self.brotherhood_of_blood = Covenant(
            self._base,
            points_path=[0xD0, 0x490, 0x1C8],
            rank_path=[0xD0, 0x490, 0x1BB]
        )
    
    self.blue_sentinels = Covenant(
            self._base,
            points_path=[0xD0, 0x490, 0x1C6],
            rank_path=[0xD0, 0x490, 0x1BA]
        )
    
class DS2Memory:
    def __init__(self):
        root = MemoryPointer("DarkSoulsII.exe", "DarkSoulsII.exe")

        self.stats = Stats(root)
        self.atributes = Atributes(root)
        self.covenants = Covenants(root)

if __name__ == "__main__":
    ds2 = DS2Memory()

    print(ds2.stats.player_max_health())