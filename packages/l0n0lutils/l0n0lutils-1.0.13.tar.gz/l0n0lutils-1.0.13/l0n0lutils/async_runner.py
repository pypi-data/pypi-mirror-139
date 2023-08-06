from typing import Awaitable, Callable
import asyncio
import logging
import sys

if sys.platform == "linux":
    try:
        import uvloop
        uvloop.install()
    except:
        pass


class async_runner:
    on_closes = []

    def exeute_on_close(self):
        try:
            for fn in self.on_closes:
                try:
                    fn()
                except KeyboardInterrupt:
                    continue
                except BaseException as e:
                    logging.exception(e.with_traceback(None), stack_info=True)
        except:
            pass

    def on_close_function(self, fn: Callable):
        self.on_closes.append(fn)
        return fn

    def run(self, loop: asyncio.BaseEventLoop = asyncio.get_event_loop(), main_task: Awaitable = None):
        try:
            if main_task:
                loop.run_until_complete(main_task)
            else:
                loop.run_forever()
        except KeyboardInterrupt:
            self.exeute_on_close()
            for task in asyncio.all_tasks(loop):
                task.cancel()
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
        except BaseException as e:
            logging.exception(e.with_traceback(None), stack_info=True)
            return


g_async_runner = async_runner()


def on_close_function(fn: Callable):
    return g_async_runner.on_close_function(fn)


def run(loop: asyncio.BaseEventLoop = asyncio.get_event_loop(), main_task: Awaitable = None):
    g_async_runner.run(loop, main_task)
