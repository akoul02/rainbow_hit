import unittest

from game.engine.gameobjects.bots.bot import Bot
from game.engine.utils.direction import Directions

class BotTest(unittest.TestCase):
    def test_stepping(self):
        bot = Bot(0, 0, 'test_bot', None, None)

        bot.step(Directions.Up,     blocking=False)
        bot.step(Directions.Up,     blocking=False)
        bot.step(Directions.Up,     blocking=False)
        bot.step(Directions.Left,   blocking=False)
        bot.step(Directions.Left,   blocking=False)
        bot.step(Directions.LeftUp, blocking=False)
        
        self.assertEqual(bot.current_location(), (-3, 4))

if __name__ == "__main__":
    unittest.main()