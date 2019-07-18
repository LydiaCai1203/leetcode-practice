"""
可以模仿扔任务，来看任务堆积的问题
"""

from celery import Celery

app = Celery('hello', broker='redis://:@127.0.0.1/14')

@app.task
def hello():
    return 'hello world'