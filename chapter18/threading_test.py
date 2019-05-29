"""
    1. 如果设置了daemon=True，join()生效，主线程等待3s以后结束执行，精灵线程也跟着死亡
    2. 如果设置了daemon=Fasle, join()依旧有效，只不过是主线程等待3秒以后结束执行，其它线程均自己执行完自行了断
    3. 可见join()的作用就是为了阻塞主线程用的
    4. 如果join()里面啥玩意儿都没有，就等待所有的线程都执行完了，主线程才会结束执行
    5. 如果join()不写的话，并不会等待3秒，主线程自己执行完就死掉了，其它线程也是各管各的。
    6. CSDN上面都是写什么垃圾玩意儿。。。
"""
import threading
import time  


def doThreadTest():  
    print('start thread time:', time.strftime('%H:%M:%S'))
    time.sleep(10)  
    print('stop thread time:', time.strftime('%H:%M:%S'))
 

print('start main thread time:', time.strftime('%H:%M:%S'))
threads = []
for i in range(3):
    thread1 = threading.Thread(target = doThreadTest)  
    thread1.setDaemon(False)    # True
    threads.append(thread1)
 
for t in threads:
    t.start() 
 
 
# for t in threads:
#     t.join()

print('stop main thread time:', time.strftime('%H:%M:%S'))
