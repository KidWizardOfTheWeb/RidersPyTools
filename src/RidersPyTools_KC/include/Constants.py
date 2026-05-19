from enum import Enum
# ID

SPEED_DIVISOR = 216.0
def pSpeed(speed_num: float):
    return speed_num / SPEED_DIVISOR

BASE_ID: int = 8770000

VANILLA_PLAYER_PTR: int = 0x80609440

# NOTE: init player ptr for TE if detected using map file/map file passed in
TE_PLAYER_PTR: int = 0x8054b100 # change to match the current ptr at time of release. Read main.map using map parser and change in config.py.
# 2.4.6 fix 1 0x80532d80

ZG_PLAYER_PTR: int = 0x804970CC # Player 1, other players may not be sequential. Do more research for this.

class GameIDs:
    SONIC_RIDERS_ID = b'GXEE8P' # Vanilla Game ID
    SONIC_RIDERS_TE_ID = b'GXSRTE' # Tournament Edition ID
    SONIC_RIDERS_DX_ID = b'GXSRDX' # DX ID
    SONIC_RIDERS_ZG_ID = b'SRZE8P' # Zero Gravity ID
    SONIC_RIDERS_FT_ID = b'FUTURE' # Future ID (follow the naming convention guys, c'mon...)

# class GameVersion(Enum):
#     Vanilla = 1
#     TE = 2
#     DX = 3
#     ZG = 4
#     FT = 5
#     pass


# class Sizes(enum):
# Signed
type s8 = 1
type s16 = 2
type s32 = 4
type s64 = 8

# Unsigned
type u8 = 1
type u16 = 2
type u32 = 4
type u64 = 8

type Bool = 1

# Floats
type f32 = 4
type f64 = 8

# Volatiles (uncommon, some symbols may use this)
type vs8 = 1
type vs16 = 2
type vs32 = 4

type vu8 = 1
type vu16 = 2
type vu32 = 4

type vf32 = 4
type vf64 = 8

# TASK is a void(*)(), so length 4
type Task = 4

# Ptr is... well a pointer, so length 4.
type ptr = 4

# Flag template handler
# TODO: Add more cases
# Note: group these? Readability would be so bad...
def Flag(f_type):
    match f_type:
        case "Buttons":
            # Controller button data
            return u32
        case "Type":
            # Shortcut type
            return u8
        case "SpecialFlags":
            # Bitfield of gearSpecialFlags
            return u32
        case "MovementFlags":
            # Player movement flags during the race, i.e. boosting.
            return u32
        case "PlayerFlags" | "PlayerStatus":
            return u32
        case "AnimationFlags":
            return u32
        case "ObjectVisibility":
            return u32
        case "ParticleCtrl":
            # Particle things
            return u16
        case _:
            return ptr
    pass

# fillerData handler
def fillerData(size):
    return size