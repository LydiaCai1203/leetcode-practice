## FRAMEWORK

+ *取长补短 聚沙成塔*

### 异常处理

#### insight
```python 
class CustomError(Exception):
    """自定义错误类型
    """  
    def __init__(self, request_handler, message, status, reason):
        super().__init__(message, status)
        self.message = message
        self.status = status
        self.reason = reason

    @property
    def details(self):
        return {
            'status': self.status,
            'reason': self.reason,
            }

    def handle_exce(self):
        request_handler.write(dumps(self.details))


def bugs_hunter(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomError as e:
            print(e.message)
    return wrapper

@bugs_hunter
def my_func():
    raise CustomError('我不想犯错', 200)
```

