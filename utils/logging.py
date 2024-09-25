import collections
import time
import datetime

import torch



class SmoothedValue:
    def __init__(self, window_size=20, fmt=None):
        if fmt is None:
            fmt = "{median:.4f} ({global_avg:.4f})"
        self.fmt = fmt
        self.deque = collections.deque(maxlen=window_size)
        
        self.total = 0.0
        self.count = 0

    def update(self, value, n=1):
        self.deque.append(value)
        self.count += n
        self.total += value * n

    @property
    def median(self):
        d = torch.tensor(list(self.deque))
        return d.median().item()
    @property
    def avg(self):
        d = torch.tensor(list(self.deque))
        return d.mean().item()
    @property
    def global_avg(self):
        return self.total / self.count
    @property
    def max(self):
        return max(self.deque)
    @property
    def value(self):
        return self.deque[-1]

    def __str__(self):
        return self.fmt.format(
                median=self.median,
                avg=self.avg,
                global_avg=self.global_avg,
                max_ele=self.max,
                value=self.value,
                )


class Nexus:
    def __init__(self, delimiter='\t'):
        self.meters = collections.defaultdict(SmoothedValue)
        
        self.delimiter = delimiter

    def add_meter(self, name, meter):
        self.meters[name] = meter

    def update(self, **kwargs):
        for name, v in kwargs.items():
            if isinstance(v, torch.Tensor):
                v = v.item()
            assert isinstance(v, (float, int))
            self.meters[name].update(v)

    def __getattr__(self, attr):
        if attr in self.meters:
            return self.meters[attr]
        if attr in self.__dict__:
            return self.__dict__[attr]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")

    def __str__(self):
        metrics_str = []
        for name, meter in self.meters.items():
            metrics_str.append(f"{name}: {str(meter)}")
        return self.delimiter.join(metrics_str)

    def log_and_iterate(self, dataloader, print_freq, header=None):
        i = 0
        if not header:
            header = ""
        space_fmt = ":" + str(len(str(len(dataloader)))) + "d"
        MB = 1024.0 * 1024.0

        start = time.time()
        end = time.time()
        date_time = SmoothedValue(fmt="{avg:.4f}")
        iter_time = SmoothedValue(fmt="{avg:.4f}")

        log_msg = [
                header,
                "[{iteration_index" + space_fmt + "}/{num_batches}]",
                "eta: {eta}",
                "{meters}",
                "time: {time}",
                "data: {data}",
                "max mem: {memory:.0f}",
                ]
        if not torch.cuda.is_available():
            log_msg.pop()
        log_msg = self.delimiter.join(log_msg)

        for batch in dataloader:
            data_time.update(time.time() - end)
            yield batch
            iter_time.update(time.time() - end)
            if i % print_freq == 0:
                eta_seconds = iter_time.global_avg * (len(dataloader) - i)
                eta_string = str(datatime.timedelta(seconds=int(eta_seconds)))
                log_msg_format = {
                        "iteration_index": i,
                        "num_batches": len(dataloader),
                        "eta": eta_string,
                        "meters": str(self),
                        "time": str(iter_time),
                        "data": str(data_time),
                        "memory": torch.cuda.max_memory_allocated() / MB if torch.cuda.is_available() else None,
                        }
                if not torch.cuda.is_available():
                    log_msg_format.pop("memory")
                print(log_msg.format(**log_msg_format))

            i += 1
            end = time.time()

        total_time = time.time() - start
        total_time_str = str(datatime.timedelta(seconds=int(total_time)))
        print(f"{header} Total time: {total_time_str}")

