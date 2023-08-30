import holoviews as hv
import pandas as pd
import hvplot.pandas  # noqa pylint :ignore
import bencher as bch
from phase_change_mug.publish_args import publish_args

class MugTemp(bch.ParametrizedSweep):
    pass


bench = bch.BenchRunner.from_parametrized_sweep(MugTemp())


df = pd.read_csv("phase_change_mug/data.csv")
ds = hv.Dataset(df)
bench.append_markdown(
    """Table oftime vs temperature for 260g of water and various mug fill materials""",
    "Time vs Temperature",
)
bench.append(ds.to(hv.Table))
bench.append_markdown("""Plot of time vs temperature for 260g of water""", "Time vs Temperature")
cv = df.hvplot.line(x="Time", y=["temp_mug", "temp_bee", "temp_air"], line_width=2, legend="right")
bench.append(cv)

bench.publish(publish_args)
bench.show()
