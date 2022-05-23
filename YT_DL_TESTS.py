
import asyncio, time


async def foo(a):
    asyncio.sleep(2)
    print(a)


def doo(loop):
    for i in range(100):
        loop.run_until_complete(foo(i))

loop = asyncio.new_event_loop()
doo(loop)


loop.close()
