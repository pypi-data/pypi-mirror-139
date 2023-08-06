from multiprocessing import get_context, Process, Queue
from typing import Callable, List


class MutiProcessRunner:
    def __init__(self, process_count: int, id_start: int, id_end: int) -> None:
        self.process_count = process_count
        self.id_start = id_start
        self.id_end = id_end
        self.data_per_process = int(
            (self.id_end - self.id_start) / self.process_count)
        self.ctx = get_context("spawn")
        self.queue: Queue = self.ctx.Queue()
        self.processes: List[Process] = []

    def run(self, fn: Callable, *args, **kwargs):
        for i in range(self.process_count):
            p_id_start = self.data_per_process * i + self.id_start
            if i != self.process_count - 1:
                p_id_end = p_id_start + self.data_per_process
            else:
                p_id_end = self.id_end
            p = self.ctx.Process(target=fn,
                                 args=(p_id_start,
                                       p_id_end,
                                       self.queue,
                                       *args), kwargs=kwargs)
            p.start()
            self.processes.append(p)

    def join(self):
        for p in self.processes:
            p.join()

    def terminate(self):
        for p in self.processes:
            p.terminate()

    def kill(self):
        for p in self.processes:
            p.kill()
