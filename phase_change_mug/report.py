from record_mug import mug_temps
from record_material import mat

import bencher as bch

bench_run = bch.BenchRunner()

bench_run.add_bench(mug_temps)

bench_run.run(level=-1, show=True)