# rainbow hit
### Описание
МИЭМ 2019 проект по питону.  
Игра основанная на том, что игрокам необходимо самостоятельно придумать алгоритм управления роботом, и записать его с помощью предоставленного API.  
Пример возможного алгоритма:
```python
# check if there is enemy around you
res = is_enemy_around()
if res != None:
    if res.distance <= bot.shot_distance:
        bot.rotate(res.direction)
        bot.fire()
    else:
        bot.move(res.direction, res.distance - bot.shot_distance)
        bot.fire()
else:
    bot.sleep(100)
```
### Структура Приложения
- Серверная часть:  
    * Логика бекенда (управление роботами, выполнение их алгоритма)  
    * Часть, которая будет взаимодействовать с веб-страницей (обновлять ее состояние (WebSockets?)) 
- Клиентская часть (веб приложение):  
    * Форма для отправки кода управления ботом  
        * поле для ввода кода c кнопкой "send" (mini-ide)
        * Кнопка "ready". 
            * Становится активной атоматически после отправки кода (в это время поле с кодом "замораживается"). 
            * Если кликнуть по активной, то у игрока снова появляется возможность изменить код, после чего снова его отправить. 
            * Когда будет активна у всех, игра начнется.
        * Кнопка "send". Отправит код для бота на сервер
    * Окно с визуализацией действий ботов
        * Игровой процесс
        * Статистика побед/поражений

Визуальное представление:
![DrawIo layout](https://i.imgur.com/EBDFnnJ.png?2)
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
class Direction(enum.Enum):
    North     = N  = Up        = 1
    NorthEast = NE = RightUp   = UpRight   = 2
    East      = E  = Right     = 3
    SouthEast = SE = DownRight = RightDown = 4 
    South     = S  = Down      = 5 
    SouthWest = SW = LeftDown  = DownLeft  = 6
    West      = W  = Left      = 7 
    NorthWest = NW = LeftUp    = UpLeft    = 8 
```

Класс описывающий направление и дистанцию:
```python
@dataclass
class DirDist():
    direction: Direction = None
    distance:  int = None
```

Описание прототипов функций:
```python
'''
1. Make n > 0 steps in direction specified using dir variable
Return:
    None
'''
def move(self, dir: Direction, n: int) -> None:
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
def check_enemy(self, dir: Direction) -> int:
    return distance_to_enemy

'''
MAY NOT BE IN THE FINAL VERSION!
4. Check if there is enemy object in all possible Directions.
Return:
    if enemy found returns DirDist instance with DirDist.direction = direction to enemy, DirDist.distance = distance to enemy
    otherwise returns None
'''
def is_enemy_around(self) -> DirDist:
    return DirDist

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
| 1. Переместить робота на __n__ клеток, в заданном с помощью переменной __dir__ направлении | `move(dir: Direction, n: int) -> None` |
| 2. Произвести выстрел | `fire() -> bool` |
| 3. Проверить наличие вражеского объекта в заданном с помощью переменной __dir__ направлении | `check_enemy(dir: Direction) -> int`|
| 4. Проверить наличие вражеского объекта во всех возможных направлениях | `is_enemy_around() -> DirDist`|
| 5. Ничего не делать, в течении __n__ миллисекунд | `sleep(n: int) -> None` |
| 6. Развернуть робота в направлении указанном в переменной __dir__ | `rotate(dir: Direction) -> None` |