import bencher as bch

from phase_change_mug.record_mug import mug_temps


bench_run = bch.BenchRunner()

bench_run.add_bench(mug_temps)

# bench_run.run(level=-1, show=True)
