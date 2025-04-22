from mempointer import MemoryPointer
import json
from enum import Enum

class PatternType(Enum):
    GAME_MANAGER_IMP = rb"\x48\x8B\x05....\x48\x8B\x58\x38\x48\x85\xDB\x74.\xF6"
    NET_SEASON_MANAGER = rb"\x48\x8B\x0D....\x48\x85\xC9\x74.\x48\x8B\x49\x18\xE8"
    KATANA_MAIN_APP = rb"\x48\x8B\x15....\x45\x32\xC0\x85\xC9"

class BaseCategory:
    _base: MemoryPointer
    _pattern_type: PatternType

    def __init__(self, root: MemoryPointer) -> None:
        base: MemoryPointer = root.relocate_pattern(self._pattern_type.value)
        offset: int = base.offset(3).read_int()
        self._base = base.offset(offset + 7).dereference()

class Stats:
    def __init__(self, base: MemoryPointer,
        hp_paths: list[list[int]], sp_paths: list[list[int]]) -> None:
        self._base = base
        self.hp_path = hp_paths[0]
        self.max_hp_path = hp_paths[1]
        self.min_hp_path = hp_paths[2]

        self.sp_path = sp_paths[0]
        self.max_sp_path = sp_paths[1]

    @property
    def current_health(self) -> int:
        return self._base.pointer_walk(*self.hp_path).read_int()
    
    @property
    def max_health(self) -> int:
        return self._base.pointer_walk(*self.max_hp_path).read_int()

    @property
    def min_health(self) -> int:
        return self._base.pointer_walk(*self.min_hp_path).read_int()
    
    @property
    def current_stamina(self) -> float:
        return self._base.pointer_walk(*self.sp_path).read_float()
    
    @property
    def max_stamina(self) -> float:
        return self._base.pointer_walk(*self.max_sp_path).read_float()

class Attributes:
    def __init__(self, base: MemoryPointer,
    attributes_paths: list[list[int]]) -> None:
        self._base = base
        self.sl_path = attributes_paths[0]
        self.vgr_path = attributes_paths[1]
        self.end_path = attributes_paths[2]
        self.vit_path = attributes_paths[3]
        self.atn_path = attributes_paths[4]
        self.str_path = attributes_paths[5]
        self.dex_path = attributes_paths[6]
        self.adp_path = attributes_paths[7]
        self.int_path = attributes_paths[8]
        self.fth_path = attributes_paths[9]

    @property
    def soul_level(self) -> int:
        return self._base.pointer_walk(*self.sl_path).read_int()

    @property
    def vigor(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.vgr_path).read_bytes(2),
            byteorder='little'
        )
    
    @property
    def attunement(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.end_path).read_bytes(2),
            byteorder='little'
        )
    
    @property
    def endurance(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.vit_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def vitality(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.atn_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def strenght(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.str_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def dexterity(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.dex_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def adaptability(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.adp_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def intelligence(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.int_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def faith(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.fth_path).read_bytes(2),
            byteorder='little'
        )

class Covenant:
    def __init__(self, base: MemoryPointer,
        points_path: list[int], rank_path: list[int]) -> None:
        self._base = base
        self.points_path = points_path
        self.rank_path = rank_path
    
    @property
    def points(self) -> int:
        return self._base.pointer_walk(*self.points_path).read_int()
    
    @property
    def rank(self) -> int:
        return self._base.pointer_walk(*self.rank_path).read_int()

class Covenants(BaseCategory):
    _pattern_type = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

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
        
        with open("covenants_ids.json", "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)
        
    @property
    def current_covenant(self) -> str:
        return self.id[str(
            int.from_bytes(
                self._base.pointer_walk(0xD0, 0x490, 0x1AD).read_bytes(1),
                byteorder='little'
            )
        )]

class OnlineSession(BaseCategory):
    _pattern_type = PatternType.NET_SEASON_MANAGER

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

    @property
    def alloted_time(self) -> float:
        return self._base.pointer_walk(0x20, 0x17C).read_float()

class AttackState(BaseCategory):
    _pattern_type = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)
    
    @property
    def guard_state_1(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0xC0, 0x78).read_bytes(1),
            byteorder="little"
        )
    
    @property
    def guard_state_2(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(0xD0, 0xC0, 0x7C).read_bytes(1),
            byteorder="little"
        )

class Rings:
    def __init__(self, base: MemoryPointer,
        slots_paths: list[list[int]]) -> None:
        self._base = base
        self._slot_1_path = slots_paths[0]
        self._slot_2_path = slots_paths[1]
        self._slot_3_path = slots_paths[2]
        self._slot_4_path = slots_paths[3]

        with open("rings_ids.json", "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)
    
    @property
    def slot_1(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_1_path).read_int()
        )]
    
    @property
    def slot_2(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_2_path).read_int()
        )]

    @property
    def slot_3(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_3_path).read_int()
        )]
    
    @property
    def slot_4(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_4_path).read_int()
        )]

class Weapons:
    def __init__(self, base: MemoryPointer,
        slots_paths: list[list[int]]) -> None:
        self._base = base
        self._slot_1_path = slots_paths[0]
        self._slot_2_path = slots_paths[1]
        self._slot_3_path = slots_paths[2]

        with open("weapons_ids.json", "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)

    @property
    def slot_1(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_1_path).read_int()
        )]
    
    @property
    def slot_2(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_2_path).read_int()
        )]
    
    @property
    def slot_3(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._slot_3_path).read_int()
        )]

class Armors:
    def __init__(self,base: MemoryPointer,
        slots_paths: list[list[int]]) -> None:
        self._base = base
        self._head_path = slots_paths[0]
        self._chest_path = slots_paths[1]
        self._hands_path = slots_paths[2]
        self._legs_path = slots_paths[3]

        with open("armors_ids.json", "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)

    @property
    def head(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._head_path).read_int()
        )]
    
    @property
    def chest(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._chest_path).read_int()
        )]

    @property
    def hands(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._hands_path).read_int()
        )]
    
    @property
    def legs(self) -> str:
        return self.id[str(
            self._base.pointer_walk(*self._legs_path).read_int()
        )]

class MyCharacter(BaseCategory):
    _pattern_type = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)
    
        self.stats = Stats(
            self._base,
            hp_paths = [
                [0xD0, 0x168],
                [0xD0, 0x170],
                [0xD0, 0x16C]
            ],
            sp_paths = [
                [0xD0, 0x1AC],
                [0xD0, 0x1B4]
            ]
        )

        self.attributes = Attributes(
            self._base,
            attributes_paths = [
                [0xD0, 0x490, 0xd0],
                [0xD0, 0x490, 0x8],
                [0xD0, 0x490, 0xE],
                [0xD0, 0x490, 0xA],
                [0xD0, 0x490, 0xC],
                [0xD0, 0x490, 0x10],
                [0xD0, 0x490, 0x12],
                [0xD0, 0x490, 0x18],
                [0xD0, 0x490, 0x14],
                [0xD0, 0x490, 0x16]
            ]
        )

        with open("team_type_ids.json", "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)
    
    @property
    def player_name(self) -> str:
        return(
            self._base.pointer_walk(0xA8, 0xC0, 0x24)
            .read_bytes(50)
            .decode("utf-16-le")
        )

    @property
    def team_type(self) -> str:
        return self.id[str(
            ord(self._base.pointer_walk(0xD0, 0xB0, 0x3D)
            .read_bytes(1))
        )]

    @property
    def player_steam_id(self) -> int:
        return int(
            self._base.pointer_walk(0xA8, 0xC8, 0x14)
            .read_string()[1:],
            16
        )

class Equipment(BaseCategory):
    _pattern_type = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

        self.rings = Rings(
            self._base,
            slots_paths = [
                [0xD0, 0x378, 0x4E8],
                [0xD0, 0x378, 0x4EC],
                [0xD0, 0x378, 0x4F0],
                [0xD0, 0x378, 0x4F4]
            ]
        )

        self.right_hand = Weapons(
            self._base,
            slots_paths = [
                [0xD0, 0x378, 0xB0],
                [0xD0, 0x378, 0xD8],
                [0xD0, 0x378, 0x100]
            ]
        )

        self.left_hand = Weapons(
            self._base,
            slots_paths = [
                [0xD0, 0x378, 0x9C],
                [0xD0, 0x378, 0xC4],
                [0xD0, 0x378, 0xEC]
            ]
        )

        self.armor = Armors(
            self._base,
            slots_paths = [
                [0xD0, 0x378, 0x114],
                [0xD0, 0x378, 0x128],
                [0xD0, 0x378, 0x13C],
                [0xD0, 0x378, 0x150]
            ]
        )

class DS2Memory:
    def __init__(self) -> None:
        root = MemoryPointer("DarkSoulsII.exe", "DarkSoulsII.exe")

        self.my_character = MyCharacter(root)
        self.covenants = Covenants(root)
        self.online = OnlineSession(root)
        self.attack_state = AttackState(root)
        self.equipment = Equipment(root)