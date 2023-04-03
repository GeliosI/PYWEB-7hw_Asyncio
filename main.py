import asyncio
import aiohttp

from api import get_people, paste_to_db


async def main():
    async with aiohttp.ClientSession() as client_session:
        coros = [get_people(i, client_session) for i in range(1, 83)]
        results = await asyncio.gather(*coros)

    asyncio.create_task(paste_to_db(people_list=results))

    all_tasks = asyncio.all_tasks()
    all_tasks = all_tasks - {asyncio.current_task()}

    await asyncio.gather(*all_tasks)


asyncio.run(main())
