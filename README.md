# rainbow hit
### Описание
МИЭМ 2019 проект по питону.  
Пошаговая игра основанная на том, что игрокам необходимо самостоятельно придумать алгоритм управления роботом, и записать его с помощью предооставленного API.  
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
    1.1 Логика бекенда ()  
    1.2 123      
2. Клиентская часть (веб приложение):  
    2.1 Форма для отправки кода управления ботом  
    2.2 Окно с визуализацией действий ботов  
Визуальное представление:

### Описание API
- Игрокам дается ссылка объект класса Bot: bot.  
- Игрокам предоставляется возможность совершения __10__ действий в течении одного хода.

Класс описывающий поля робота:
```python
@dataclass
class Bot():
    # mac actions per move
    MAX_ACTIONS: int = 10
    # number of actions currently used
    actions: int = 0
```

Класс описывающий возможные направления в виде перечисления:
```python
import enum
class Directions(enum.Enum):
   Up    = 1
   Down  = 2
   Left  = 3
   Right = 4
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
def is_enemy(self, dir: Directions) -> int:
    return distance_to_enemy

'''
4. Just do nothing for n actions
'''
def sleep(self, n: int) -> None:
    return None
```
|Описание|функция|используемое количество действий|
|:--:|:--:|:--:|
| 1. Переместить робота на __n__ клеток, в заданном с помощью переменной __dir__ направлении | `bot.move(dir: Directions, n: int) -> None` | __n * 2__ |
| 2. Произвести выстрел | `bot.fire() -> bool` | __2__ |
| 3. Проверить наличие вражеского объекта в заданном с помощью переменной __dir__ направлении | `is_enemy(dir: Directions) -> int`| __1__ |
| 4. Ничего не делать, a.k.a. NOP | `sleep(n: int) -> None` | __n__ |