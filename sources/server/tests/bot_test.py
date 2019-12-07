import unittest

import sys, os
sys.path.insert(0, 'C:\\Users\\madrat\\Desktop\\rainbow_hit\\sources\\server\\game\\')

from engine.gameobjects.bots.bot import Bot
from engine.utils.direction import Direction

class BotTest(unittest.TestCase):
    def test_stepping(self):
        bot = Bot(0, 0, 'test_bot', None, None)

        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Left,   blocking=False)
        bot.step(Direction.Left,   blocking=False)
        bot.step(Direction.LeftUp, blocking=False)
        
        self.assertEqual(bot.current_location(), (-3, 4))

if __name__ == "__main__":
    unittest.main()