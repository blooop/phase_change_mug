import holoviews as hv
import bencher as bch
from phase_change_mug.mqtt_client import TemperatureSensor
import time
from enum import auto
from strenum import StrEnum

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


# run_cfg = bch.BenchRunCfg()
# run_cfg.use_sample_cache = True
# run_cfg.only_hash_tag = True
# run_cfg.repeats = 1
# # run_cfg.overwrite_sample_cache=True
# # run_cfg.use_cache = True
# # run_cfg.over_time=True
# run_cfg.auto_plot = False
# bench = bch.Bench("mug_temps", TemperatureRecorder(), run_cfg=run_cfg)

# res = bench.plot_sweep(
#     "Time vs Temperature",
#     input_vars=[TemperatureRecorder.param.time, TemperatureRecorder.param.mug],
#     result_vars=[TemperatureRecorder.param.temperature],
#     const_vars=TemperatureRecorder.get_input_defaults(),
# )



# bench.append(res.summarise_sweep())
# bench.append(res.to_curve().overlay().opts(width=500, height=500, ylim=(45, 92)))
# bench.append(res.to_hv_dataset().to(hv.Table), "Temperature vs Time per mug")
# # bench.save_index()
# bench.show()
