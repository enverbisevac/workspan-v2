import threading
from workspan.counter import Counter

def test_increment():
    counter = Counter()
    got = counter.inc()
    expected = 1

    assert got == expected

def test_threading():
    counter = Counter()

    def incrementor():
        for i in range(1000):
            counter.inc()

    threads = []
    for i in range(3):
        thread = threading.Thread(target=incrementor)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    assert counter.value == 3000