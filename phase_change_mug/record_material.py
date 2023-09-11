import holoviews as hv
import bencher as bch
from enum import auto
from strenum import StrEnum

from phase_change_mug.temperature_recorder import TemperatureRecorderBase

time_res = 1.0
duration = 180.0


class Substance(StrEnum):
    bees_wax = auto()
    # soy_wax = auto()
    # cocunut_wax=auto()


class TemperatureRecorderSubstance(TemperatureRecorderBase):
    time = bch.FloatSweep(
        default=0, bounds=[0, duration], samples=int(duration) + 1, units="minutes"
    )

    substance = bch.EnumSweep(Substance, units="")


def material_temps(run_cfg: bch.BenchRunCfg = bch.BenchRunCfg()):
    run_cfg.use_sample_cache = True
    run_cfg.only_hash_tag = True
    run_cfg.auto_plot = False
    run_cfg.run_tag = "10-9-23-v1"
    # run_cfg.overwrite_sample_cache=True
    bench = bch.Bench("substance_cooling_curve", TemperatureRecorderSubstance(), run_cfg=run_cfg)

    res = bench.plot_sweep(
        "Time vs Temperature",
        input_vars=[
            TemperatureRecorderSubstance.param.time,
            TemperatureRecorderSubstance.param.substance,
        ],
        result_vars=[TemperatureRecorderSubstance.param.temperature],
        const_vars=TemperatureRecorderSubstance.get_input_defaults(),
    )

    bench.report.append(res.summarise_sweep())
    bench.report.append(res.to_curve().overlay().opts(width=500, height=500))
    bench.report.append(res.to_hv_dataset().to(hv.Table), "Temperature vs Time per mug")
    return bench


if __name__ == "__main__":
    material_temps().show()
