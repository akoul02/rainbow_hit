from bot import Bot

def run_user(bot: Bot):
    bot.step(5)
    bot.step(1)
    bot.step(3)

def run_enemy(bot: Bot):
    bot.step(7)
    bot.step(5)
    bot.step(3)
    # bot.step(4)

    # if bot.x > 10:
    #     if bot.x > 10:
    #         bot.step(1337)