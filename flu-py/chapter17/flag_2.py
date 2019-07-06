"""
3个线程和5个线程的差别还是很明显的，但是10个线程和20个线程的效果就已经不明显了，是差不多的速度
"""
import time

from concurrent import futures
import requests


def download_one(i):
    print('current thread is:{}'.format(i))
    resp = requests.get('https://www.baidu.com')
    return resp.content


def download_many():
    with futures.ThreadPoolExecutor(5) as executor:                    # 指定threadpool里面最多有几个thread
        res = executor.map(download_one, [i for i in range(20)])
    return res


if __name__ == '__main__':
    now = time.time()
    res_gen = download_many()
    
    for res in res_gen:
        # print(res)
        pass
    
    print(time.time() - now)