import pyaudio
import time
import sys
import socket
import threading

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

g_exit = False
g_data = bytes()


p = pyaudio.PyAudio()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(10.0)
lock = threading.Lock()

s = time.time()

def callback(in_data, frame_count, time_info, status):
    global s, g_data
    buf_size = frame_count * 2  # 16bit sound, Sso multiply by 2
    if len(g_data) > buf_size:
        lock.acquire()
        data = g_data[:buf_size]
        g_data = g_data[buf_size:]
        lock.release()
        e = time.time()
        print("play [%d] remain[%d] callback time:%f"%(len(data), len(g_data), e - s))
        s = e
        return (data, pyaudio.paContinue)
    else:
        print("play end [%d]"%(len(g_data)))
        return (None, pyaudio.paComplete)    
        #return (None, pyaudio.paOutputUnderflow)

def sock_recv():
    global g_data
    while not g_exit:
        try:
            data, _ = sock.recvfrom(2048) 
            if len(data):
                lock.acquire()
                g_data += data
                lock.release()
                print("rcv audio %d"%(len(data)))

        except socket.timeout:
            print("time out")
            break
        except KeyboardInterrupt:
            print("Ctrl+C")
            break

def buffering(sec):
    while True:
        if len(g_data) > 320 * 50 * sec: # 320X50 =>1sec audio
            break
        print("udp rcv[%d] wait..."%(len(g_data)))
        time.sleep(0.01)    


t = threading.Thread(target=sock_recv)
t.start()

#You should buffer before make pyaudio stream
buffering(1)

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=8000,
                output=True,
                stream_callback=callback)

stream.start_stream()
t.join()

print("Play End")

stream.stop_stream()
stream.close()
p.terminate()