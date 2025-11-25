import asyncio
import logging
from typing import Dict, List

from src import settings
from src.events.processor import BaseEventProcessor


class SampleEventPoller:
    def __init__(self, event_processor: BaseEventProcessor):
        self.__backoff_initial_in_seconds__ = settings.sample_event_polling_backoff_initial_in_seconds
        self.__backoff_max_in_seconds__ = settings.sample_event_polling_backoff_max_in_seconds

        self.__event_processor__ = event_processor
        self.__logger__ = logging.getLogger(__name__)
        self.__is_running__ = False

    async def poll_messages(self) -> None:
        self.__is_running__ = True
        backoff = self.__backoff_initial_in_seconds__

        self.__logger__.info("Event poller started")

        try:
            while self.__is_running__:
                try:
                    msgs = await asyncio.to_thread(self.__receive__)
                    if not msgs:
                        await asyncio.sleep(backoff)
                        backoff = self.__backoff_initial_in_seconds__
                        continue

                    for msg in msgs:
                        try:
                            await self.__event_processor__.process(msg)
                            self.__logger__.info("Processed message successfully")
                        except Exception as ex:
                            self.__logger__.exception("Error processing message: %s", ex)

                    backoff = self.__backoff_initial_in_seconds__

                except asyncio.CancelledError:
                    self.__logger__.info("Polling cancelled, shutting down gracefully")
                    raise
                except Exception:
                    self.__logger__.exception("Top-level polling error; backing off %.1fs", backoff)
                    await asyncio.sleep(backoff)
                    backoff = min(backoff * 2, self.__backoff_max_in_seconds__)
        finally:
            self.__is_running__ = False
            self.__logger__.info("Event poller stopped")

    def __receive__(self) -> List[Dict]:
        """
        Override this method to implement actual message receiving logic.
        This is a synchronous method that will be run in a thread pool.
        """
        return []

    def stop(self):
        """Signal the poller to stop gracefully"""
        self.__is_running__ = False
