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


def mug_temps(
    run_cfg: bch.BenchRunCfg = bch.BenchRunCfg(), report: bch.BenchReport = bch.BenchReport()
):
    run_cfg.use_sample_cache = True
    run_cfg.use_cache = False
    run_cfg.only_hash_tag = True
    run_cfg.auto_plot = False
    bench = bch.Bench(
        "mug_temps",
        TemperatureRecorder(),
        run_cfg=run_cfg,
        report=report,
        plot_lib=bch.PlotLibrary.none().add(bch.PlotTypes.lineplot_hv),
    )

    preferred_temp = 62

    res = bench.plot_sweep(
        "Tea Temperature vs Time",
        description="""
        ## Question: 
        What material keeps a drink in the mug closest to the ideal temperature for the longest?  I sampled tea at different temperatures and found the hottest I could start drinking comfortably was at 62 degrees C.

        ### Materials:
         - Ceramic: Your bog-standard ceramic mug
         - Glass: A mug made of solid glass with quite thick walls
         - Air: A tall double wall glass mug with air inside the walls. 
         - Air_pavina: A double wall pavina glass mug with air inside the walls. 
         - Bees_wax: A pavina double wall mug filled with bees wax
         - Soy_wax: A pavina double wall mug filled with soy wax         

        ## Procedure:         
        Pour 230ml of boiling water into each mug and record the temperature in 1 minute increments for 30 minutes
        """,
        input_vars=[TemperatureRecorder.param.time, TemperatureRecorder.param.mug],
        result_vars=[TemperatureRecorder.param.temperature],
        const_vars=TemperatureRecorder.get_input_defaults(),
    )

    report.append_tab(res.summarise_sweep())
    report.append(
        res.to_curve().overlay().opts(ylim=(45, 92), shared_axes=False, title=res.title)
        * hv.HLine(preferred_temp).opts(color="r", line_width=1, line_dash="dashed")
    )

    report.append_markdown(
        """## Discussion:
The raw data aboive shows the temperature vs time plots for each mug temperature.  The beeswax mug's cooling curve gradient is shallower than the other materials after around 63 degrees C.  The gradient changes close to the ideal tea temperature and in theory would retain the heat for longer.  The ideal mug would keep the tea as close to the desired temperature for as long as possible.  The plot below shows the absolute difference between the mug temperature and the desired temperature."""
    )

    res.ds["temperature"] = abs(res.ds["temperature"] - preferred_temp)

    report.append(
        res.to_hv_dataset()
        .to(hv.Curve)
        .overlay()
        .opts(shared_axes=False, title="abs(temperature-desired_temperature)")
    )

    report.append_markdown(
        """The best mug would have the smallest area under the curve, these graphs show the area curve for each material"""
    )

    report.append(res.to_hv_dataset().to(hv.Area).layout().opts(shared_axes=False))

    report.append_markdown(
        """The graphs above clearly show the time it takes before the tea becomes drinkable. The double wall air mugs take around 17 to 18 minutes before they are drinkable.  By this time I have usually forgotten that I made a tea. The beeswax and soy wax are drinkable the fastest at 9 minutes, and glass takes up the middle."""
    )

    hvds = hv.Dataset(res.ds.sum(["time"]).squeeze(), kdims="mug", vdims="temperature")
    report.append(
        hvds.to(hv.Bars, kdims=["mug"], vdims="temperature").opts(
            title="Sum of absolute temperature difference vs mug material", shared_axes=False
        )
    )

    report.append_markdown(
        """This graph confirms that bees wax is the best mug material as it has the smallest area under the curve."""
    )

    return bench


if __name__ == "__main__":
    mug_temps().report.show()
    mug_temps().report.save_index()
