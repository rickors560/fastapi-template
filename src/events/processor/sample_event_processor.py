import logging

from src.events.processor.base_event_processor import BaseEventProcessor


class SampleEventProcessor(BaseEventProcessor):

    def __init__(self):
        self.__logger__ = logging.getLogger(__name__)

    async def process(self, event):
        """
        Process the event. Implement your business logic here.

        Args:
            event: The event to process
        """
        self.__logger__.info(f"Processing event: {event}")
        # Add your event processing logic here
