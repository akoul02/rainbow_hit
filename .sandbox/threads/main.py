from threading import Barrier, Thread, Lock
from playerCode import *
from bot import Bot
from executor import Executor

def main():
    playerLock = Lock()
    enemyLock = Lock()
    executor1 = Executor(0, 'player', playerLock, runUser)
    executor2 = Executor(0, 'enemy', enemyLock, runEnemy)

    threads = []

    threads.append(Thread(target=executor1.init))
    threads[-1].start()

    threads.append(Thread(target=executor2.init))
    threads[-1].start()


    for step in range(0, 8):
        playerLock.release()
        enemyLock.release()

if __name__ == "__main__":
    main()