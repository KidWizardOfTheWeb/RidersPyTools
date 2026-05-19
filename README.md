# RidersPyTools

Package designed to write scripts for Sonic Riders (GameCube) and Sonic Riders: Zero Gravity (Wii). Compatible with vanilla/all mods.

Still a MAJOR work in progress, but functional at a basic level for now.

## Code style

We enforce the same standards as the SRTE C++ codebase, aiming to be as close as possible in syntax.

In some cases, this isn't 100% possible, but it remains the goal, as this allows us to read code similarly between C++ and python, 
as well as provide a bridge for newer users learning to program to jump into the C++ side of things.

Some concepts:

Ways to get a player pointer:
Instantiate a player object in Python:

`player1 = Player(0)`

Instantiate a player object starting at X address:

`player1 = Player(0, 0x80609440)`

Things you can do:

Read data:

`print(player1.rings)`

```python
if player1.rings > 0:
    print("You have at least one ring!")
```

Write data:

```python
player1.currentAir = 100000
player1.gearStats[int(player1.level)].boostSpeed = pSpeed(300.0)
```

And you can integrate this into other scripts too!

We use hatchling to compile the builds. Build compilation instructions coming soon.