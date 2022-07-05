# Naval Battle Game API

This game is based on the classic "naval battle".

## Rules
### Naval Battle rules
Each player has a board of NxM cells (N and M can be equal). Normally the game is played by 2 players. The first step is for each player to decide 
where to allocate their ships that consist of 1 or more consecutive cells.
Successively, on each turn, a player will pick a cell in the board, identified by a tuple (X,Y). If on the other player's board there is a cell composing the ship, then this unit will be lost.
The game ends when one of the players has lost all of its units.

### Naval Battle Revisited
The current implementation adds some revisited rules:
- up to 4 players can join a game
- the ships have a fixed length of 3 units
- if a ship is hit in the middle, all the 3 units, or the remaining ones, are lost
- at the same time a player can hit more than one opponent
- the game ends when only a player is left with its ships on the board, and wins the game

## How to start the game service

### Requirements
docker >= 20.10.12
docker-compose >= 1.29.2

To run the whole infrastructure:
