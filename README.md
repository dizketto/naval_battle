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
- the board is limited to 10x10 max and 4x4 min
- the ships have a fixed length of 3 units, and maximum 2 ships per player
- if a ship is hit in the middle, all the 3 units of the ship or the remaining ones, are destroyed
- at the same time a player can hit more than one opponent
- the game ends when only a player is left with its ships on the board, and wins the game

## How to start the game service

### Requirements
- `docker >= 20.10.12`
- `docker-compose >= 1.29.2`

To run the whole infrastructure you can use the Makefile with one of its targets:
 - `run_services_detached` : runs in detached mode and if needed builds the services
 - `build_and_run_services_detached` : builds and run the services in detached mode
 - `run_services` : runs services NOT in detached mode
 - `build_and_run_services` : builds and run services NOT in detached mode
 
 
 ex.
 ```make build_and_run_services_detached```
 
## Using the API
 
The documentation and testing of the API is available at its own swagger, reachable through:
`http://localhost:8000/docs`

![API SWAGGER](https://user-images.githubusercontent.com/58236349/177278846-47002a8c-e952-4cb7-a14e-10f6a64f99f9.png)




To use each endpoint, click on the endpoint and then on the `Try it out` button, you can add the parameters of the request directly in the swagger and then click on the `EXECUTE` button, to send the request. 

### Authentication

First of all an user will sign up to the service through the `/v1/user/signup` endpoint. 
After sending the request, if the data is consistent, you will get an access_token (all the part of sending confirmation email, is not present in the service for conveniency).



![Access Token](https://user-images.githubusercontent.com/58236349/177280335-958451a6-d8d5-42d9-8bb0-1875e4cbb8eb.png)




Successively, you can use the `/v1/user/login` endpoint to access the service with a previously registered user, still obtaining an access token.
To use the access token, you can copy the "access_token" value in the response, click on the button `Authorize` and paste the access token.



![Authorize](https://user-images.githubusercontent.com/58236349/177282254-b0692ffb-fff3-4751-9116-428da15fe8a4.png)





### Creating and joining games
With this access token you can either create or join a game. If there is no other game created, you can't join other games.
Joining a game means that you will request to join any game that still allows players in.
If a joinable game is found, then you will get the access token to play in that game.

You can create or join as many games as you want at the same time, and play several games at the same time.
A game is not started until the number of players in the game matches the setting of the game creation (players_number).
Once all the players have joined the game is closed for joining.

Once a game is created or joined, it will give back a new Access Token. This is the Access Token to be used to play uniquely that game.

### Playing the game
Once again, use the access token obtained from joining or creating the game on the Authorization button (if you already used one to authorize, just logout with this one, paste the new access token, and authorize again)

When all the players for the game is joined, will be possible to start the game.

In the first stage of the game players add their ships to their board using the endpoint `/v1/game/add_ship`. It's sufficient to give one point and the `vertical` flag, and the ship will be created with its center on the point given in input. You need to add 2 ships to be able to play. Just call the endpoint twice with different points/verse.



![add ship](https://user-images.githubusercontent.com/58236349/177284452-3158d2ef-69c5-4ea0-acc9-2dd3e3388422.png)




Once all the players have added their ships, it's possible to start shooting on a turn-based way, using the endpoint `/v1/game/shot`, and giving the coordinates point where you want to shoot.
The response will show what was the effect on other players, for each player the outcome will be MISSED, HIT, or DESTROYED.
In case a ship gets destroyed, it will also return all the points of the ship's units.



![missed ship](https://user-images.githubusercontent.com/58236349/177285415-9f5c47bc-516b-4481-833f-a957981f814d.png)




### Stats and Utils

For convenience, there is a "cheating" endpoint that can show the board and the ships for a user for the game associated to the specific token.
`/v1/reveal`



![Reveal](https://user-images.githubusercontent.com/58236349/177286800-2fd3ec75-e138-4c32-9326-4193f77ef6aa.png)


#### Scores

You can check the user scores chart using the `/v1/scores` endpoint.



![scores](https://user-images.githubusercontent.com/58236349/177288260-ee7ce55e-86f7-40cd-98ee-525682745ed4.png)















