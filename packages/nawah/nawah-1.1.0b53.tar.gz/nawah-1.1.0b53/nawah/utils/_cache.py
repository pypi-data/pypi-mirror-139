'''Provides `reset_cache`, `reset_expired_cache` Utility'''
import datetime
import logging
from typing import cast

import aioredis

from nawah.classes import AIORedisJSON
from nawah.config import Config

logger = logging.getLogger('nawah')

Config._sys_cache = cast(AIORedisJSON, Config._sys_cache)
Config.cache_expiry = cast(int, Config.cache_expiry)


async def check_cache_connection(attempt: int = 3):
    '''Attempts to read from cache to force re-connection if broken'''

    try:
        await Config._sys_cache.get('__connection')
    except aioredis.exceptions.ConnectionError as e:
        if attempt != 0:
            return await check_cache_connection(attempt=attempt - 1)

        raise e


async def reset_cache_channel(channel: str):
    '''Resets specific cache `channel` by deleting it from active Redis db'''

    try:
        await Config._sys_cache.delete(channel, '.')
    except aioredis.exceptions.ConnectionError:
        logger.error(
            'Connection with Redis server \'%s\' failed. Skipping resetting Cache Channel \'%s\'.',
            Config.cache_server,
            channel,
        )


async def reset_expired_cache():
    '''Deleted expired cache keys from Cache Channel'''

    logger.debug(
        'Executing `reset_expired_cache` on Cache Channels: %s', Config._cache_channels
    )

    cache = Config._sys_cache
    for channel in Config._cache_channels:
        logger.debug('Checking modules for Cache Channel: %s', channel)
        try:
            await check_cache_connection()
            modules_keys = await cache.objkeys(channel, '.')
            if not modules_keys:
                logger.debug('-Skipping Cache Channel due to no modules keys.')
                continue

            for module in modules_keys:
                logger.debug('-Checking methods for module: %s', module)
                methods_keys = await cache.objkeys(channel, f'.{module}')
                if not methods_keys:
                    logger.debug('--Skipping module due to no methods keys.')
                    continue

                for method in methods_keys:
                    logger.debug('--Checking Cache Keys for method: %s', method)
                    cache_keys = await cache.objkeys(channel, f'.{module}.{method}')
                    if not cache_keys:
                        logger.debug('---Skipping method due to no Cache Keys.')
                        continue

                    for cache_key in cache_keys:
                        logger.debug('---Checking Cache Key: %s', cache_key)
                        cache_time = await cache.get(
                            channel,
                            f'.{module}.{method}.{cache_key}.results.args.cache_time',
                        )
                        cache_age = (
                            datetime.datetime.utcnow()
                            - datetime.datetime.fromisoformat(cache_time)
                        ).seconds

                        if cache_age > Config.cache_expiry:
                            logger.debug('----Cache is expired. Deleteing..')
                            await cache.delete(
                                channel, f'.{module}.{method}.{cache_key}'
                            )
                            continue

                        logger.debug('----Skipping Cache as it is still valid.')
        except aioredis.exceptions.ConnectionError:
            logger.error(
                'reset_expired_cache iteration stopped due to connection error.'
            )
