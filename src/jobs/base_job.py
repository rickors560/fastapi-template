import abc

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger


class BaseJob(abc.ABC):

    def __init__(self, name: str, cron_expression: str, replace_existing: bool = True):
        self.__name__ = name
        self.__cron_expression__ = cron_expression
        self.__replace_existing__ = replace_existing

    @abc.abstractmethod
    def run(self):
        """Run the job."""
        pass

    def register_job(self, scheduler:BaseScheduler):
        trigger = CronTrigger.from_crontab(self.__cron_expression__)
        scheduler.add_job(self.run, trigger, id=self.__name__, replace_existing=self.__replace_existing__)
