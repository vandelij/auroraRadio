import os
import signal
import subprocess
import time


gnu_radio_script = subprocess.Popen("~/Desktop/Aurora_Radio/rtl_sdr_test.py", shell=True, preexec_fn=os.setsid)

pause = 12
print(f'Waiting {pause} seconds..')
time.sleep(pause)

print('Killing all children...')
os.killpg(os.getpgid(gnu_radio_script.pid), signal.SIGTERM)

print('Should be dead')

print('Now lets do some other stuff!')


for i in range(4):
    print(f'hello number {i}')
    time.sleep(2)

print('Okay the script is done now')
