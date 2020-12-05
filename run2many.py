import importlib.util
import sys
from sources.server.game.game_sync import Game
# from dataclasses import dataclass
from pathlib import Path
import sqlite3
import hashlib

players = []
names = []
player_id = []

conn = sqlite3.connect('ranking.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS participants (name text, sha256 blob UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS results(
        player1 int, player2 int, wins_by_1 int, wins_by_2 int, draws int,
        FOREIGN KEY(player1) REFERENCES participants(rowid),
        FOREIGN KEY(player2) REFERENCES participants(rowid)
)''')

for i in range(1, len(sys.argv)):
    spec = importlib.util.spec_from_file_location(f'bot{i}', sys.argv[i])
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name] = module
    spec.loader.exec_module(module)
    players.append(module.BotActivity)
    names.append(Path(sys.argv[i]).stem)
    hasher = hashlib.sha256()
    hasher.update(Path(sys.argv[i]).read_bytes())
    sha = hasher.digest()
    c.execute('select rowid from participants where sha256 = ?', [sha])
    res = c.fetchone()
    if res is None:
        c.execute('insert into participants(name, sha256) values(?,?)',
                  [names[-1], sha])
        res = [c.lastrowid]
    player_id += res

N = len(players)


# @dataclass
# class Result:
#     won1: int = 0
#     draw: int = 0
#     won2: int = 0


# results = {}

for i in range(N):
    for j in range(N):
        c.execute(
            'select rowid, wins_by_1 + draws + wins_by_2 from results '
            'where player1 = ? and player2 = ?', [player_id[i], player_id[j]])
        res = c.fetchone()
        if res is None:
            c.execute(
                'insert into results(player1, player2, \
                    wins_by_1, draws, wins_by_2) values(?,?,0,0,0)',
                [player_id[i], player_id[j]])
            rowid, scores = c.lastrowid, 0
        else:
            rowid, scores = res
        # scores = (res or [0])[0]
        print(names[i], 'vs', names[j], scores)
        for _ in range(scores, 64):
            game = Game(players[i], players[j], [0, 1])
            result = game.run()
            # out = results.setdefault((names[i], names[j]), Result())
            if result.game_won:
                if result.winner.name == 0:
                    col = 'wins_by_1'
                    # out.won1 += 1
                else:
                    col = 'wins_by_2'
                    # out.won2 += 1
            else:
                col = 'draws'
                # out.draw += 1
            c.execute(
                f'update results set {col}={col}+1\
                        where player1 = ? and player2 = ?',
                [player_id[i], player_id[j]])
            conn.commit()
# print(results)
