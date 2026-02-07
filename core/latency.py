import time
import random


class LatencySimulator:
    """
    Simulates latency at different stages of a decision pipeline.
    """

    def __init__(
        self,
        ingestion_ms=(2, 5),
        feature_ms=(5, 10),
        inference_ms=(1, 3),
    ):
        self.ingestion_ms = ingestion_ms
        self.feature_ms = feature_ms
        self.inference_ms = inference_ms

    def _sleep_ms(self, ms_range):
        delay = random.uniform(*ms_range) / 1000.0
        time.sleep(delay)
        return delay * 1000  # return ms

    def simulate(self):
        """
        Simulate end-to-end latency and return breakdown.
        """
        timings = {}

        timings["ingestion"] = self._sleep_ms(self.ingestion_ms)
        timings["feature"] = self._sleep_ms(self.feature_ms)
        timings["inference"] = self._sleep_ms(self.inference_ms)

        timings["total"] = sum(timings.values())
        return timings

from core.latency import LatencySimulator

lat = LatencySimulator()
print(lat.simulate())
