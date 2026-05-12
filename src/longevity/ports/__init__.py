# longevity.ports
"""Port interfaces (Protocols) defining the hexagonal architecture boundaries."""
from longevity.ports.clock import Clock
from longevity.ports.fetcher import LongevityHtmlFetcher
from longevity.ports.parser import LongevityHtmlParser

__all__ = ["Clock", "LongevityHtmlFetcher", "LongevityHtmlParser"]
