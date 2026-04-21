import copy
from typing import Callable
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from time import sleep


class Task:
    def __init__(self,task_name,fn : Callable,*args,**kwargs):
        self.task_name = task_name
        self.fn = fn
        self.args = copy.deepcopy(args)
        self.kwargs = copy.deepcopy(kwargs)

    def exe(self):
        self.fn(*self.args,**self.kwargs)



class QueueTaskManager:

    def __init__(self,main_q_maxsize :int  = 0 , thread_pool_executor_max_workers : int = 3 , logger : Callable[[str],None] = print):
        self.manager_thread = None
        self._queue : Queue[Task] = Queue(maxsize=main_q_maxsize)
        self.logger = logger
        self.exc_pool = ThreadPoolExecutor(max_workers=thread_pool_executor_max_workers,thread_name_prefix="QTM_")
        self._is_running = False
        self._manager_thread = None


    def start(self):
        self._manager_thread = Thread(target=self._process,daemon=True,name="QueueTaskManager_main_thread")
        self._manager_thread.start()
        self._is_running = True

    def _process(self):
        while True:
            try:

                if self.exc_pool._work_queue.qsize() > 50 :
                    sleep(0.5)
                    self.logger(f"Waiting for worker queue to be smaller")
                    continue

                t : Task = self._queue.get()
                self.exc_pool.submit(t.exe)
                self.logger(f"Processing {t.task_name}")
                self._queue.task_done()
                self.logger(f"Done with {t.task_name}")
            except Exception as e:
                self.logger(f"Some Error {str(e)}")



    def put(self,task_name : str,fn : Callable , *args , **kwargs):
        t = Task(task_name,fn,*args,**kwargs)
        self._queue.put(t)

    def stop(self):
        self.logger("Initiating graceful shutdown...")

        self._is_running = False

        if self._manager_thread:
            self._manager_thread.join()
            self.logger("Manager thread finished processing queue.")

        self.exc_pool.shutdown(wait=True)
        self.logger("Thread pool shut down. Goodbye!")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_status(self):
        return {
            "in_queue": self._queue.qsize(),
            # נותן הערכה גסה של משימות בביצוע + אלו שמחכות בתור הפנימי של ה-Pool
            "pending": self.exc_pool._work_queue.qsize() ,
            "running": len(self.exc_pool._threads)
        }