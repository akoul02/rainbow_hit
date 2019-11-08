# rainbow hit
### Описание
МИЭМ 2019 проект по питону.  
Игра основанная на том, что игрокам необходимо самостоятельно придумать алгоритм управления роботом, и записать его с помощью предооставленного API.  
Пример возможного алгоритма:
```python
# check if there is enemy around you
res = is_enemy_around()
if res != None:
    direct = res[0]
    distan = res[1]

    if distan <= bot.shot_distance:
        bot.rotate(direct)
        bot.fire()
    else:
        bot.move(direct, distan - bot.shot_distance)
        bot.fire()
else:
    bot.sleep(100)
```
### Структура Приложения
1. Серверная часть:  
    1.1 Логика бекенда
    1.2       
2. Клиентская часть (веб приложение):  
    2.1 Форма для отправки кода управления ботом  
    2.2 Окно с визуализацией действий ботов  
Визуальное представление:

### Описание API
- Игрокам дается ссылка объект класса Bot: bot.  

Класс описывающий поля робота:
```python
@dataclass
class Bot():
    MAX_SHOT_DST: int
    MIN_SHOT_DST: int
    shot_distance: int

    MAX_HEALTH: int
    MIN_HEALTH: int
    health: int

    MAX_SPEED: int
    MIN_SPEED: int
    speed: int

    DEFAULT_HANDLE: str
    handle: str

    MAX_DAMAGE: int
    MIN_DAMAGE: int
    damage: int
```

Класс описывающий возможные направления в виде перечисления:
```python
import enum
class Directions(enum.Enum):
    North     = N  = Up        = 1
    NorthEast = NE = RightUp   = UpRight   = 2
    East      = E  = Right     = 3
    SouthEast = SE = DownRight = RightDown = 4 
    South     = S  = Down      = 5 
    SouthWest = SW = LeftDown  = DownLeft  = 6
    West      = W  = Left      = 7 
    NorthWest = NW = LeftUp    = UpLeft    = 8 
```
Описание прототипов функций
```python
'''
1. Make n > 0 steps in direction specified using dir variable
Return:
    None
'''
def move(self, dir: Directions, n: int) -> None:
    return None

'''
2. Fire in direction, you're currently looking in
Return:
    return true, if you're hitted enemy, otherwise return false
'''
def fire(self) -> bool:
    return is_hit_success

'''
3. Check if there is an enemy in specific direction specified by dir variable
Return:
    return distance to enemy in cells, or -1 if there is no enemies on the row
'''
def check_enemy(self, dir: Directions) -> int:
    return distance_to_enemy

'''
4. Check if there is enemy object in all possible directions.
Return:
    if enemy found returns list with first element = direction to enemy, and second = distance to enemy
    otherwise returns None
'''
def is_enemy_around(self) -> dict(dir: Direction, dist: int):
    return dict(dir: Direction, dist: int)

'''
5. Just do nothing for n milliseconds
'''
def sleep(self, n: int) -> None:
    return None

'''
6. Rotate bot in dir: Direction
'''
def rotate(self, dir: Direction) -> None:
    return None
```
|Описание|функция|
|:--:|:--:|
| 1. Переместить робота на __n__ клеток, в заданном с помощью переменной __dir__ направлении | `move(dir: Directions, n: int) -> None` |
| 2. Произвести выстрел | `fire() -> bool` |
| 3. Проверить наличие вражеского объекта в заданном с помощью переменной __dir__ направлении | `check_enemy(dir: Directions) -> int`|
| 4. Проверить наличие вражеского объекта во всех возможных направлениях | `is_enemy_around() -> dict(dir: Direction, dist: int)`|
| 5. Ничего не делать, a.k.a. NOP | `sleep(n: int) -> None` |
| 6. Развернуть робота в направлении указанном в переменной __dir__ | `rotate(dir: Directions) -> None` |