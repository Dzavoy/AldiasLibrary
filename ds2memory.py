from mempointer import MemoryPointer
import json

class BaseCategory:
    _base: MemoryPointer

    def __init__(self, root: MemoryPointer, pattern: bytes) -> None:
        base: MemoryPointer = root.relocate_pattern(pattern)
        offset: int = base.offset(3).read_int()
        self._base = base.offset(offset + 7).dereference()

class Stats(BaseCategory):
    def __init__(self, root: MemoryPointer) -> None:
        pattern: bytes = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

    def player_health(self) -> int:
        return self._base.pointer_walk(0xD0, 0x168).read_int()
    
    def player_min_health(self) -> int:
        return self._base.pointer_walk(0xD0, 0x16C).read_int()

    def player_max_health(self) -> int:
        return self._base.pointer_walk(0xD0, 0x170).read_int()
    
    def player_stamina(self) -> float:
        return self._base.pointer_walk(0xD0, 0x1AC).read_float()
    
    def player_max_stamina(self) -> float:
        return self._base.pointer_walk(0xD0, 0x1B4).read_float()

    def player_name(self) -> str:
        return self._base.pointer_walk(0xA8, 0xC0, 0x24).read_bytes(50).decode("utf-16-le")

    def team_type(self) -> int:
        return ord(self._base.pointer_walk(0xD0, 0xB0, 0x3D).read_bytes(1))

    def player_steam_id(self) -> int:
        return int(self._base.pointer_walk(0xA8, 0xC8, 0x14).read_string()[1:], 16)

class Attributes(BaseCategory):
    def __init__(self, root: MemoryPointer) -> None:
        pattern: bytes = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

    def player_level(self) -> int:
        return self._base.pointer_walk(0xD0, 0x490, 0xd0).read_int()

    def player_vigor(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x8).read_bytes(2),
            byteorder='little'
        )
    
    def player_attunement(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0xE).read_bytes(2),
            byteorder='little'
        )

    def player_endurance(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0xA).read_bytes(2),
            byteorder='little'
        )

    def player_vitality(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0xC).read_bytes(2),
            byteorder='little'
        )

    def player_strenght(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x10).read_bytes(2),
            byteorder='little'
        )

    def player_dexterity(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x12).read_bytes(2),
            byteorder='little'
        )

    def player_adaptability(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x18).read_bytes(2),
            byteorder='little'
        )

    def player_intelligence(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x14).read_bytes(2),
            byteorder='little'
        )

    def player_faith(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x16).read_bytes(2),
            byteorder='little'
        )

class Covenant:
    def __init__(self, base: MemoryPointer, points_path: list[int], rank_path: list[int]) -> None:
        self._base = base
        self.points_path = points_path
        self.rank_path = rank_path
    
    def points(self) -> int:
        return self._base.pointer_walk(*self.points_path).read_int()
    
    def rank(self) -> int:
        return self._base.pointer_walk(*self.rank_path).read_int()

class Covenants(BaseCategory):
    def __init__(self, root: MemoryPointer) -> None:
        pattern: bytes = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

        self.heirs_of_the_sun = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1C4],
                rank_path=[0xD0, 0x490, 0x1B9]
            )

        self.way_of_blue = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1CA],
                rank_path=[0xD0, 0x490, 0x1BC]
            )

        self.rat_king = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1CC],
                rank_path=[0xD0, 0x490, 0x1BD]
            )

        self.bell_keeper = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1CE],
                rank_path=[0xD0, 0x490, 0x1BE]
            )

        self.dragon_remnants = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1D0],
                rank_path=[0xD0, 0x490, 0x1BF]
            )
        
        self.company_of_champions = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1D2],
                rank_path=[0xD0, 0x490, 0x1C0]
            )
        
        self.pilgrims_of_dark = Covenant(
                self._base,
                points_path=[0xD0, 0x490, 0x1D4],
                rank_path=[0xD0, 0x490, 0x1C1]
            )

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
        
    def current_covenant(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0x490, 0x1AD).read_bytes(1),
            byteorder='little'
        )

class OnlineSession(BaseCategory):
    def __init__(self, root: MemoryPointer) -> None:
        pattern: bytes = rb"\x48\x8B\x0D....\x48\x85\xC9\x74.\x48\x8B\x49\x18\xE8"
        super().__init__(root, pattern)

    def alloted_time(self) -> float:
        return self._base.pointer_walk(0x20, 0x17C).read_float()

class AttackState(BaseCategory):
    def __init__(self, root: MemoryPointer) -> None:
        pattern: bytes = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)
    
    def guard_state_1(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0xC0, 0x78).read_bytes(1),
            byteorder="little"
        )
    
    def guard_state_2(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0xC0, 0x7C).read_bytes(1),
            byteorder="little"
        )

class Rings:
    def __init__(self, base: MemoryPointer, slots_paths: list[list[int]]) -> None:

        self._base = base
        self.slot_1_path = slots_paths[0]
        self.slot_2_path = slots_paths[1]
        self.slot_3_path = slots_paths[2]
        self.slot_4_path = slots_paths[3]

        with open("rings_ids.json", "r", encoding='utf-8') as file:
            self.id = json.load(file)
    
    def slot_1(self) -> int:
        return self.id[str(self._base.pointer_walk(*self.slot_1_path).read_int())]
    
    def slot_2(self) -> int:
        return self.id[str(self._base.pointer_walk(*self.slot_2_path).read_int())]

    def slot_3(self) -> int:
        return self.id[str(self._base.pointer_walk(*self.slot_3_path).read_int())]
    
    def slot_4(self) -> int:
        return self.id[str(self._base.pointer_walk(*self.slot_4_path).read_int())]

class Equipment(BaseCategory):
    def __init__(self, root: MemoryPointer) -> None:
        pattern: bytes = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
        super().__init__(root, pattern)

        self.rings = Rings(
            self._base,
            slots_paths = [
                [0xD0, 0x378, 0x4E8],
                [0xD0, 0x378, 0x4EC],
                [0xD0, 0x378, 0x4F0],
                [0xD0, 0x378, 0x4F4]
            ]
        )

class DS2Memory:
    def __init__(self) -> None:
        root = MemoryPointer("DarkSoulsII.exe", "DarkSoulsII.exe")

        self.stats = Stats(root)
        self.attributes = Attributes(root)
        self.covenants = Covenants(root)
        self.online = OnlineSession(root)
        self.attak_state = AttackState(root)
        self.equipment = Equipment(root)