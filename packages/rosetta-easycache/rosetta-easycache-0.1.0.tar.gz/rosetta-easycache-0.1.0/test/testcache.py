import asyncio
from loguru import logger
from easycache import easycache

cache1 = easycache.bind_redis('127.0.0.1', 6379)

@cache1.find(prefix='term', key_param_index=1)
async def ddd1(terminology_id):
    logger.info('read in db')
    await asyncio.sleep(3)
    return "ddd1 running"

def mulid(dir):
    return dir['list']

@cache1.delete(prefix='term', key_param_index=5)
async def ddd2(terminology_id):

    logger.info('funcing')
    await asyncio.sleep(1)
    return "ddd2 running"

@cache1.delete(prefix='term', key_param_index=1, get_multiple_key_func=mulid)
async def ddd3(tdis):
    logger.info('ddd3')
    await asyncio.sleep(1)
    return 'ddd3 running'

async def main():
    task_list = []
    task_list.append(asyncio.create_task(ddd1(1)))
    task_list.append(asyncio.create_task(ddd1('bbb')))
    task_list.append(asyncio.create_task(ddd1('ccc')))
    result = await asyncio.gather(*task_list)
    tmp = {'list':['aaa', 'bbb', 'ccc']}
    await asyncio.gather(asyncio.create_task(ddd3(tmp)))
    return result

result = asyncio.run(main())
print(result)