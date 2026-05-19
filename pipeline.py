
from multiprocessing import Process, Queue


class Pipeline:
    def __init__(self, queue_size=10):
        self.stages = []
        self.queues = []
        self.processes = []
        self.queue_size = queue_size

    def add_stage(self, stage):
        self.stages.append(stage)

    def build(self):
        self.queues = [Queue(maxsize=self.queue_size) for _ in range(len(self.stages)-1)]

    def run(self):
        self.build()

        for i, stage in enumerate(self.stages):
            if i == 0:
                proc = Process(target=stage.run, args=(self.queues[0],))
            elif i == len(self.stages)-1:
                proc = Process(target=stage.run, args=(self.queues[i-1],))
            else:
                proc = Process(target=stage.run, args=(self.queues[i-1], self.queues[i]))
            self.processes.append(proc)

        for p in self.processes:
            p.start()

        for p in self.processes:
            p.join()
