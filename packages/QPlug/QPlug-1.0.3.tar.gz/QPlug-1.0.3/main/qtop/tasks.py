"""Classes to easily implement Qt-friendly computational tasks running in external threads or processes, with a simple API."""

import time
import traceback
import inspect
import logging
from queue import Queue as tQueue
from queue import Empty
from threading import Thread
from multiprocessing import Process, Queue as pQueue

try:
    from qtpy.QtCore import QThread, QTimer, QObject
    def _start_thread(fun, *args, **kwargs):
        """Start a QThread."""
        class MyQThread(QThread):
            def run(self):
                fun(*args, **kwargs)
            def join(self):
                self.wait()
        qthread = MyQThread()
        qthread.start(QThread.LowPriority)
        return qthread
except ImportError:
    def _start_thread(fun, *args, **kwargs):
        """Start a Thread normally."""
        _thread = Thread(target=fun, args=args, kwargs=kwargs)
        _thread.start()
        return _thread

FINISHED = '__END__'
TIMER_MASTER_DELAY = .01

__all__ = [
           'TasksBase',
           'TasksInThread',
           'TasksInProcess',
           'inthread',
           'inprocess',
           ]

class ToInstanciate(object):
    def __init__(self, task_class, *initargs, **initkwargs):
        self.task_class = task_class
        self.initargs = initargs
        self.initkwargs = initkwargs
    
    def instanciate(self):
        return self.task_class(*self.initargs, **self.initkwargs)
        

def worker_loop(task_obj, qin, qout, qout_sync, impatient=False):
    """Worker loop that processes jobs send by the master."""
    if isinstance(task_obj, ToInstanciate):
        task_obj = task_obj.instanciate()
    while True:
        r = qin.get()
        if r == FINISHED:
            qout.put(FINISHED)
            break
        if impatient and not qin.empty():
            continue
        method, args, kwargs, sync = r
        if hasattr(task_obj, method):
            try:
                result = getattr(task_obj, method)(*args, **kwargs)
            except Exception as e:
                msg = traceback.format_exc()
                print("An exception occurred: {0:s}.".format(msg))
                result = e
            kwargs_back = kwargs.copy()
            kwargs_back.update(_result=result)
            if sync:
                q = qout_sync
            else:
                q = qout
            q.put((method, args, kwargs_back))

def master_loop(task_class, qin, qout, results=[], task_obj=None):
    """Master loop that retrieves jobs processed by the worker."""
    if task_obj is None:
        task_obj = task_class
    while True:
        r = qout.get()
        if r == FINISHED:
            break
        method, args, kwargs = r
        results.append((method, args, kwargs))
        done_name = method + '_done'
        if hasattr(task_class, done_name):
            getattr(task_obj, done_name)(*args, **kwargs)
    
def master_iteration(task_class, qin, qout, results=[], task_obj=None):
    """Master loop that retrieves jobs processed by the worker."""
    try:
        r = qout.get_nowait()
    except Empty:
        return
    if r == FINISHED:
        return
    if task_obj is None:
        task_obj = task_class
    method, args, kwargs = r
    results.append((method, args, kwargs))
    done_name = method + '_done'
    if hasattr(task_class, done_name):
        getattr(task_obj, done_name)(*args, **kwargs)

class TasksBase(QObject):
    """Implements a queue containing jobs (Python methods of a base class
    specified in `cls`)."""
    def __init__(self, cls, *initargs, **initkwargs):
        super(TasksBase, self).__init__(initkwargs.pop('parent', None))
        self.results = []
        self.impatient = initkwargs.pop('impatient', None)
        self.use_master_thread = initkwargs.pop('use_master_thread', True)
        self.initargs, self.initkwargs = initargs, initkwargs
        self.task_class = cls
        self.init_queues()
        self.instanciate_task()
        self.start()
        
    def init_queues(self):
        """Initialize the two queues (two directions), named _qin and _qout.
        
        """
        pass
    
    def instanciate_task(self):
        """Instanciate the task self.task_obj.
        
        This object can be a ToInstanciate instance if the task needs
        to be instanciated in a separated thread or process.
        
        """
        pass
    
    def start(self):
        pass
    
    def start_worker(self):
        """Start the worker thread or process."""
        pass
        
    def start_master(self):
        """Start the master thread, used to retrieve the results."""
        pass
        
    def join(self):
        """Stop the worker and master as soon as all tasks have finished."""
        pass
    
    def get_result(self, index=-1):
        result = self.results[index][2]['_result']
        if isinstance(result, Exception):
            raise result
        return result
    
    def _start(self):
        """Worker main function."""
        worker_loop(self.task_obj, self._qin, self._qout, self._qout_sync,
            self.impatient)

    def _retrieve(self):
        """Master main function."""
        if self.use_master_thread:
            master_loop(self.task_class, self._qin, self._qout, self.results)
        else:
            master_iteration(self.task_class, self._qin, self._qout, self.results)
        
    def _put(self, fun, *arg, **kwargs):
        """Put a function to process on the queue."""
        sync = kwargs.pop('_sync', None)
        self._qin.put((fun, arg, kwargs, sync))
        if sync:
            return self._qout_sync.get()
        
    def __getattr__(self, name):
        if hasattr(self.task_obj, name):
            v = getattr(self.task_obj, name)
            if inspect.ismethod(v):
                return lambda *args, **kwargs: self._put(name, *args, **kwargs)
            else:
                return v
        raise AttributeError("'{0:s}' is not an attribute of '{1:s}'".format(
            name, self))

class TasksInThread(TasksBase):
    """Implements a queue containing jobs (Python methods of a base class
    specified in `cls`)."""
    def init_queues(self):
        self._qin = tQueue()
        self._qout = tQueue()
        self._qout_sync = tQueue()
    
    def instanciate_task(self):
        self.task_obj = self.task_class(*self.initargs, **self.initkwargs)
        
    def _retrieve(self):
        """Master main function."""
        if self.use_master_thread:
            master_loop(self.task_class, self._qin, self._qout, self.results,
                task_obj=self.task_obj)
        else:
            master_iteration(self.task_class, self._qin, self._qout, 
                self.results, task_obj=self.task_obj)
        
    def start(self):
        self.start_worker()
        self.start_master()
    
    def start_worker(self):
        """Start the worker thread or process."""
        self._thread_worker = _start_thread(self._start)
        
    def start_master(self):
        """Start the master thread, used to retrieve the results."""
        if self.use_master_thread:
            self._thread_master = _start_thread(self._retrieve)
        else:
            self._timer_master = QTimer(self)
            self._timer_master.setInterval(int(TIMER_MASTER_DELAY * 1000))
            self._timer_master.timeout.connect(self._retrieve)
            self._timer_master.start()
        
    def join(self):
        """Stop the worker and master as soon as all tasks have finished."""
        self._qin.put(FINISHED)
        self._thread_worker.join()
        if self.use_master_thread:
            self._thread_master.join()
        else:
            self._timer_master.stop()
                
    def __getattr__(self, name):
        task_obj = self.task_obj
        if hasattr(task_obj, name):
            v = getattr(task_obj, name)
            if inspect.ismethod(v):
                return lambda *args, **kwargs: self._put(name, *args, **kwargs)
            else:
                return v
        else:
            result = self._put('__getattribute__', name, _sync=True)
            return result[2]['_result']
            
def inthread(cls):
    class MyTasksInThread(TasksInThread):
        def __init__(self, *initargs, **initkwargs):
            super(MyTasksInThread, self).__init__(cls, *initargs, **initkwargs)
    return MyTasksInThread

class TasksInProcess(TasksBase):
    """Implements a queue containing jobs (Python methods of a base class
    specified in `cls`)."""
    def init_queues(self):
        self._qin = pQueue()
        self._qout = pQueue()
        self._qout_sync = pQueue()
        
    def instanciate_task(self):
        self.task_obj = ToInstanciate(self.task_class, *self.initargs, **self.initkwargs)
        self.task_obj_master = self.task_class(*self.initargs,
            **self.initkwargs)
    
    def start(self):
        self.start_worker()
        self.start_master()
    
    def start_worker(self):
        """Start the worker thread or process."""
        self._process_worker = Process(target=worker_loop, args=(self.task_obj, 
            self._qin, self._qout, self._qout_sync, self.impatient))
        self._process_worker.start()
    
    def _retrieve(self):
        """Master main function."""
        if self.use_master_thread:
            master_loop(self.task_class, self._qin, self._qout, self.results,
                task_obj=self.task_obj_master)
        else:
            master_iteration(self.task_class, self._qin, self._qout, self.results,
                task_obj=self.task_obj_master)
            
    def start_master(self):
        """Start the master thread, used to retrieve the results."""
        if self.use_master_thread:
            self._thread_master = _start_thread(self._retrieve)
        else:
            self._timer_master = QTimer(self)
            self._timer_master.setInterval(int(TIMER_MASTER_DELAY * 1000))
            self._timer_master.timeout.connect(self._retrieve)
            self._timer_master.start()
        
    def join(self):
        """Stop the worker and master as soon as all tasks have finished."""
        self._qin.put(FINISHED)
        if self.use_master_thread:
            self._thread_master.join()
        else:
            self._timer_master.stop()
        self._process_worker.terminate()
        self._process_worker.join()
    
    def terminate(self):
        self._process_worker.terminate()
        self._process_worker.join()
        self._qout.put(FINISHED)
        if self.use_master_thread:
            self._thread_master.join()
        else:
            self._timer_master.stop()
    
    def __getattr__(self, name):
        task_obj = self.task_obj_master
        if hasattr(task_obj, name):
            v = getattr(task_obj, name)
            if inspect.ismethod(v):
                return lambda *args, **kwargs: self._put(name, *args, **kwargs)
            else:
                return v
        else:
            result = self._put('__getattribute__', name, _sync=True)
            return result[2]['_result']

def inprocess(cls):
    class MyTasksInProcess(TasksInProcess):
        def __init__(self, *initargs, **initkwargs):
            super(MyTasksInProcess, self).__init__(cls, *initargs, **initkwargs)
    return MyTasksInProcess