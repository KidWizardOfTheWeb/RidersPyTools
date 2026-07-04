# RidersPyTools

Package designed to write scripts for Sonic Riders (GameCube) and Sonic Riders: Zero Gravity (Wii). Compatible with vanilla/all mods.

Still a MAJOR work in progress, but functional at a basic level for now.

## Code style

We enforce the same standards as the Sonic Riders: Tournament Edition C++ codebase for Sonic Riders, aiming to be as close as possible in syntax to the existing decompilation.

In some cases, this isn't 100% possible, but it remains the goal, as this allows us to read code similarly between C++ and python, 
as well as provide a bridge for newer users learning to program to jump into the C++ side of things.

Other games may have different data structures and syntax, feel free to add/modify classes as needed to fit your game.

Some concepts:

Ways to get a player pointer:
Instantiate a player object in Python:

`player1 = Player(0) # Instantiates a pointer to player 1, based on the current game version detected.`

Instantiate a player object starting at X address:

```python
player1Vanilla = Player(0, 0x80609440) # Vanilla address
player1TE = Player(0, TE_PLAYER_PTR) # Some addresses are given identifiers for ease of use
```

Things you can do:

Read data:

`print(player1.rings)`

Compare data:

```python
player1 = Player(0, 0x80609440)
if player1.rings > 0:
    print("You have at least one ring!")
```

Write data:

```python
player1 = Player(0, 0x80609440)
player1.currentAir = 100000
player1.gearStats[int(player1.level)].boostSpeed = pSpeed(300.0)
```

Math operations:
```python
player1 = Player(0, 0x80609440)
hundredRingDiff = 100 - int(player1.rings)
print(hundredRingDiff)
```

And you can integrate this into other scripts too!

We use hatchling to compile the builds. Build compilation instructions coming soon.