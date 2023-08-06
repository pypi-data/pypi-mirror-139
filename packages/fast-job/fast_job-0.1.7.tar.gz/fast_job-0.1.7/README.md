### fast_job 
- name = "fast_job"
- description = "Provides scheduling apis and scheduling and task-related services"
- authors = ["Euraxluo <euraxluo@qq.com>"]
- license = "The MIT LICENSE"
- repository = "https://github.com/Euraxluo/fast_job"
- coverage : 74%
- version : 0.1.*

![test-report](https://gitee.com/Euraxluo/images/raw/master/pycharm/MIK-HQpicL.png)

#### install
`pip install fast-job`

#### UseAge

1.wrapper function to build task

```
from fast_job import schedule, task_api_router_init


@schedule.task('task1', summer="test_task_1", tag='test', description="test_task_1")
def test(tag: int):
    print({"msg": "test_task_1", "tag": tag})
    return {"msg": "test_task_1", "tag": tag}


@schedule.task('task2', summer="test_task_2", tag='test', description="test_task_2")
def test2(tag: int):
    print({"msg": "test_task_2", "tag": tag})
    return {"msg": "test_task_2", "tag": tag}


@schedule.task('task3', summer="test_task_3", tag='test', description="test_task_3")
def task3(tag: int):
    raise Exception(str({"msg": "test_task_2", "tag": tag}))


task_api_router = task_api_router_init()
```

2.include in your fastApi

```python
from loguru import logger
from fastapi import FastAPI
from fast_job import schedule, fast_job_api_router
from example.jobs import task_api_router
from example.conftest import rdb as redis

app = FastAPI()


@app.on_event("startup")
async def registry_schedule():
    logger.debug("server start")
    schedule.setup(prefix='test:', logger=logger, redis=redis, distributed=True)
    logger.debug("server started")


@app.on_event("shutdown")  # 关闭调度器
async def shutdown_connect():
    logger.debug("server shutdown")
    schedule.shutdown()


prefix = "/test"
app.include_router(fast_job_api_router, prefix=prefix, tags=["jobs"])  # include router
app.include_router(task_api_router, prefix=prefix, tags=["tasks"])  # include router
```