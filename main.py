from config import *
import time


is_on = True
while is_on:
    time.sleep(60)
    if is_iss_close() and is_dark():
        send_email()





