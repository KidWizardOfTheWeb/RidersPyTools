import enum
# ID

BASE_ID: int = 8770000
VANILLA_PLAYER_PTR: int = 0x80609440
# NOTE: init player ptr for TE if detected using map file
TE_PLAYER_PTR: int = 0x80609440 # change to match the current ptr. Maybe read main.map somehow?
ZG_PLAYER_PTR: int = 0x804970CC # Player 1, other players may not be sequential
SONIC_RIDERS_ID = "GXEE8P"
SONIC_RIDERS_TE_ID = "GXSRTE"
SONIC_RIDERS_DX_ID = "GXSRDX"
SONIC_RIDERS_ZG_ID = "SRZE8P"

class GameVersion(enum):
    Vanilla = 1
    TE = 2
    DX = 3
    ZG = 4
    pass
