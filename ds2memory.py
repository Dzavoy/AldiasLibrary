from mempointer import MemoryPointer, Utils
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

         # Magic formula
        self._base: MemoryPointer = base.offset(offset + 7).dereference()

class IdReader:
    def __init__(self, file_name: str) -> None:
        with open(file_name, "r", encoding='utf-8') as file:
            self.id: dict[str, str] = json.load(file)

    def get_id(self) -> dict[str, str]:
        return self.id


# ================================ Stats ================================

class Stats:
    def __init__(self, base: MemoryPointer,
        hp_paths: list[list[int]], sp_paths: list[list[int]],
        name_path: list[int], team_type_path: list[int],
        steam_id_path: list[int]) -> None:
        self._base: MemoryPointer = base
        self.hp_path: list[int] = hp_paths[0]
        self.min_hp_path: list[int] = hp_paths[1]
        self.max_hp_path: list[int] = hp_paths[2]

        self.sp_path: list[int] = sp_paths[0]
        self.max_sp_path: list[int] = sp_paths[1]

        self.name_path: list[int] = name_path
        self.team_type_path: list[int] = team_type_path
        self.steam_id_path: list[int] = steam_id_path

        self.id_map: dict[str, str] = IdReader(
            "team_type_ids.json"
        ).get_id()

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
        return self.id_map[str(
            ord(self._base.pointer_walk(*self.team_type_path)
            .read_bytes(1))
        )]

    @property
    def steam_id(self) -> int:
        return int(
            self._base.pointer_walk(*self.steam_id_path)
            .read_string()[1:], 16
        )


# ================================ Attributes ================================

class Attributes:
    def __init__(self, base: MemoryPointer,
    attributes_paths: list[list[int]], sl_path: list[int]) -> None:
        self._base: MemoryPointer = base
        self.sl_path: list[int] = sl_path
        self.vgr_path: list[int] = attributes_paths[0]
        self.end_path: list[int] = attributes_paths[1]
        self.vit_path: list[int] = attributes_paths[2]
        self.atn_path: list[int] = attributes_paths[3]
        self.str_path: list[int] = attributes_paths[4]
        self.dex_path: list[int] = attributes_paths[5]
        self.adp_path: list[int] = attributes_paths[8]
        self.int_path: list[int] = attributes_paths[6]
        self.fth_path: list[int] = attributes_paths[7]

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


# ================================ Covenant ================================

class Covenant:
    def __init__(self, base: MemoryPointer,
        points_path: list[int], rank_path: list[int]) -> None:
        self._base: MemoryPointer = base
        self.points_path: list[int] = points_path
        self.rank_path: list[int] = rank_path

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
        self._base: MemoryPointer = base
        self.current_covenant_path: list[int] = current_covenant_path
        self.points_path: list[list[int]] = points_path
        self.rank_path: list[list[int]] = rank_path

        self.heirs_of_the_sun: Covenant = Covenant(
            self._base,
            self.points_path[0],
            self.rank_path[0]
        )
        
        self.blue_sentinels: Covenant = Covenant(
            self._base,
            self.points_path[1],
            self.rank_path[1]
        )
        
        self.brotherhood_of_blood: Covenant = Covenant(
            self._base,
            self.points_path[2],
            self.rank_path[2]
        )

        self.way_of_blue: Covenant = Covenant(
            self._base,
            self.points_path[3],
            self.rank_path[3]
        )

        self.rat_king: Covenant = Covenant(
            self._base,
            self.points_path[4],
            self.rank_path[4]
        )

        self.bell_keeper: Covenant = Covenant(
            self._base,
            self.points_path[5],
            self.rank_path[5]
        )

        self.dragon_remnants: Covenant = Covenant(
            self._base,
            self.points_path[6],
            self.rank_path[6]
        )

        self.company_of_champions: Covenant = Covenant(
            self._base,
            self.points_path[7],
            self.rank_path[7]
        )

        self.pilgrims_of_dark: Covenant = Covenant(
            self._base,
            self.points_path[8],
            self.rank_path[8]
        )

        self.id_map: dict[str, str] = IdReader("covenants_ids.json").get_id()

    @property
    def current_covenant(self) -> str:
        return self.id_map[str(
            int.from_bytes(
                self._base.pointer_walk(
                *self.current_covenant_path)
                .read_bytes(1),
                byteorder='little'
            )
        )]


# ================================ AttackState & OnlineSession ================================

class OnlineSession(BaseCategory):
    _pattern_type: PatternType = PatternType.NET_SEASON_MANAGER

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

    @property
    def alloted_time(self) -> float:
        return self._base.pointer_walk(0x20, 0x17C).read_float()

    @alloted_time.setter
    def alloted_time(self, value: float) -> None:
        self._base.pointer_walk(0x20, 0x17C).write_float(value)

class AttackState(BaseCategory):
    _pattern_type: PatternType = PatternType.GAME_MANAGER_IMP

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

    @property
    def lock_roll_state(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0x8C)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_roll_state.setter
    def lock_roll_state(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0x8C)

        step_4.write_bytes(byte_val, 1)

    @property
    def lock_stance(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xC)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_stance.setter
    def lock_stance(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xC)

        step_4.write_bytes(byte_val, 1)

    @property
    def lock_guard(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xA8)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_guard.setter
    def lock_guard(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xA8)

        step_4.write_bytes(byte_val, 1)

    @property
    def lock_attack_1l(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0x98)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_attack_1l.setter
    def lock_attack_1l(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0x98)

        step_4.write_bytes(byte_val, 1)

    @property
    def lock_attack_1h(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0x9C)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_attack_1h.setter
    def lock_attack_1h(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0x9C)

        step_4.write_bytes(byte_val, 1)

    @property
    def lock_attack_2l(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xA0)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_attack_2l.setter
    def lock_attack_2l(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xA0)

        step_4.write_bytes(byte_val, 1)

    @property
    def lock_attack_2h(self) -> bool:
        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xA4)
        return bool(int.from_bytes(step_4.read_bytes(1)))

    @lock_attack_2h.setter
    def lock_attack_2h(self, value: bool) -> None:
        utils: Utils = Utils(value)
        byte_val: bytes = utils.bool_to_bytes(value)

        step_1: MemoryPointer = self._base.offset(0xD0).dereference()
        step_2: MemoryPointer = step_1.offset(0xB8).dereference()
        step_3: MemoryPointer = step_2.offset(0x4D0)
        step_4: MemoryPointer = step_3.offset(0xA4)

        step_4.write_bytes(byte_val, 1)

    @property
    def animation_state(self) -> int:
        return int.from_bytes(self._base.pointer_walk(0xD0, 0xB8, 0x8).read_bytes(1))


# ================================ Rings ================================

class Rings:
    def __init__(self, base: MemoryPointer,
        slots_paths: list[list[int]]) -> None:
        self._base: MemoryPointer = base
        self._slot_1_path: list[int] = slots_paths[0]
        self._slot_2_path: list[int] = slots_paths[1]
        self._slot_3_path: list[int] = slots_paths[2]
        self._slot_4_path: list[int] = slots_paths[3]

        self.id_map: dict[str, str] = IdReader("rings_ids.json").get_id()

    @property
    def slot_1(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._slot_1_path).read_int()
        )]

    @property
    def slot_2(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._slot_2_path).read_int()
        )]

    @property
    def slot_3(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._slot_3_path).read_int()
        )]

    @property
    def slot_4(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._slot_4_path).read_int()
        )]


# ======================== Weapons Phantom Buffs ========================

class WeaponBuffs(BaseCategory):
    _pattern_type: PatternType = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

        # +0x18 -> deref
        step1: MemoryPointer = self._base.offset(0x18).dereference()

        # +0x310 -> deref
        step2: MemoryPointer = step1.offset(0x310).dereference()

        # +0xD8 -> deref
        step3: MemoryPointer = step2.offset(0xD8).dereference()

        # +0x1C8 -> ONLY OFFSET (no deref)
        self._chr_phantom_param: MemoryPointer = step3.offset(0x1C8)

        # ParamStart = ChrPhantomParam + 0x60C (only offset)
        self._param_start: MemoryPointer = self._chr_phantom_param.offset(0x60C)

    def _addr(self, rel: int) -> MemoryPointer:
        return self._param_start.offset(rel)

    # magic = ParamStart + 0x254
    @property
    def magic(self) -> float:
        return self._addr(0x254).read_float()

    @magic.setter
    def magic(self, value: float) -> None:
        self._addr(0x254).write_float(value)
    
    # lightning = ParamStart + 0x274
    @property
    def lightning(self) -> float:
        return self._addr(0x274).read_float()

    @lightning.setter
    def lightning(self, value: float) -> None:
        self._addr(0x274).write_float(value)

    # fire = ParamStart + 0x294
    @property
    def fire(self) -> float:
        return self._addr(0x294).read_float()

    @fire.setter
    def fire(self, value: float) -> None:
        self._addr(0x294).write_float(value)    
    
    # dark = ParamStart + 0x2B4
    @property
    def dark(self) -> float:
        return self._addr(0x2B4).read_float()

    @dark.setter
    def dark(self, value: float) -> None:
        self._addr(0x2B4).write_float(value)  

    # poison = ParamStart + 0x2D4
    @property
    def poison(self) -> float:
        return self._addr(0x2D4).read_float()

    @poison.setter
    def poison(self, value: float) -> None:
        self._addr(0x2D4).write_float(value)  

    # bleed = ParamStart + 0x2F4
    @property
    def bleed(self) -> float:
        return self._addr(0x2F4).read_float()

    @bleed.setter
    def bleed(self, value: float) -> None:
        self._addr(0x2F4).write_float(value) 

    # great_magic = ParamStart + 0x3B4
    @property
    def great_magic(self) -> float:
        return self._addr(0x3B4).read_float()

    @great_magic.setter
    def great_magic(self, value: float) -> None:
        self._addr(0x3B4).write_float(value) 


# ================================ Weapons ================================

class WeaponSlot:
    def __init__(self, base: MemoryPointer, id_path: list[int],
    db_path: list[int], infusion_path: list[int]) -> None:
        self._base: MemoryPointer = base
        self.id_path: list[int] = id_path
        self.db_path: list[int] = db_path
        self.infusion_path: list[int] = infusion_path

        self.id_map: dict[str, str] = IdReader("weapons_ids.json").get_id()
        
        self.infusion_id_map: dict[str, str] = IdReader(
            "infusions_ids.json"
        ).get_id()

    @property
    def id(self) -> int:
        return self._base.pointer_walk(*self.id_path).read_int()

    @property
    def name(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self.id_path).read_int()
        )]

    @property
    def durability(self) -> float:
        return self._base.pointer_walk(*self.db_path).read_float()
    
    @property
    def infusion(self) -> str:
        return self.infusion_id_map[str(
            self._base.pointer_walk(*self.infusion_path).read_int()
        )]

class Weapons:
    def __init__(self, base: MemoryPointer,
        ids_paths: list[list[int]], db_paths: list[list[int]],
        infusion_paths: list[list[int]]) -> None:
        self._base: MemoryPointer = base
        self._slot_1_id_path: list[int] = ids_paths[0]
        self._slot_2_id_path: list[int] = ids_paths[1]
        self._slot_3_id_path: list[int] = ids_paths[2]

        self._slot_1_db_path: list[int] = db_paths[0]
        self._slot_2_db_path: list[int] = db_paths[1]
        self._slot_3_db_path: list[int] = db_paths[2]

        self._slot_1_infusion_path: list[int] = infusion_paths[0]
        self._slot_2_infusion_path: list[int] = infusion_paths[1]
        self._slot_3_infusion_path: list[int] = infusion_paths[2]

        self.slot_1: WeaponSlot = WeaponSlot(
            self._base,
            self._slot_1_id_path,
            self._slot_1_db_path,
            self._slot_1_infusion_path
        )

        self.slot_2: WeaponSlot = WeaponSlot(
            self._base,
            self._slot_2_id_path,
            self._slot_2_db_path,
            self._slot_2_infusion_path
        )

        self.slot_3: WeaponSlot = WeaponSlot(
            self._base,
            self._slot_3_id_path,
            self._slot_3_db_path,
            self._slot_3_infusion_path
        )


# ================================ Armors ================================

class Armors:
    def __init__(self,base: MemoryPointer,
        slots_paths: list[list[int]]) -> None:
        self._base: MemoryPointer = base
        self._head_path: list[int] = slots_paths[0]
        self._chest_path: list[int] = slots_paths[1]
        self._hands_path: list[int] = slots_paths[2]
        self._legs_path: list[int] = slots_paths[3]

        self.id_map: dict[str, str] = IdReader("armors_ids.json").get_id()

    @property
    def head(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._head_path).read_int()
        )]

    @property
    def chest(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._chest_path).read_int()
        )]

    @property
    def hands(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._hands_path).read_int()
        )]

    @property
    def legs(self) -> str:
        return self.id_map[str(
            self._base.pointer_walk(*self._legs_path).read_int()
        )]


# ================================ Equipment ================================

class Equipment:
    def __init__(self, base: MemoryPointer, rings_paths: list[list[int]],
        r_hand_paths: list[list[int]], l_hand_paths: list[list[int]],
        r_hand_db_paths: list[list[int]], l_hand_db_paths: list[list[int]],
        r_hand_infusion_paths: list[list[int]], l_hand_infusion_paths: list[list[int]],
        armor_paths: list[list[int]]) -> None:
        self._base: MemoryPointer = base
        self.rings_paths: list[list[int]] = rings_paths
        self.r_hand_paths: list[list[int]] = r_hand_paths
        self.l_hand_paths: list[list[int]] = l_hand_paths
        self.r_hand_db_paths: list[list[int]] = r_hand_db_paths
        self.l_hand_db_paths: list[list[int]] = l_hand_db_paths
        self.r_hand_infusion_paths: list[list[int]] = r_hand_infusion_paths
        self.l_hand_infusion_paths: list[list[int]] = l_hand_infusion_paths

        self.armor_paths: list[list[int]] = armor_paths

        self.rings: Rings = Rings(
            self._base,
            self.rings_paths
        )

        self.right_hand: Weapons = Weapons(
            self._base,
            self.r_hand_paths,
            self.r_hand_db_paths,
            self.r_hand_infusion_paths
        )

        self.left_hand: Weapons = Weapons(
            self._base,
            self.l_hand_paths,
            self.l_hand_db_paths,
            self.l_hand_infusion_paths
        )

        self.armor: Armors = Armors(
            self._base,
            self.armor_paths
        )


# ================================ MyCharacter ================================

class MyCharacter(BaseCategory):
    _pattern_type: PatternType = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

        self.stats: Stats = Stats(
            self._base,
            name_path = [0xA8, 0xC0, 0x24],
            team_type_path = [0xD0, 0xB0, 0x3D],
            steam_id_path = [0xA8, 0xC8, 0x14],
            hp_paths = [[0xD0, 0x168 + i*4] for i in range(3)],
            sp_paths = [[0xD0, 0x1AC + i*8] for i in range(2)]
        )

        self.attributes: Attributes = Attributes(
            self._base,
            sl_path = [0xD0, 0x490, 0xd0],
            attributes_paths = [[0xD0, 0x490, 0x8 + i*2] for i in range(9)]
        )

        self.covenants: Covenants = Covenants(
            self._base,
            points_path = [[0xD0, 0x490, 0x1C4 + i*2] for i in range(9)],
            rank_path = [[0xD0, 0x490, 0x1B9 + i] for i in range(9)],
            current_covenant_path = [0xD0, 0x490, 0x1AD]
        )

        self.equipment: Equipment = Equipment(
            self._base,
            rings_paths = [[0xD0, 0x378, 0x4E8 + i*4] for i in range(4)],
            r_hand_paths = [[0xD0, 0x378, 0xB0 + i*40] for i in range(3)],
            l_hand_paths = [[0xD0, 0x378, 0x9C + i*40] for i in range(3)],
            r_hand_db_paths = [[0xD0, 0x378, 0x28, 0x16C + i*72] for i in range(3)],
            l_hand_db_paths = [[0xD0, 0x378, 0x28, 0x94 + i*72] for i in range(3)],
            r_hand_infusion_paths = [[0xD0, 0x378, 0x28, 0x149 + i*72] for i in range(3)],
            l_hand_infusion_paths = [[0xD0, 0x378, 0x28, 0x71 + i*72] for i in range(3)],
            armor_paths = [[0xD0, 0x378, 0x114 + i*20] for i in range(4)]
        )


# ================================ Player 1 ================================

class Player1(BaseCategory):
    _pattern_type: PatternType = PatternType.NET_SEASON_MANAGER

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)

        self.stats: Stats = Stats(
            self._base,
            name_path = [0x20, 0x234],
            team_type_path = [0x20, 0x1E8, 0xB0, 0x4D],
            steam_id_path = [], # Need to find this path.
            hp_paths = [[0x20, 0x1E8, 0x168 + i*4] for i in range(3)],
            sp_paths = [[0x20, 0x1E8, 0x1AC + i*8] for i in range(2)]
        )

        self.attributes: Attributes = Attributes(
            self._base,
            sl_path = [0x20, 0x1E8, 0x490, 0xD0],
            attributes_paths = [[0x20, 0x1E8, 0x490, 0x8 + i*2] for i in range(9)]
        )

        self.covenants: Covenants = Covenants(
            self._base,

            # There is a high probability that this is incorrect, but I’m not certain.
            points_path = [[0x20, 0x1E8, 0x1C4 + i*2] for i in range(9)],

            # There is a high probability that this is incorrect, but I’m not certain.
            rank_path = [[0x20, 0x1E8, 0x490, 0x1B9 + i] for i in range(9)],
            
            current_covenant_path = [0x20, 0x1E8, 0x490, 0x1AD]
        )

        self.equipment: Equipment = Equipment(
            self._base,
            rings_paths = [[0x20, 0x1E8, 0x9AC + i*20] for i in range(4)],
            r_hand_paths = [[0x20, 0x1E8, 0x880 + i*40] for i in range(3)],
            l_hand_paths = [[0x20, 0x1E8, 0x86C + i*40] for i in range(3)],

            # This path is incorrect, I need to find it.
            r_hand_db_paths = [[0x20, 0x1E8, 0x28, 0x16C + i*72] for i in range(3)],

            # This path is incorrect, I need to find it.
            l_hand_db_paths = [[0x20, 0x1E8, 0x28, 0x94 + i*72] for i in range(3)],

            # This path is incorrect, I need to find it.
            r_hand_infusion_paths = [[0xD0, 0x378, 0x28, 0x149 + i*72] for i in range(3)],

            # This path is incorrect, I need to find it.
            l_hand_infusion_paths = [[0xD0, 0x378, 0x28, 0x71 + i*72] for i in range(3)],

            armor_paths = [[0x20, 0x1E8, 0x8E4 + i*20] for i in range(4)]
        )


# ================================ Player 2 ================================

class Player2(BaseCategory):
    _pattern_type: PatternType = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)


# ================================ Player 3 ================================

class Player3(BaseCategory):
    _pattern_type: PatternType = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)


# ================================ Player 4 ================================

class Player4(BaseCategory):
    _pattern_type: PatternType = PatternType.GAME_MANAGER_IMP

    def __init__(self, root: MemoryPointer) -> None:
        super().__init__(root)


# ================================ DS2Memory ================================

class DS2Memory:
    def __init__(self) -> None:
        root: MemoryPointer = MemoryPointer(
            "DarkSoulsII.exe",
            "DarkSoulsII.exe"
        )
        self.my_character: MyCharacter = MyCharacter(root)
        self.player_1: Player1 = Player1(root)
        self.player_2: Player2 = Player2(root)
        self.player_3: Player3 = Player3(root)
        self.player_4: Player4 = Player4(root)
        self.online: OnlineSession = OnlineSession(root)
        self.attack_state: AttackState = AttackState(root)
        self.weapon_buffs: WeaponBuffs = WeaponBuffs(root)