import time
import random
import threading
from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame

def main():
    # Find our device
    devs = GsUsb.scan()
    if len(devs) == 0:
        print("Can not find gs_usb device")
        return
    dev = devs[0]

    # Configuration
    if not dev.set_bitrate(500000):
        print("Can not set bitrate for gs_usb")
        return

    # Start device
    dev.start()

    # Prepare frames

    frames=[]
    for i in range(0,0x7FF):
        data = bytearray()
        for byte in range(0, random.randint(1,8)):
            data.append(random.randrange(0, 255))
        data = bytes(data)
        frames.append(GsUsbFrame(can_id=i, data=data))

    print(frames[1].can_id)

    def sender():
        while True:
            for i in range(0,0x7FF):
                num=random.randrange(0,0x7FF)
                if dev.send(frames[num]):
                    print("TX  {}".format(frames[num]))
                    time.sleep(0.01)
    threads=[]
    for i in range(0,15):
        threads.append(threading.Thread(target=sender))
        threads[i].start()
    print(threads)

    '''second = threading.Thread(target=sender)
    third = threading.Thread(target=sender)
    fourth = threading.Thread(target=sender)
    fifth = threading.Thread(target=sender)
    first.start()
    second.start()
    third.start()
    fourth.start()'''
    #fifth.start()




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass