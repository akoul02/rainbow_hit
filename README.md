# rainbow hit
### Описание
МИЭМ 2019 проект по питону.  
Игра основанная на том, что игрокам необходимо самостоятельно придумать алгоритм управления роботом, и записать его с помощью предоставленного API.  

### Задачи
- Представление игрового мира
- Своевременное оформление тестов и документации в процессе написания (сдаешь функцию = есть тесты и документация)
- Разделение на модули
- GUI? (web/pySimpleGUI)

Пример возможного алгоритма:
```python
# check if there is enemy around you
res = is_enemy_around()
if res != None:
    if res.distance <= bot.shot_distance:
        bot.rotate(~res.direction)
    else:
        bot.move(res.direction, res.distance - bot.shot_distance)
        bot.rotate(~res.direction)
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

Визуальное представление (client-side):  
![DrawIo client-side layout](https://i.imgur.com/EBDFnnJ.png?3)

Система передвижения/координат в игровом мире:
- Боты могут передвигаться в 8 направлениях
- У ботов есть "поле зрения" (FOV), в границах которго, они могут "видеть" объекты

![location system](https://i.imgur.com/Z5iXOvs.png)

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

    # overloading '~' operator
    def __invert__(self):
        if self == self.N:
            return self.S
        elif self == self.NE:
            return self.SW
        elif self == self.E:
            return self.W
        elif self == self.SE:
            return self.NW
        elif self == self.S:
            return self.N
        elif self == self.SW:
            return self.NE
        elif self == self.W:
            return self.E
        elif self == self.NW:
            return self.SE
```

Класс описывающий возможные объекты:
```python 
import enum
class ObjectType(enum.Enum):
    enemy    = 1
    power_up = 2
    bullet   = 3
```

Класс описывающий направление, дистанцию и другие характеристики объекта:
```python
@dataclass
class ObjectDescriptor():
    direction: Direction = None
    distance: int = None
    x: int = None
    y: int = None
    obj_type: ObjectType = None
```

Описание прототипов функций:
```python
'''
1. Make n > 0 steps in direction specified using dir variable

Parameters
----------
dir : Direction
    specify direction in which you want to move
n : int
    number of steps
    
Returns
-------
    None
'''
def move(self, dir: Direction, n: int) -> None:
    return None

'''
2. Fire in direction, you're currently looking in

Returns
-------
    true, if you're hitted enemy, otherwise false
'''
def fire(self) -> bool:
    return is_hit_success

'''
3. Check if there is an enemy in selected direction specified by dir variable

Parameters
----------
dir: Direction
    direction, where you want to check for enemy presence

Returns
-------
    return distance to enemy in cells, or -1 if there is no enemies on the row
'''
def check_enemy(self, dir: Direction) -> int:
    return distance_to_enemy

'''
MAY NOT BE IN THE FINAL VERSION!
4. Check if there is object in in FOV.

Returns
------
    if object is found returns ObjectDescriptor instance with:
    ObjectDescriptor.direction = direction to object,
    ObjectDescriptor.distance  = distance to object,
    ObjectDescriptor.x = object .x coordinate
    ObjectDescriptor.y = object .y coordinate
    ObjectDescriptor.obj_type = object .obj_type 

    # TODO maybe it's better, to return object itself, without any additional obj_type, etc

    otherwise returns None
'''
def is_object_around(self) -> ObjectDescriptor:
    return ObjectDescriptor()

'''
5. Just do nothing for n milliseconds

Parameters
----------
n: int
    amount of milliseconds to sleep 

Returns
------
    None
'''
def sleep(self, n: int) -> None:
    return None

'''
6. Rotate bot in dir: Direction

Parameters
----------
dir: Direction
    the direction you want to turn

Returns
------
    None
'''
def rotate(self, dir: Direction) -> None:
    return None
```
|Описание|функция|
|:--:|:--:|
| 1. Переместить робота на __n__ клеток, в заданном с помощью переменной __dir__ направлении | `move(dir: Direction, n: int) -> None` |
| 2. Произвести выстрел | `fire() -> bool` |
| 3. Проверить наличие вражеского объекта в заданном с помощью переменной __dir__ направлении | `check_enemy(dir: Direction) -> int`|
| 4. Проверить наличие вражеского объекта во всех возможных направлениях | `is_enemy_around() -> ObjectDescriptor`|
| 5. Ничего не делать, в течении __n__ миллисекунд | `sleep(n: int) -> None` |
| 6. Развернуть робота в направлении указанном в переменной __dir__ | `rotate(dir: Direction) -> None` |