import logging

from src import settings
from .base_job import BaseJob



class SampleJob(BaseJob):
    def __init__(self):
        super().__init__(name="sample_job",
                         cron_expression=settings.sample_job_frequency, replace_existing=True)
        self.__logger__ = logging.getLogger(__name__)

    def run(self):
        try:
            self.__logger__.info("Starting Sample Job...")
        except Exception:
            self.__logger__.exception("Unable to start Sample sync job, due to ...")
