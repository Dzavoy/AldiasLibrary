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

class IdReader:
    def __init__(self, file_name: str) -> None:
        with open(file_name, "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)
    
    def get_id(self) -> dict[str, str]:
        return self.id

class Stats:
    def __init__(self, base: MemoryPointer,
        hp_paths: list[list[int]], sp_paths: list[list[int]],
        name_path: list[int], team_type_path: list[int],
        steam_id_path: list[int]) -> None:
        self._base = base
        self.hp_path = hp_paths[0]
        self.min_hp_path = hp_paths[1]
        self.max_hp_path = hp_paths[2]

        self.sp_path = sp_paths[0]
        self.max_sp_path = sp_paths[1]

        self.name_path = name_path
        self.team_type_path = team_type_path
        self.steam_id_path = steam_id_path
        
        self.id = IdReader("team_type_ids.json").get_id()

    @property
    def current_health(self) -> int:
        return self._base.pointer_walk(*self.hp_path).read_int()

    @current_health.setter
    def current_health(self, value: int) -> None:
        self._base.pointer_walk(*self.hp_path).write_int(value)

    @property
    def max_health(self) -> int:
        return self._base.pointer_walk(*self.max_hp_path).read_int()

    @max_health.setter
    def max_health(self, value: int) -> None:
        self._base.pointer_walk(*self.max_hp_path).write_int(value)

    @property
    def min_health(self) -> int:
        return self._base.pointer_walk(*self.min_hp_path).read_int()

    @min_health.setter
    def min_health(self, value: int) -> None:
        self._base.pointer_walk(*self.min_hp_path).write_int(value)

    @property
    def current_stamina(self) -> float:
        return self._base.pointer_walk(*self.sp_path).read_float()

    @current_stamina.setter
    def current_stamina(self, value: float) -> None:
        self._base.pointer_walk(*self.sp_path).write_float(value)

    @property
    def max_stamina(self) -> float:
        return self._base.pointer_walk(*self.max_sp_path).read_float()

    @max_stamina.setter
    def max_stamina(self, value: float) -> None:
        self._base.pointer_walk(*self.max_sp_path).write_float(value)

    @property
    def name(self) -> str:
        return(
            self._base.pointer_walk(*self.name_path)
            .read_bytes(50)
            .decode("utf-16-le")
        )

    @name.setter
    def name(self, value: str) -> None:
        (self._base.pointer_walk(*self.name_path)
        .write_bytes(value.encode("utf-16-le"), length=50))

    @property
    def team_type(self) -> str:
        return self.id[str(
            ord(self._base.pointer_walk(*self.team_type_path)
            .read_bytes(1))
        )]

    @property
    def steam_id(self) -> int:
        return int(
            self._base.pointer_walk(*self.steam_id_path)
            .read_string()[1:],
            16
        )

class Attributes:
    def __init__(self, base: MemoryPointer,
    attributes_paths: list[list[int]], sl_path: list[int]) -> None:
        self._base = base
        self.sl_path = sl_path
        self.vgr_path = attributes_paths[0]
        self.end_path = attributes_paths[1]
        self.vit_path = attributes_paths[2]
        self.atn_path = attributes_paths[3]
        self.str_path = attributes_paths[4]
        self.dex_path = attributes_paths[5]
        self.adp_path = attributes_paths[8]
        self.int_path = attributes_paths[6]
        self.fth_path = attributes_paths[7]

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
    def endurance(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.end_path).read_bytes(2),
            byteorder='little'
        )
    
    @property
    def vitality(self) -> int:
        return int.from_bytes(
            self._base.pointer_walk(*self.vit_path).read_bytes(2),
            byteorder='little'
        )

    @property
    def attunement(self) -> int:
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

    @points.setter
    def points(self, value: int) -> None:
        self._base.pointer_walk(*self.points_path).write_int(value)

    @property
    def rank(self) -> int:
        return self._base.pointer_walk(*self.rank_path).read_int()

    @rank.setter
    def rank(self, value: int) -> None:
        self._base.pointer_walk(*self.rank_path).write_int(value)

class Covenants:
    def __init__(self, base: MemoryPointer, current_covenant_path: list[int],
        points_path: list[list[int]], rank_path: list[list[int]]) -> None:
        self._base = base
        self.current_covenant_path = current_covenant_path
        self.points_path = points_path
        self.rank_path = rank_path

        self.heirs_of_the_sun = Covenant(
                self._base,
                self.points_path[0],
                self.rank_path[0]
            )
        
        self.blue_sentinels = Covenant(
                self._base,
                self.points_path[1],
                self.rank_path[1]
            )
        
        self.brotherhood_of_blood = Covenant(
                self._base,
                self.points_path[2],
                self.rank_path[2]
            )

        self.way_of_blue = Covenant(
                self._base,
                self.points_path[3],
                self.rank_path[3]
            )

        self.rat_king = Covenant(
                self._base,
                self.points_path[4],
                self.rank_path[4]
            )

        self.bell_keeper = Covenant(
                self._base,
                self.points_path[5],
                self.rank_path[5]
            )

        self.dragon_remnants = Covenant(
                self._base,
                self.points_path[6],
                self.rank_path[6]
            )

        self.company_of_champions = Covenant(
                self._base,
                self.points_path[7],
                self.rank_path[7]
            )

        self.pilgrims_of_dark = Covenant(
                self._base,
                self.points_path[8],
                self.rank_path[8]
            )

        self.id = IdReader("covenants_ids.json").get_id()

    @property
    def current_covenant(self) -> str:
        return self.id[str(
            int.from_bytes(
                self._base.pointer_walk(
                *self.current_covenant_path)
                .read_bytes(1),
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

    @alloted_time.setter
    def alloted_time(self, value: float) -> None:
        self._base.pointer_walk(0x20, 0x17C).write_float(value)

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

        self.id = IdReader("rings_ids.json").get_id()

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

        self.id = IdReader("weapons_ids.json").get_id()

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

        self.id = IdReader("armors_ids.json").get_id()

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

class Equipment:
    def __init__(self, base: MemoryPointer, rings_paths: list[list[int]],
        r_hand_paths: list[list[int]], l_hand_paths: list[list[int]],
        armor_paths: list[list[int]]) -> None:
        self._base = base
        self.rings_paths = rings_paths
        self.r_hand_paths = r_hand_paths
        self.l_hand_paths = l_hand_paths
        self.armor_paths = armor_paths

        self.rings = Rings(
            self._base,
            self.rings_paths
        )

        self.right_hand = Weapons(
            self._base,
            self.r_hand_paths
        )

        self.left_hand = Weapons(
            self._base,
            self.l_hand_paths
        )

        self.armor = Armors(
            self._base,
            self.armor_paths
        )

class MyCharacter(BaseCategory):
    _pattern_type = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

        self.stats = Stats(
            self._base,
            name_path = [0xA8, 0xC0, 0x24],
            team_type_path = [0xD0, 0xB0, 0x3D],
            steam_id_path = [0xA8, 0xC8, 0x14],
            hp_paths = [[0xD0, 0x168 + i*4] for i in range(3)],
            sp_paths = [[0xD0, 0x1AC + i*8] for i in range(2)]
        )

        self.attributes = Attributes(
            self._base,
            sl_path = [0xD0, 0x490, 0xd0],
            attributes_paths = [[0xD0, 0x490, 0x8 + i*2] for i in range(9)]
        )

        self.covenants = Covenants(
            self._base,
            points_path = [[0xD0, 0x490, 0x1C4 + i*2] for i in range(9)],
            rank_path = [[0xD0, 0x490, 0x1B9 + i] for i in range(9)],
            current_covenant_path = [0xD0, 0x490, 0x1AD]
        )

        self.equipment = Equipment(
            self._base,
            rings_paths = [[0xD0, 0x378, 0x4E8 + i*4]for i in range(4)],
            r_hand_paths = [[0xD0, 0x378, 0xB0 + i*40]for i in range(3)],
            l_hand_paths = [[0xD0, 0x378, 0x9C + i*40]for i in range(3)],
            armor_paths = [[0xD0, 0x378, 0x114 + i*20] for i in range(4)]
        )

class DS2Memory:
    def __init__(self) -> None:
        root = MemoryPointer("DarkSoulsII.exe", "DarkSoulsII.exe")

        self.my_character = MyCharacter(root)
        self.online = OnlineSession(root)
        self.attack_state = AttackState(root)