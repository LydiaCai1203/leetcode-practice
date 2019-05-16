## 学习笔记之：Logging, Flask, and Gunicorn

#### 问题描述：
> 通过gunicorn启动flask脚本文件的时候，发现使用flask自带的app.logger无法打印日志到终端上面
> 当然了，print也是看不见的了。
> 如果不通过gunicorn，而是直接启动flask脚本文件的时候会发现，使用app.logger打印的日志是可以显示在终端上的
>> 当直接运行脚本的时候，模块名字就等于__main__
>> 通过gunicorn启动flask脚本的时候，模块名字不等于__main__


#### 问题分析：
##### python的logging模块中的：logger,logger.handler分别是什么东西
> logging由四个部分组成分别是
>> 1. logger：提供了应用程序可以直接使用的接口
>> 2. handler：将logger创建的日志发送到合适的目标输出
>> 3. filters：提供一个精度更加细致的日志记录是否输出控制
>> 4. formatters：控制日志记录输出的格式
                                                   
##### maybe 你还需要知道使用logging的步骤
> 1. 创建一个logger对象
> 2. 设置logger对象的日志级别(`logging.DEBUG`,`logging.INFO`, `logging.WARNING`, 'logging.ERROR'等等)
> 3. 创建一个handler,你可以将多个handler绑定到同一个logger上
> 4. 设置handler的日志级别
> 5. 设置日志格式
> 6. 将handler对象绑定到logger对象上面

##### flask, gunicorn层面上的logger
> 1. app.logger的预设设置会将log信息发布在stdout上
> 2. Gunicorn will not catch errors from the app into it's error log - instead, they go to stdout/stderr.

#### 总结：
> 1. github上面gunicorn的issuse中，已经提到，这其实是gunicorn的一个bug，
> 2. 只有数据是流向gunicorn.error.log的日志信息我们才能看得见，但是实际上flask.app.handler是流向的gunicorn进程的标准输入输出流中，所以我们看不到数据的显示
> 3. 解决办法就是将flask.app.logger的handler流引向gunicorn的error.log中，这样才能看得见信息


#### 解决方法-code：
```python 
import logging
from flask import Flask, jsonify

app = Flask(__name__)

if __name__ != ‘__main__’:
    gunicorn_logger = logging.getLogger(‘gunicorn.error’)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route(‘/’)
def default_route():
    “””Default route”””
    app.logger.debug(‘this is a DEBUG message’)
    app.logger.info(‘this is an INFO message’)
    app.logger.warning(‘this is a WARNING message’)
    app.logger.error(‘this is an ERROR message’)
    app.logger.critical(‘this is a CRITICAL message’)
    return jsonify(‘hello world’)

if __name__ == ‘__main__’:
    app.run(host=’0.0.0.0', port=8000, debug=True)
```

#### 代码解析：
> `gunicorn_logger = logging.getLogger(‘gunicorn.error’)`获得gunicorn的logger
> `app.logger.handlers = gunicorn_logger.handlers` flask.app的handler引用只想gunicorn.logger的handler，使其只想同一个stderr/stdin/stdout
> `app.logger.setLevel(gunicorn_logger.level)` 将flask.app的logger级别的空值设成能从gunicorn直接设置的
>  直接在启动命令上使用`gunicorn --workers=2 --bind=0.0.0.0:8000 --log-level=debug app:app`就可以打印出debug和info的日志信息了。


##### 原来这是gunicorn的一个bug... 显示不出来是因为app.logger默认的handler是将日志信息定向到标准输出流中，所以直接执行flask-server.py文件的时候是可以在console看见日志信息的，使用gunicorn托管了以后，只有将日志信息定向到gunicorn errorlog中才能看得见。 所以才要拿到getLogger('gunicorn.error').handler，再扩展到app.logger.handlers上面.....


#### 相关的链接推荐：
[想了解原理-必看2](https://github.com/benoitc/gunicorn/issues/1124)  </br>
[想了解原理-必看1](https://itweb.me/post/blog/2016-03-31-python-logging)   </br>
[只想解决问题看这个](https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f)   </br>
