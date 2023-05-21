import socket
import time
import threading


HOST = "127.0.0.1"
PORT = 5005

data = bytes() # Stream of audio bytes 

BROADCAST_SIZE = 320

AUDIO_FILE = "fourseason.pcm"  #8000, 16BIT, MONO FORMAT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with open(AUDIO_FILE, "rb") as f:   # 8000, 16bit , mono
    # for x in range(20):
    #     buf = f.read(BROADCAST_SIZE * 4)
    #     sock.sendto(buf, (HOST, int(PORT)))
    while True:
        s = time.time()
        buf = f.read(BROADCAST_SIZE)
        if 0 == len(buf) :
            break
        sock.sendto(buf, (HOST, int(PORT)))
        sleep_tm = 0.02 - (time.time() - s)
        print("snd audio %d sleep[%f]"%(len(buf), sleep_tm))
        # time.sleep(0.8 * 0.02)
        time.sleep(0.01)
sock.close()


