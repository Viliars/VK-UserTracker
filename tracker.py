from utils import load_users_info, chunks
from config import config
from typing import List, Dict
from loguru import logger
import asyncio
import sys
from datetime import datetime

logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


async def main():
    logger.info("Start tracker")
    with open(str(config.ids)) as fin:
        users_ids: List[int] = [int(ID.strip()) for ID in fin]

    logger.info(f"Number of users = {len(users_ids)}")

    fields: List[str] = ["status"]

    parts_ids: List[List[str]] = [list(map(str, chunk)) for chunk in chunks(users_ids, 750)]

    dt = datetime.now()
    path = config.output_path / dt.strftime("%Y_%m_%d_%H_%m_%S")

    for i, chunk in enumerate(chunks(parts_ids, 100)):
        logger.info(f"--- PART #{i+1} ---")

        tasks: List = [load_users_info(part, fields) for part in chunk]

        result: List[List[Dict]] = await asyncio.gather(*tasks)

        users_info = sum(result, start=[])

        # фильтруем живых пользователей
        alive: List[Dict] = []
        banned: List[Dict] = []
        deleted: List[Dict] = []
        for user_info in users_info:
            if user_info['deactivated'] is None:
                alive.append(user_info)
            elif user_info['deactivated'] == 'banned':
                banned.append(user_info)
            elif user_info['deactivated'] == 'deleted':
                deleted.append(user_info)

        logger.info(f"len(alive) = {len(alive)}")
        logger.info(f"len(banned) = {len(banned)}")
        logger.info(f"len(deleted) = {len(deleted)}")

        # Находим тех, кто слушает музыку
        music: List[Dict] = []
        for user_info in alive:
            if user_info['status_audio'] is not None:
                music.append(user_info)

        logger.info(f"len(music) = {len(music)}")

        with open(str(path), "a") as fout:
            for user_info in music:
                print(user_info['id'], file=fout)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
