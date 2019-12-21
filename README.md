# rainbow_hit

### Project Description
HSE miem 2019 python project.

### How to run
While you're **exactly** in rainbow_hit directory run `python3 ./sources/main.py`

### Game information
#### Tweakable settings
- Labyrinth density can be edited by changing `LABYRINTH_DENSITY` const inside `./sources/server/constants.py`. *(Bigger value = maze with more spaces)*
- Bots behaviour can be updated by editing their constructor parameters inside `./sources/server/game/game.py` (lines 34, 35)

#### Game steps  
1. The game is fully emulated using the "server" module
2. The game is visualized using the "client" module

#### Running game
- You can write any python code for each of the bots inside this file: `./rainbow_hit/sources/server/game/bots_code/code.py`. The code must be written in the body of the `run_user1` and `run_user2`.

#### Game screenshots
![StartGame](https://i.imgur.com/N5gDV8M.png)
![GameOver](https://i.imgur.com/axErrF5.png)