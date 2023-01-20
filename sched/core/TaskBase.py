from utils.Serializable import Serializable


class TaskBase(Serializable):
    def __init__(self, come_time: int, duration: int):
        assert come_time >= 0
        assert duration > 0

        self.come_time = come_time
        self.duration = duration

    def serialize(self):
        return {
            "come_time": self.come_time,
            "duration": self.duration
        }