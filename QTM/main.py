from QueuedTaskManager.QTManager import QueueTaskManager
from random import randint

def my_f(*args,**kwargs):
    print("Inner Print My Func")
    print(args)
    print(kwargs)


with QueueTaskManager() as qtm :
    while True:
        try:
            i = randint(1,20)
            if i >= 10:
                qtm.put(f"my_f task{i}",my_f,i,2,"y",['o',[9,"ppp"]],o=9,t={'y':8})
        except Exception as e:
            print(f"Some Error OUTER{str(e)}")
            exit(3)



