from django.test import TestCase
import time
import threading


# Create your tests here.

# 计时线程
class Thread_count(threading.Thread):
    def __init__(self, users):
        threading.Thread.__init__(self)
        self.users = users
        self.turn_id = users[0]
        self.turn_index = 0

    def run(self):
        while True:
            print(self.turn_id)
            time.sleep(0.5)
            t_index = self.turn_index
            t_index += 1
            if t_index == len(self.users):
                t_index = 0
            self.turn_index = t_index
            self.turn_id = self.users[t_index]


t1 = Thread_count([1, 2, 3, 4])
t1.start()
