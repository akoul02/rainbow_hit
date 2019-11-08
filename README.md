# rainbow hit
### Описание
МИЭМ 2019 проект по питону.  
Игра основанная на том, что игрокам необходимо самостоятельно придумать алгоритм управления роботом, и записать его с помощью предооставленного API.  
Пример возможного алгоритма:
```python
# check if there is enemy around you
if is_enemy(Directions::Left):
    bot.move(Directions::Left, 1)
elif is_enemy(Directions::Right): 
    bot.move(Directions::Right, 1)
elif is_enemy(Directions::Up):
    bot.move(Directions::Up, 1)
elif is_enemy(Directions::Down):
    bot.move(Directions::Down, 1)
else:
    bot.sleep(bot.MAX_ACTIONS - bot.actions)

# fire
bot.fire()
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
    hp: int
    speed: int
    handle: str
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
1. Make n steps in direction specified using dir variable
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
4. Just do nothing for n actions
'''
def sleep(self, n: int) -> None:
    return None
```
|Описание|функция|
|:--:|:--:|
| 1. Переместить робота на __n__ клеток, в заданном с помощью переменной __dir__ направлении | `move(dir: Directions, n: int) -> None` |
| 2. Произвести выстрел | `fire() -> bool` |
| 3. Проверить наличие вражеского объекта в заданном с помощью переменной __dir__ направлении | `check_enemy(dir: Directions) -> int`|
| 4. Ничего не делать, a.k.a. NOP | `sleep(n: int) -> None` |