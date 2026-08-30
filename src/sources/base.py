from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def extract(self):
        """Extract raw data from the source."""
        pass

    @abstractmethod
    def transform(self, data):
        """Transform raw data into a standard structure."""
        pass
