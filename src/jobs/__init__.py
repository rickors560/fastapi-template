from .sample_job import SampleJob
from .configure_scheduler import get_scheduler

scheduler = get_scheduler()

sample_job = SampleJob()
sample_job.register_job(scheduler)

