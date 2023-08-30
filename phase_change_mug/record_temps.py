import holoviews as hv
import pandas as pd
import hvplot.pandas  # noqa pylint :ignore
import bencher as bch
from phase_change_mug.publish_args import publish_args
from mqtt_client import TemperatureSensor
import time
from enum import auto
from strenum import StrEnum

time_res = 1.
duration = 30.



class MugWallType(StrEnum):
    ceramic = auto()
    soy_wax = auto()
    glass=auto()
    # air = auto()
    # bees_wax =auto()
    # cocunut_wax = auto()

class TemperatureRecorder(bch.ParametrizedSweep):

    time = bch.FloatSweep(default=0,bounds=[0,duration],samples=int(duration)+1,units="minutes")

    temperature = bch.ResultVar("deg C")

    mug = bch.EnumSweep(MugWallType)

    def __init__(self, **params):
        super().__init__(**params)
        self.temp_sense = TemperatureSensor()
        self.temp_sense.get_data()
        self.start_time = time.time()

    def __call__(self,**kwargs):
        self.update_params_from_kwargs(**kwargs)
        while True:            
            cur_time = (time.time()- self.start_time)/60.
            print(f"waiting until time {self.time} > current time {cur_time}")
            if  self.time < cur_time  :
                break
            time.sleep(1)
           
        self.temp_sense.get_data()
        self.temperature = self.temp_sense.temperature
        return self.get_results_values_as_dict()



run_cfg = bch.BenchRunCfg()
run_cfg.use_sample_cache=True
run_cfg.only_hash_tag=True
# run_cfg.use_cache = True
# run_cfg.over_time=True
bench = bch.Bench("mug_temps",TemperatureRecorder(),run_cfg=run_cfg)

res =bench.plot_sweep("Time vs Temperature",input_vars=[TemperatureRecorder.param.time,TemperatureRecorder.                                                  param.mug],result_vars=[TemperatureRecorder.param.temperature],
const_vars=TemperatureRecorder.get_input_defaults())
# const_vars=TemperatureRecorder.get_input_defaults([TemperatureRecorder.param.mug.with_const(MugWallType.glass)]))

# bench.append(res.ds.to_dataframe().hvplot)
bench.show()

