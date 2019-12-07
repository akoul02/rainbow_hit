import ctypes 
import threading
import time

from exceptions import FatalException

class KThread(threading.Thread):
    '''This thread can be killed.

    Attributes
    ----------
    killed : bool
        shows, that thread is killed, or not
    '''
    killed: bool = False

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

    def async_raise(self, exception) -> None:
        desired = (tid for tid, obj in threading._active.items() if obj is self)

        try:
            tid = next(desired)
        except StopIteration:
            raise ValueError("Doesn't found any suitable thread objects!")

        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exception))
        if ret == 0:
            raise ValueError("Invalid TID")
        elif ret > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise FatalException("ctypes pythonapi failed!")

        return None

    def terminate(self, exception=Exception):
        if not self.killed and self.is_alive():
            self.async_raise(exception)
            self.join()
            self.killed = True

if __name__ == "__main__":
    main()