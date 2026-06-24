import time

from app.rate_limit import MinIntervalRateLimiter


def test_rate_limiter_waits_between_calls():
    limiter = MinIntervalRateLimiter(min_interval_seconds=0.05)

    first_wait = limiter.wait()
    start = time.monotonic()
    second_wait = limiter.wait()
    elapsed = time.monotonic() - start

    assert first_wait == 0.0
    assert second_wait > 0.0
    assert elapsed >= 0.045
