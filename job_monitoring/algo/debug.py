import time


def long_running(anything):
    print("Waiting 20 seconds...")
    time.sleep(20)
    print("Done!")
    return anything


def raise_exception(anything):
    print("Waiting 5 seconds before raising an exception...")
    time.sleep(5)
    raise Exception("A very expected error occured!")
