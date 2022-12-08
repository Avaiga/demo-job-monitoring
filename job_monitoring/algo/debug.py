import time


def long_running(anything):
    print("Waiting 20 seconds...")
    time.sleep(20)
    print("Done!")
    return anything
