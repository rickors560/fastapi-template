import asyncio

from .pollers import SampleEventPoller
from .processor import SampleEventProcessor

async def register_event_pollers():
    event_processor = SampleEventProcessor()
    sqs_poller = SampleEventPoller(event_processor)
    await sqs_poller.poll_messages()
