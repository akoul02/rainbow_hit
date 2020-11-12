# rainbow_hit

### Project Description
HSE miem 2019 python project.

### How to run
Cd to `sources` and run `python3 main.py`

### Game information
#### Tweakable settings
- Labyrinth density can be edited by changing `LABYRINTH_DENSITY` const inside [`./sources/server/constants.py`](https://github.com/m4drat/rainbow_hit/blob/7c3e6411f22bb2ba62f2feb90987a58776f20269/sources/server/game/constants.py#L2). *(Bigger value = maze with more spaces)*
- Bots behaviour can be updated by editing their constructor parameters inside [`./sources/server/game/game.py`](https://github.com/m4drat/rainbow_hit/blob/7c3e6411f22bb2ba62f2feb90987a58776f20269/sources/server/game/game.py#L34) (lines 34, 35)

#### Game steps  
1. The game is fully emulated using the "server" module
2. The game is visualized using the "client" module

#### Running game
- You can write custom python scripts for each of the bots inside this directory: `./rainbow_hit/sources/server/game/bots_code/bot_scripts_sync/`. The code must be written inside a wrapper class BotActivity, which should contain function `perform`. In file `./rainbow_hit/sources/server/game/bots_code/config.py` write names of preferred scripts in variables `p1sc` and `p2sc`.

#### Game screenshots
![StartGame](https://i.imgur.com/8qojgjc.png)
![Gameplay](https://i.imgur.com/7QbjNjD.png)
![GameOver](https://i.imgur.com/oy1Nj9g.png)
