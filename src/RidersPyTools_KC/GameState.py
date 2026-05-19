import dataclasses

from .include.Constants import GameIDs
from enum import Enum
# from src.RidersPyTools_KC.Constants import GameVersion

# Starts as vanilla unless written otherwise
GAME_VERSION = GameIDs.SONIC_RIDERS_TE_ID

# Main game mode ID, see GameModes.
CURRENT_GAME_MODE = None

# Internal ID used by the game to determine certain states about certain modes
GAME_DETAIL = None

# AKA ExitMethod
END_OF_GAME_FLAG = None

class GameModes:
    TITLE_SCREEN = 0x1,
    STORY_MODE = 100,
    MISSION_MODE = 200,
    TAG_MODE = 300,
    EMERALD_CHASE = 400,
    BATTLE_MODE = 500,
    TIME_TRIAL = 600,
    FREE_RACE = 700,
    WORLD_GRAND_PRIX = 800,
    UNK_MODE = 900,  # Complete mystery to this day...
    CUTSCENE_MODE = 1000

class ExitMethod(Enum):
    Quit = 1,
    Retry = 2

class RaceState(Enum):
    Init = 0,
    OpeningCutscene = 1,
    Countdown = 2,
    Active = 3,
    End = 4

# TODO: Map this to data addresses properly so that modifying an instance of the rules will modify the game memory
@dataclasses.dataclass
class RuleSettings:
    unk31: bool
    unk30: bool
    unk29: bool
    unk28: bool
    unk27: bool
    announcer: bool
    unk25: bool
    unk24: bool
    unk23: bool
    unk22: bool
    cpu_racers: bool
    unk20: bool
    disable_retire: bool
    unk18: bool
    unk17: bool
    unk16: bool
    unk15: bool
    unk14: bool
    unk13: bool
    unk12: bool
    unk11: bool
    air_pits: bool
    items: bool
    japanese_voices: bool
    unk7: bool
    max_lap: int
    pass