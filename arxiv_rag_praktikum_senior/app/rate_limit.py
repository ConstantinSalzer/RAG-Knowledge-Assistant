import time
from dataclasses import dataclass, field


@dataclass
class MinIntervalRateLimiter:
    min_interval_seconds: float
    last_start_monotonic: float | None = field(default=None)

    def wait(self) -> float:
        now = time.monotonic()

        if self.last_start_monotonic is None:
            self.last_start_monotonic = now
            return 0.0

        elapsed = now - self.last_start_monotonic
        wait_seconds = max(0.0, self.min_interval_seconds - elapsed)

        if wait_seconds > 0:
            time.sleep(wait_seconds)

        self.last_start_monotonic = time.monotonic()
        return wait_seconds
