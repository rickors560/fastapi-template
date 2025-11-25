import abc


class BaseEventProcessor(abc.ABC):
    @abc.abstractmethod
    async def process(self, event):
        """
        Process an incoming event.

        Args:
            event: The event to process

        Raises:
            Exception: If processing fails
        """
        pass
