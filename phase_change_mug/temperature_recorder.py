import bencher as bch
from phase_change_mug.mqtt_client import TemperatureSensor
import time

time_res = 1.0
duration = 30.0


class TemperatureRecorderBase(bch.ParametrizedSweep):
    time = bch.FloatSweep(
        default=0, bounds=[0, duration], samples=int(duration) + 1, units="minutes"
    )

    temperature = bch.ResultVar("deg C")

    def __init__(self, **params):
        super().__init__(**params)
        self.temp_sense = TemperatureSensor()
        # self.temp_sense.get_data()
        self.start_time = time.time()

    def __call__(self, **kwargs):
        self.update_params_from_kwargs(**kwargs)
        while True:
            cur_time = (time.time() - self.start_time) / 60.0
            print(f"waiting until time {self.time} > current time {cur_time}")
            if self.time < cur_time:
                break
            time.sleep(1)

        self.temp_sense.get_data()
        self.temperature = self.temp_sense.temperature
        return self.get_results_values_as_dict()

    def poll(self):
        while True:
            # self.__call__()
            time.sleep(10)


if __name__ == "__main__":
    TemperatureRecorderBase().poll()
