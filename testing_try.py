import time

try:
    print('hello')
    print('sleeping for 5 seconds')
    time.sleep(5)
    term = 5/0

except KeyboardInterrupt:
    print('exiting as asked!')

except Exception:
    print('You cant divide by zero fam.')