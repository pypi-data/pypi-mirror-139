import asyncio
import time

import easycache_V1
import aioredis
from aiodis import aiocache
class RedisDBConfig:
    HOST = '127.0.0.1'
    PORT = 6379
    DBID = 0

async def main():
    task_list = []
    """
    easycache = easycache_V1.EasyCache(redis_pool.pool)
    def p2k(a):
        return a['list']
    @easycache.delete(key_param_name='a', prefix='test', opt_param2keys_func=p2k)
    def ddd1(a):
        print('ddd1 run')

    for i in range(1, 2):
        mp = {'list':['test:1', 'test:2', 'test:3', 'test:4', 'test:5']}
        task_tmp = ddd1(a=mp)
        task_list.append(asyncio.create_task(task_tmp))
    """

    async def process(key_name: str):
        print(key_name + ' running')
        async with aiocache as r:
            await r.delete(key_name, 'redis pool test V1')
        print(key_name + ' have conn')
        await asyncio.sleep(1)
        print(key_name + ' is endding')

    for i in range(1, 10020):
        task_tmp = process(str(i))
        task_list.append(asyncio.create_task(task_tmp))
    result = await asyncio.wait(task_list)
    return result

if __name__ == '__main__':
    start = time.time()
    result = asyncio.run(main())
    print(time.time() - start)