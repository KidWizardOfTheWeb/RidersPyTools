"""
CLASS SCHEMA FOR PLAYER
"""

from enum import IntEnum, IntFlag

import dolphin_memory_engine as DME
from .include.Controller import Controller
from .include.GenericData import GenericData
from .include.GearStats import GearStats
from .include.Constants import *
from .GameState import GAME_VERSION

INIT_STATE = True

# Rename to TypeSkill for clarity? Unsure.
class Type(IntFlag):
    noType = 0,
    Speed = 1 << 0,
    Fly = 1 << 1,
    Power = 1 << 2,
    All = 1 << 0 | 1 << 1 | 1 << 2

class TrickRanks(IntEnum):
    CRank = 0,
    BRank = 1,
    ARank = 2,
    APlusRank = 3,
    SRank = 4,
    SPlusRank = 5,
    XRank = 6,
    TenPlus = 7

class MovementFlags(IntFlag):
    none = 0,
    drifting = 1 << 14,
    boosting = 1 << 10,
    jumpCharge = 1 << 12,
    railLink = 1 << 16,
    braking = 1 << 8,
    TurbulenceLRExit = 1 << 18,
    noBoostChain = 1 << 13

class PlayerState(IntEnum):
    QTE = 0x0,
    StartLine = 0x1,
    Unknown = 0x2,
    Death = 0x3,
    Retire = 0x4,
    Cruise = 0x5,
    Jump = 0x6,
    Fall = 0x7,
    FrontflipRamp = 0x8,
    BackflipRamp = 0x9,
    UnknownTrick = 0xA,
    HalfPipeTrick = 0xB,
    ManualRamp = 0xC,
    TurbulenceTrick = 0xD,
    TurbulenceTrick2 = 0xE,
    PlayerCollide = 0xF,
    TurbulenceRide = 0x10,
    QTE2 = 0x11,
    RailGrind = 0x12,
    Fly = 0x13,
    AttackingPlayer = 0x15,
    AttackedByPlayer = 0x16,
    Stun = 0x17,
    Unk1 = 0x18,
    Run = 0x19,
    StartLineShock = 0x1A,
    Unknown2 = 0x1B

class PlayerFlags(IntFlag):
    none					= 0,
    WallGrind				= 1 << 0,
    Unknown					= 1 << 2,
    WallBonk				= 1 << 5,
    Unknown2				= 1 << 8,
    OnTurbulence			= 1 << 11,
    TurbulenceLRExit		= 1 << 14,
    RaceWin					= 1 << 19,
    ItemBoxCooldown			= 1 << 21,
    InAPit					= 1 << 25,

class PlayerStatus(IntFlag):
    NoStatus 				= 0,
    BallAndChainStatus 		= 1 << 0,
    MagnetStatus			= 1 << 2,
    InvincibilityStatus 	= 1 << 4


class Player:
    def __getattr__(self, name):
        global INIT_STATE

        if INIT_STATE:
            return None

        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_read = vars(self.__getattribute__(name))["_datatype"]
        offset_to_read = vars(self.__getattribute__(name))["_offset"]

        # Check our types, read from game, return value if found
        if 'READ_FROM_DME' in name:
            try:
                value_read = None
                if type_to_read == u8 or type_to_read == s8 or type_to_read == Bool:
                    value_read = DME.read_byte(offset_to_read)
                if type_to_read == u16 or type_to_read == s16:
                    value_read = DME.read_byte(offset_to_read)
                if type_to_read == u32 or type_to_read == s32 or type_to_read == vu32:
                    value_read = DME.read_word(offset_to_read)
                if type_to_read == f32:
                    value_read = DME.read_float(offset_to_read)
                if value_read is None:
                    # No types were valid, read bytes instead
                    value_read = DME.read_bytes(offset_to_read, type_to_read)
                return value_read
            except RuntimeError as e:
                print("RuntimeError: DME is " + str(e) + ". Failed to return value.")
        return vars(self.__getattribute__(name))
    def __setattr__(self, name, value):
        global INIT_STATE

        # On startup, this allows everything to be assigned to the player object.
        # We NEED this for init ONLY.
        # Once every struct variable is done, SET INIT_STATE = False.
        # Once that is done, this will retrieve data from DME instead of setting the attribute's value.
        if INIT_STATE:
            super().__setattr__(name, value)
            return
        # Use this function for GenericData value assignment that isn't setting equal to a new object instance (that's handled in their own classes)

        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        # check_DME_value = vars(self.__getattribute__(name))
        type_to_write = vars(self.__getattribute__(name))["_datatype"]
        offset_to_write = vars(self.__getattribute__(name))["_offset"]

        # Check our types, read from game, return value if found
        try:
            if type_to_write == u8 or type_to_write == s8 or type_to_write == Bool:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u16 or type_to_write == s16:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u32 or type_to_write == s32 or type_to_write == vu32:
                DME.write_word(offset_to_write, value)
            if type_to_write == f32:
                DME.write_float(offset_to_write, value)
        except RuntimeError as e:
            print("RuntimeError: DME is " + str(e) + ". Failed to write new value.")
        return
    def __init__(self, playerNum, playerPtr=None):
        global INIT_STATE
        INIT_STATE = True
        # TODO: If TE, use the map file instead of this for ptr
        # If a player pointer is passed in, use that instead and skip the match.
        # This is especially helpful for when TE builds change pointers and the ptr hasn't been updated in the constants yet.
        if playerPtr:
            self.playerPtr = playerPtr + (0x1080 * playerNum)
        else:
            match GAME_VERSION:
                # Vanilla based IDs for vanilla, DX, FT
                case GameIDs.SONIC_RIDERS_ID:
                    self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
                case GameIDs.SONIC_RIDERS_DX_ID:
                    self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
                case GameIDs.SONIC_RIDERS_FT_ID:
                    self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)

                # TE is special, as the game is a shiftable dol.
                # I'd suggest using the map file to figure out what this is supposed to be,
                # Or having a user enter it manually if no map is passed in.
                case GameIDs.SONIC_RIDERS_TE_ID:
                    self.playerPtr = TE_PLAYER_PTR + (0x1080 * playerNum)

                # ZG has dynamic player ptrs, this is not very reliable as of now.
                case GameIDs.SONIC_RIDERS_ZG_ID:
                    self.playerPtr = ZG_PLAYER_PTR + (0x1120 * playerNum)
                case _:
                    pass
        pass
        # Inputs are always defined on game load, at least for P1.
        # The input ptr is always at the start of the playerPtr struct, so just read word from here and pass the struct ID
        ptr_start_addr = self.playerPtr

        # Go to pointer for controls, starts at offset 0
        self.input = Controller(DME.follow_pointers(ptr_start_addr, [0]), ptr)
        self.tornadoInvulnerabilityTimer = GenericData(ptr_start_addr + 0x4, u8)
        self.ignoreTurbulence = GenericData(ptr_start_addr + 0x8, Bool)

        self.character = GenericData(ptr_start_addr + 0xBA, u8)
        self.extremeGear = GenericData(ptr_start_addr + 0xBB, u8)
        self.aiControl = GenericData(ptr_start_addr + 0xBC, Bool)
        self.playerType = GenericData(ptr_start_addr + 0xBD, Bool)
        self.gearType = GenericData(ptr_start_addr + 0xBE, u8)
        self.attributes = GenericData(ptr_start_addr + 0xBF, u8)
        self.current_itemID = GenericData(ptr_start_addr + 0xF4, u32)
        self.tornadoIgnore_invincibilityTimer = GenericData(ptr_start_addr + 0xF8, u8)
        self.characterVoiceID = GenericData(ptr_start_addr + 0xFA, u16)
        # self.currentCollision = GenericData(DME.follow_pointers(ptr_start_addr, [0]), ptr) // Needs collision class.
        self.gearSpecificFlags = GenericData(ptr_start_addr + 0x100, u32) # Bitset for level 4.
        self.maxJump = GenericData(ptr_start_addr + 0x104, u8)
        self.midJump = GenericData(ptr_start_addr + 0x105, u8)
        self.badJump = GenericData(ptr_start_addr + 0x106, u8)
        self.absoluteMaxJump = GenericData(ptr_start_addr + 0x107, u8)
        self.last_itemID_lap = GenericData(ptr_start_addr + 0x108, u8)
        self.trickCount = GenericData(ptr_start_addr + 0x109, u8)
        self.last_itemID = GenericData(ptr_start_addr + 0x10C, u32)
        self.last_itemBox_random = GenericData(ptr_start_addr + 0x110, Bool)
        self.last_level4 = GenericData(ptr_start_addr + 0x111, Bool)
        self.rainbowTrailState = GenericData(ptr_start_addr + 0x112, Bool)
        self.dreamTrail_timer = GenericData(ptr_start_addr + 0x113, u8)
        self.exhaustTrailColor = GenericData(ptr_start_addr + 0x114, u32) # Uses RGBA class
        self.berserkerCooldown = GenericData(ptr_start_addr + 0x118, u8)  # Uses RGBA class

        # State unions (same addresses, different names)
        self.coverF_archetype = GenericData(ptr_start_addr + 0x11A, u8)
        self.superFormState = GenericData(ptr_start_addr + 0x11A, u8)
        self.coverP_weightState = GenericData(ptr_start_addr + 0x11A, u8)

        self.slipstream = GenericData(ptr_start_addr + 0x11B, Bool)
        self.magneticImpulse_timer = GenericData(ptr_start_addr + 0x11C, f32)
        self.turningSpeedLoss = GenericData(ptr_start_addr + 0x120, f32)
        self.x = GenericData(ptr_start_addr + 0x1E4, f32)
        self.y = GenericData(ptr_start_addr + 0x1E8, f32)
        self.z = GenericData(ptr_start_addr + 0x1EC, f32)
        self.verticalRotation = GenericData(ptr_start_addr + 0x1F0, f32)
        self.horizontalRotation = GenericData(ptr_start_addr + 0x1F4, f32)
        self.rotationRoll = GenericData(ptr_start_addr + 0x1F8, f32)

        self.xDifferenceFromNextPlayer = GenericData(ptr_start_addr + 0x340, f32)
        self.yDifferenceFromNextPlayer = GenericData(ptr_start_addr + 0x344, f32)
        self.zDifferenceFromNextPlayer = GenericData(ptr_start_addr + 0x348, f32)

        # Uses Vector3F (X float, y float, z float)
        # Replace with class instance later rather than array.
        self.forward = [GenericData(ptr_start_addr + 0x358, f32), GenericData(ptr_start_addr + 0x35C, f32), GenericData(ptr_start_addr + 0x360, f32)]

        self.currPathFindingPoint = GenericData(ptr_start_addr + 0x5E6, u16)
        self.prevPathFindingPoint = GenericData(ptr_start_addr + 0x5E8, u16)

        self.railState = GenericData(ptr_start_addr + 0x624, u16)
        self.railPart = GenericData(ptr_start_addr + 0x626, u16)
        self.railID = GenericData(ptr_start_addr + 0x628, u16)
        self.collisionProperties = GenericData(ptr_start_addr + 0x6C0, u16) # Has IDs. Add later.
        self.railID = GenericData(ptr_start_addr + 0x6C4, u16)
        self.turbulenceState = GenericData(ptr_start_addr + 0x6C8, u16)

        self.lastAnimationID = GenericData(ptr_start_addr + 0x764, u32)
        self.currentAnimationID = GenericData(ptr_start_addr + 0x764, u32)
        self.animationFlags = GenericData(ptr_start_addr + 0x764, u32) # Has its own flag class, add later.
        self.currentAnimationFrame = GenericData(ptr_start_addr + 0x770, f32)
        self.animationSpeed = GenericData(ptr_start_addr + 0x784, f32)

        # Timer union
        self.fastest_timer = GenericData(ptr_start_addr + 0x87C, u32)
        self.superTails_transformCooldown = GenericData(ptr_start_addr + 0x87C, u32)
        self.hyperSonic_totalLinkTimer = GenericData(ptr_start_addr + 0x87C, u32)
        self.SuperMetalFrameCounter = GenericData(ptr_start_addr + 0x87C, u32)

        self.boostDuration = GenericData(ptr_start_addr + 0x8AC, s32)
        self.lightBoard_flag = GenericData(ptr_start_addr + 0x8C0, u32)

        # GearStats[3] -> index per level
        self.gearStats = [GearStats(ptr_start_addr + 0x8DC, u32), GearStats(ptr_start_addr + 0x914, u32), GearStats(ptr_start_addr + 0x94C, u32)]
        self.currentAir = GenericData(ptr_start_addr + 0x984, u32)
        self.changeInAir_gain = GenericData(ptr_start_addr + 0x988, u32)
        self.changeInAir_loss = GenericData(ptr_start_addr + 0x98C, u32)
        self.weight = GenericData(ptr_start_addr + 0x994, f32)
        self.requiredDriftDashFrames = GenericData(ptr_start_addr + 0x9C4, s32)
        self.trickAirGainMultiplier = GenericData(ptr_start_addr + 0x9C8, f32)
        self.shortcutAirGainMultiplier = GenericData(ptr_start_addr + 0x9CC, f32)
        self.QTEAirGainMultiplier = GenericData(ptr_start_addr + 0x9D0, f32)
        self.specialFlags = GenericData(ptr_start_addr + 0x9D4, u32) # Uses SpecialFlags enum
        self.trickSpeed = GenericData(ptr_start_addr + 0x9E0, u32)
        self.trickDirection = GenericData(ptr_start_addr + 0x9E8, u32)
        self.jumpCharge = GenericData(ptr_start_addr + 0x9F4, u16)
        self.startingTrick = GenericData(ptr_start_addr + 0x9F8, u8)
        self.rampType = GenericData(ptr_start_addr + 0x9F9, u8)
        self.trickTrajectory = GenericData(ptr_start_addr + 0x9FE, u8)
        self.trickRank = GenericData(ptr_start_addr + 0x9FF, u8) # Uses trick rank enum
        self.trickFail = GenericData(ptr_start_addr + 0xA03, u8)

        self.movementFlags = GenericData(ptr_start_addr + 0xA28, u32) # Uses movement flags enum
        self.last_movementFlags = GenericData(ptr_start_addr + 0xA2C, u32)

        self.characterptr = GenericData(ptr_start_addr + 0xA40, u32) # Uses character ptr class
        self.gearptr = GenericData(ptr_start_addr + 0xA44, u32) # Uses gear ptr class

        self.verticalSpeed = GenericData(ptr_start_addr + 0xAA4, f32)
        self.generalSpeedLoss = GenericData(ptr_start_addr + 0xAA8, f32)
        self.speed = GenericData(ptr_start_addr + 0xAAC, f32)
        self.maxSpeedPercentage = GenericData(ptr_start_addr + 0xAB0, f32)
        self.speedCap = GenericData(ptr_start_addr + 0xAB4, f32)
        self.minSpeedCap = GenericData(ptr_start_addr + 0xAB8, f32)

        # Float distance from other players, 8 entries total.
        self.otherPlayerDistance = [GenericData(ptr_start_addr + x, f32) for x in range (0xAD4, 0xAF0, 0x4)]

        self.speedAsInt = GenericData(ptr_start_addr + 0xABC, u32)

        self.driftDirection = GenericData(ptr_start_addr + 0xB4C, f32)
        self.driftDashFrames = GenericData(ptr_start_addr + 0xB54, s32)
        self.boostingAnimationID = GenericData(ptr_start_addr + 0xB7C, u32)

        # List of laps and their times in centiseconds, up to 99 laps
        self.lapTimeList = [GenericData(ptr_start_addr + x, u32) for x in range(0xBF4, 0xD7C, 0x4)]

        self.rings = GenericData(ptr_start_addr + 0xB98, u32)

        # Add flags for this class
        self.playerDisplayFlags = GenericData(ptr_start_addr + 0xBA8, u32)

        self.statusEffectFlags = GenericData(ptr_start_addr + 0xBB0, u32)

        self.stageProgress = GenericData(ptr_start_addr + 0xBC4, f32)

        # Uses type enum
        self.typeAttributes = GenericData(ptr_start_addr + 0xBD3, u8)

        # Last recorded lap as an int, in centiseconds.
        self.lastSplitLapTime = GenericData(ptr_start_addr + 0xD80, u32)

        self.closestTurbulenceIndex = GenericData(ptr_start_addr + 0xE90, u32)

        # Ptrs to attacking/who's attacked.
        # Needs their own structs.
        # self.attackedPlayer = GenericData(ptr_start_addr + 0xF38, u32)
        # self.attackingPlayer = GenericData(ptr_start_addr + 0xF3C, u32)
        # self.attackProperties = GenericData(ptr_start_addr + 0xF40, u32)

        # This is an array of bytes:
        # 1st byte = ms, 2nd byte = sec, 3rd byte = min
        self.raceFinishTime = [GenericData(ptr_start_addr + 0xFF4, u8), GenericData(ptr_start_addr + 0xFF5, u8), GenericData(ptr_start_addr + 0xFF6, u8)]
        # Note: on lap being completed, this resets to zero in-game.
        self.lapElapsedTime = [GenericData(ptr_start_addr + 0xFF8, u8), GenericData(ptr_start_addr + 0xFF9, u8), GenericData(ptr_start_addr + 0xFFA, u8)]

        self.reciproExtendTimer = GenericData(ptr_start_addr + 0x101A, u16)
        self.death_spawnPoint = GenericData(ptr_start_addr + 0x101E, u16)
        self.index = GenericData(ptr_start_addr + 0x1029, u8)
        self.currentLap = GenericData(ptr_start_addr + 0x102A, u8)
        self.previousLap = GenericData(ptr_start_addr + 0x102B, u8)
        self.placement_counter = GenericData(ptr_start_addr + 0x102C, u8)
        self.placement = GenericData(ptr_start_addr + 0x102D, u8)
        self.level = GenericData(ptr_start_addr + 0x102E, u8)
        self.subState = GenericData(ptr_start_addr + 0x102F, u8)
        self.state = GenericData(ptr_start_addr + 0x1034, u8)
        self.previousState = GenericData(ptr_start_addr + 0x1035, u8)
        self.turbulenceTrickType = GenericData(ptr_start_addr + 0x1042, u8) # Uses trick enum
        self.qteState = GenericData(ptr_start_addr + 0x1043, u8)
        self.unk1044 = GenericData(ptr_start_addr + 0x1044, u8)
        self.stage_subState = GenericData(ptr_start_addr + 0x1048, u8)
        self.greenCave_subState = GenericData(ptr_start_addr + 0x105C, u8)
        self.y_toggle = GenericData(ptr_start_addr + 0x1068, u8)
        self.grindRailDash = GenericData(ptr_start_addr + 0x106A, u8)
        self.flyHoopDash = GenericData(ptr_start_addr + 0x106B, u8)
        self.splashCanyonFlyRoute = GenericData(ptr_start_addr + 0x106C, Bool)
        self.airBroomParticles = GenericData(ptr_start_addr + 0x106D, Bool)
        self.specialReciproExtend = GenericData(ptr_start_addr + 0x106E, Bool)
        self.magneticImpulse_soundStatus = GenericData(ptr_start_addr + 0x1079, u8)

        # TE SPECIFIC, all other builds check "archetype" with character checks instead
        self.characterArchetype = GenericData(ptr_start_addr + 0x107C, u8)

        # Extra union
        self.fastest_superCruise = GenericData(ptr_start_addr + 0x107E, Bool)
        self.stardustspeederII_1frameboost = GenericData(ptr_start_addr + 0x107E, Bool)

        # TE SPECIFIC
        self.canBeAttacked = GenericData(ptr_start_addr + 0x107F, Bool)


        # DO NOT TOUCH, REQUIRED FOR INIT/RUNTIME TO WORK
        INIT_STATE = False