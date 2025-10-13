# RidersPyTools

Package designed to write scripts for Sonic Riders (GameCube) and Sonic Riders: Zero Gravity (Wii). Compatible with vanilla/all mods.


Ways to get a player:
list of players -> index of dicts containing offsets for player -> data offset dict

RidersPlayers[0]["rings"]

Ways to call a function:
function key for dict -> parameters

RidersFunc["lbl_0009623C"](players[0])

Ways to read/write data.s:
data key for dict

RidersDataS["data_C24DB2D8"]