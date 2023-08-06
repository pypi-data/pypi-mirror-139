import asyncio
import sys
import os

sys.path.insert(1, ".")


from l0n0lutils.async_runner import async_runner


async def task_test():
    await asyncio.sleep(5)
    print("closed")

def on_close():
    print("xxxxxx")

loop = asyncio.get_event_loop()
r = async_runner()
r.on_close_function(on_close)
loop.create_task(task_test())
r.run_forever(loop, True)

