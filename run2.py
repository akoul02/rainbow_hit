import importlib.util
import sys
from sources.api import run

players = []

for i in range(1, 3):
    spec = importlib.util.spec_from_file_location(f'bot{i}', sys.argv[i])
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name] = module
    spec.loader.exec_module(module)
    players.append(module.BotActivity)

run(*players)