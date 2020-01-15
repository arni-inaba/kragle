import asyncio
import asynctest
import pytest

from kragle import Debouncer


@pytest.mark.asyncio
async def test_debouncer():
    semaphore = asyncio.Semaphore(0)
    event = asyncio.Event()
    test_debouncer.counter = 0

    # We use a lock instead of sleep() to control
    # precisely what happens when instead of relying on timing
    async def lock_it(_unused_delay):
        await semaphore.acquire()

    async def do_it():
        test_debouncer.counter += 1
        event.set()

    with asynctest.patch("asyncio.sleep", lock_it):
        debouncer = Debouncer()
        debouncer.debounce(1, "key1", do_it)
        debouncer.debounce(1, "key1", do_it)
        semaphore.release()
        semaphore.release()
        await event.wait()
        assert test_debouncer.counter == 1
