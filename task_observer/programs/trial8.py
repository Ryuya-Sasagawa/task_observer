import signal
import time

stopped = False

out = open('log.txt', 'w')

def stop(sig, frame):
    global stopped
    stopped = True
    out.write('caught SIGTERM\n')
    out.flush()

def ignore(sig, frsma):
    out.write('ignoring signal %d\n' % sig)
    out.flush()

signal.signal(signal.SIGTERM, stop)
# signal.signal(signal.SIGHUP, ignore)

while not stopped:
    out.write('running\n')
    out.flush()
    time.sleep(1)

stop_time = time.time()
while True:
    out.write('%.4fs after stop\n' % (time.time() - stop_time))
    out.flush()
    time.sleep(0.1)