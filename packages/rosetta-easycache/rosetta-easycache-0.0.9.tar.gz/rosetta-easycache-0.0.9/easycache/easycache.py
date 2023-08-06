from functools import wraps
import json
import ujson
from bson import ObjectId
from loguru import logger
import asyncio
from typing import List
from .json_encoder import DateEncoder
class EasyCache:
    def __init__(self, redis):
        self.default_redis = redis

    def find(self, *, prefix : str = '', redis=None, key_expire_time : int = 10 * 60,
             key_param_index : int = 1, key_param_name : str = None, opt_param2key_func=None):
        def func_decorator(func):
            @wraps(func)
            async def wrapped_function(*args, **kw):
                param, eil = self.__get_param(key_param_index, key_param_name, *args, **kw)
                if eil:
                    logger.warning(eil)
                    return await self.__run_func(func, *args, **kw)
                if opt_param2key_func:
                    key = opt_param2key_func(param)
                    if not isinstance(key, str):
                        logger.warning(f'opt_param2key_func:{opt_param2key_func.__name__}'
                                       f' should return a primary key of string type'
                                       )
                        return await self.__run_func(func, *args, **kw)
                else:
                    key, eil = self.__default_param2key_func(param, prefix)
                    if eil:
                        logger.warning(eil)
                        return await self.__run_func(func, *args, **kw)
                current_redis = redis if redis else self.default_redis
                response, ok = await self.__find_in_redis(key, current_redis)
                if ok:
                    return ujson.loads(response)
                response = await self.__run_func(func, *args, **kw)
                await self.__add_cache(key, key_expire_time, response, current_redis)
                return response
            return wrapped_function
        return func_decorator


    def delete(self, *, prefix : str = '', redis=None, key_param_index : int = 1,
               key_param_name : str = None, opt_param2keys_func=None):
        def func_decorator(func):
            @wraps(func)
            async def wrapped_function(*args, **kw):
                param, eil = self.__get_param(key_param_index, key_param_name, *args, **kw)
                if eil:
                    logger.warning(eil)
                    return await self.__run_func(func, *args, **kw)
                if opt_param2keys_func:
                    key_list = opt_param2keys_func(param)
                    if not isinstance(key_list, List):
                        logger.warning(f'opt_param2key_func:{opt_param2keys_func.__name__}'
                                       f' should return a primary key of string type'
                                       )
                        return await self.__run_func(func, *args, **kw)
                else:
                    key_list, eil = self.__default_param2keys_func(param, prefix)
                    if eil:
                        logger.warning(eil)
                        return await self.__run_func(func, *args, **kw)
                current_redis = redis if redis else self.default_redis
                await self.__delete_cache(key_list, current_redis)
                res = await self.__run_func(func, *args, **kw)
                await asyncio.sleep(0.01)
                await self.__delete_cache(key_list, current_redis)
                return res
            return wrapped_function
        return func_decorator

    def __get_param(self, key_param_index, key_param_name, *args, **kw):
        if key_param_name:
            if key_param_name in kw:
                return kw[key_param_name], ''
            eil = f'"{key_param_name}" param not fount , not use'
        else:
            key_index = key_param_index
            for tmp in args:
                key_index -= 1
                if not key_index:
                    return tmp, ''
            for key, value in kw.items():
                key_index -= 1
                if not key_index:
                    return value, ''
            eil = f'param index overflow, not use cache'
        return None, eil

    async def __run_func(self, func, *args, **kw):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kw)
        else:
            return func(*args, **kw)

    def __default_param2key_func(self, param, prefix):
        if isinstance(param, ObjectId):
            param = str(param)
        if not isinstance(param, str):
            eil = f'param type is {type(param)} not primary key of string type,' \
                  f' please use opt_param2key_func or change param'
            return None, eil
        cache_key = prefix + ':' + param
        return cache_key, ''

    def __default_param2keys_func(self, param, prefix):
        key_list = []
        if isinstance(param, ObjectId):
            param = str(param)
        if not isinstance(param, str):
            eil = f'param type is {type(param)} not primary key of string type, ' + \
                   'please use opt_param2key_func or change param'
            return None, eil
        cache_key = prefix + ':' + param
        key_list.append(cache_key)
        return key_list, ''

    async def __find_in_redis(self, cache_key, redis):
        response = await redis.get(cache_key)
        if not response:
            logger.warning(f'key: {cache_key} cache not found')
            return response, False
        return response, True

    async def __add_cache(self, cache_key, expire_time, response, redis):
        info = json.dumps(response, cls=DateEncoder, ensure_ascii=False)
        await redis.setex(cache_key, expire_time, info)
        logger.info('Add cache finish!')
        return

    async def __delete_cache(self, key_list, redis):
        if key_list:
            await redis.delete(*key_list)
        logger.info('Delete cache finish!')
        return
