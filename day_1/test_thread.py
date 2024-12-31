import threading
import time

def worker():
    print("worker1")
    time.sleep(1)
    print("worker2")


if __name__ == '__main__':
    print("main1")
    t = threading.Thread(target=worker())
    t.start()
    print("main2")
