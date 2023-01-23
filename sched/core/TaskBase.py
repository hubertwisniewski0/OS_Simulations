from utils.Serializable import Serializable


class TaskBase(Serializable):
    """
    Task base class (used for simulation input data generation)
    """
    def __init__(self, come_time: int, duration: int):
        """
        :param come_time: time when the task becomes available to be run
        :param duration: time that the task takes to run
        """
        assert come_time >= 0
        assert duration > 0

        self.come_time = come_time
        self.duration = duration

    def serialize(self):
        return {
            "come_time": self.come_time,
            "duration": self.duration
        }