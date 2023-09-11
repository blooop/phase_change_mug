import holoviews as hv
import bencher as bch
from enum import auto
from strenum import StrEnum

from phase_change_mug.temperature_recorder import TemperatureRecorderBase

time_res = 1.0
duration = 30.0


class MugWallType(StrEnum):
    air = auto()
    air_pavina = auto()
    bees_wax = auto()
    ceramic = auto()
    soy_wax = auto()
    glass = auto()


class TemperatureRecorder(TemperatureRecorderBase):
    time = bch.FloatSweep(
        default=0, bounds=[0, duration], samples=int(duration) + 1, units="minutes"
    )
    mug = bch.EnumSweep(MugWallType, units="")


def mug_temps(run_cfg: bch.BenchRunCfg = bch.BenchRunCfg(),report:bch.BenchReport=bch.BenchReport()):
    run_cfg.use_sample_cache = True
    run_cfg.only_hash_tag = True
    run_cfg.auto_plot = False
    bench = bch.Bench("mug_temps", TemperatureRecorder(), run_cfg=run_cfg,report=report)

    res = bench.plot_sweep(
        "Mug Temperature vs Time",
        input_vars=[TemperatureRecorder.param.time, TemperatureRecorder.param.mug],
        result_vars=[TemperatureRecorder.param.temperature],
        const_vars=TemperatureRecorder.get_input_defaults(),
    )

    bench.report.append(res.summarise_sweep())
    bench.report.append(res.to_curve().overlay().opts(width=500, height=500, ylim=(45, 92)))
    bench.report.append(res.to_hv_dataset().to(hv.Table), "Temperature vs Time per mug")
    # bench.save_index()
    bench.show()


if __name__ == "__main__":
    mug_temps().show()
