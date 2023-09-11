import bencher as bch

from phase_change_mug.record_mug import mug_temps
from phase_change_mug.record_material import material_temps

bench_run = bch.BenchRunner()

bench_run.add_run(mug_temps)
bench_run.add_run(material_temps)

bench_run.run(level=0,grouped=True)

bench_run.report.show()
