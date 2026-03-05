import logging
import asyncio
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_file = os.path.join(BASE_DIR, "errors.log")


logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message):
    logging.error(message)


async def retry(task, retries=3, delay=3):

    for attempt in range(retries):

        try:
            return await task()

        except Exception as e:

            if attempt == retries - 1:
                raise e

            await asyncio.sleep(delay)