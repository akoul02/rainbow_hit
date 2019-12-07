import ctypes 
import threading
import time
from dataclasses import dataclass

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
        target_tid = (tid for tid, tobj in threading._active.items() if tobj is self)

        try:
            target_tid = next(target_tid)
        except StopIteration:
            raise ValueError("Invalid thread object")

        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, ctypes.py_object(exception))
        if ret == 0:
            raise ValueError("Invalid TID")
        elif ret > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")

        return None

    def terminate(self, exception=Exception):
        if not self.killed and self.is_alive():
            self.async_raise(exception)
            self.join()
            self.killed = True

if __name__ == "__main__":
    main()