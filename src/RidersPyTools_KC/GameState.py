import dataclasses

from .include.Constants import GameIDs
from enum import Enum, IntEnum
# from src.RidersPyTools_KC.Constants import GameVersion

# Starts as vanilla unless written otherwise
GAME_VERSION = GameIDs.SONIC_RIDERS_TE_ID

# Main game mode ID, see GameModes.
CURRENT_GAME_MODE = None

# Internal ID used by the game to determine certain states about certain modes
GAME_DETAIL = None

# AKA ExitMethod
END_OF_GAME_FLAG = None

class GameModes(IntEnum):
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
    SAVE_MODE = 2000 # Something about time trial save screen

MODE_ID_TO_NAME = {
    GameModes.TITLE_SCREEN: "Title Screen",
    GameModes.STORY_MODE: "Story Mode",
    GameModes.MISSION_MODE: "Mission Mode",
    GameModes.TAG_MODE: "Tag Mode",
    GameModes.EMERALD_CHASE: "Emerald Chase",
    GameModes.BATTLE_MODE: "Battle Mode",
    GameModes.TIME_TRIAL: "Time Trial",
    GameModes.FREE_RACE: "Free Race",
    GameModes.WORLD_GRAND_PRIX: "World Grand Prix",
    GameModes.UNK_MODE: "Unknown Mode",
    GameModes.CUTSCENE_MODE: "In a Cutscene",
    GameModes.SAVE_MODE: "Saving game"
}
ALL_MODES = list(MODE_ID_TO_NAME.keys())

class ExitMethod(IntEnum):
    Quit = 1,
    Retry = 2

class RaceState(IntEnum):
    Init = 0,
    OpeningCutscene = 1,
    Countdown = 2,
    Active = 3,
    End = 4

RACESTATE_ID_TO_NAME = {
    RaceState.Init: "Initializing race",
    RaceState.OpeningCutscene: "Starting race",
    RaceState.Countdown: "Race Countdown",
    RaceState.Active: "In an active race",
    RaceState.End: "Race finished"
}
ALL_RACESTATES = list(RACESTATE_ID_TO_NAME.keys())

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