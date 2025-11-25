from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler

from src import settings


def get_scheduler() -> BaseScheduler:
    # Convert async database URL to sync for APScheduler
    # APScheduler's SQLAlchemyJobStore requires a synchronous connection
    sync_database_url = settings.database_url.replace(
        'postgresql+psycopg://',
        'postgresql+psycopg://'
    ).replace(
        'postgresql+asyncpg://',
        'postgresql+psycopg://'
    )

    jobstores = {
        'default': SQLAlchemyJobStore(
            url=sync_database_url,
            tableschema=settings.job_store_database_schema
        )
    }

    job_defaults = {
        'coalesce': True,           # Combine multiple pending executions of the same job into one
        'max_instances': 1,         # Maximum number of concurrently executing instances of a job
        'misfire_grace_time': 60    # Seconds after designated run time that job is still allowed to run
    }

    scheduler = AsyncIOScheduler(
        jobstores=jobstores,
        job_defaults=job_defaults
    )
    return scheduler
