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
- docker >= 20.10.12
- docker-compose >= 1.29.2

To run the whole infrastructure you can use the Makefile with one of its targets:
 - run_services_detached : runs in detached mode and if needed builds the services
 - build_and_run_services_detached : builds and run the services in detached mode
 - run_services : runs services NOT in detached mode
 - build_and_run_services : builds and run services NOT in detached mode
 
 ```
  make build_and_run_services_detached
 ```
 
 ## Using the API
 
 The documentation and testing of the API is available at its own swagger, reachable through:
 `http://localhost:8000/docs`
 
 ![API SWAGGER](https://user-images.githubusercontent.com/58236349/177278846-47002a8c-e952-4cb7-a14e-10f6a64f99f9.png)

