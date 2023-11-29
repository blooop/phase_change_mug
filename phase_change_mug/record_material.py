import bencher as bch
from enum import auto
from strenum import StrEnum
import pandas as pd
from phase_change_mug.temperature_recorder import TemperatureRecorderBase

# from phase_change_mug.record_material import Su

time_res = 1.0
duration = 180.0


# soy_wax = auto()
# cocunut_wax=auto()
class Substance(StrEnum):
    bees_wax = auto()
    soy_wax = auto()
    cocunut_wax = auto()


class TemperatureRecorderSubstance(TemperatureRecorderBase):
    time = bch.FloatSweep(
        default=0, bounds=[0, duration], samples=int(duration) + 1, units="minutes"
    )

    substance = bch.EnumSweep(Substance, units="")

    def __call__(self, **kwargs):
        df = pd.read_csv("cocuno.csv")
        # df.set_index("time",inplace=True)
        # print(df)
        tm = kwargs["time"]
        dat = df.loc[df["time"] == tm]["temperature"]
        self.temperature = dat.values[0]
        self.temperature = 100.0

        # print(self.temperature)

        # return dict(temperature=dat)


def material_temps(
    run_cfg: bch.BenchRunCfg = bch.BenchRunCfg(), report: bch.BenchReport = bch.BenchReport()
):
    run_cfg.use_sample_cache = True
    run_cfg.only_hash_tag = True
    run_cfg.auto_plot = False
    run_cfg.run_tag = "11-9-23-v1"
    # run_cfg.overwrite_sample_cache=True
    bench = bch.Bench(
        "substance_cooling_curve", TemperatureRecorderSubstance(), run_cfg=run_cfg, report=report
    )

    res = bench.plot_sweep(
        "Material Temperature vs Time",
        input_vars=[
            TemperatureRecorderSubstance.param.time,
            TemperatureRecorderSubstance.param.substance,
        ],
        result_vars=[TemperatureRecorderSubstance.param.temperature],
        const_vars=TemperatureRecorderSubstance.get_input_defaults(),
    )

    # df =res.get_dataframe()
    # print(df)
    # df.to_csv("cocuno.csv")

    bench.report.append_tab(res.summarise_sweep())
    # bench.report.append(res.to_curve().overlay().opts(width=500, height=500))
    # bench.report.append(res.to_hv_dataset().to(hv.Table), "Temperature vs Time per mug")
    return bench


if __name__ == "__main__":
    material_temps().show()
