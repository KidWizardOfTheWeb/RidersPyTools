from enum import Enum
# ID

BASE_ID: int = 8770000

VANILLA_PLAYER_PTR: int = 0x80609440

# NOTE: init player ptr for TE if detected using map file/map file passed in
TE_PLAYER_PTR: int = 0x80609440 # change to match the current ptr at time of release. Read main.map using map parser and change in config.py.

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
s8 = 1
s16 = 2
s32 = 4
s64 = 8

# Unsigned
u8 = 1
u16 = 2
u32 = 4
u64 = 8

Bool = 1

# Floats
f32 = 4
f64 = 8

# Volatiles (uncommon, some symbols may use this)
vs8 = 1
vs16 = 2
vs32 = 4

vu8 = 1
vu16 = 2
vu32 = 4

vf32 = 4
vf64 = 8

# TASK is a void(*)(), so length 4
Task = 4

# Ptr is... well a pointer, so length 4.
ptr = 4