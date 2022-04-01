import serial
import time
import threading

line = ''

ser = serial.Serial('/dev/ttyS0', 115200, timeout=3)

alivethread = True

def readthread(ser):
    global line

    while alivethread:
        for c in ser.read():
            line = line + (chr(c))
            if line.startswith('[') and line.endswith(']'):
                print('receive data=' + line)
                line = ''
    ser.close()

def test_main():
    thread = threading.Thread(target=readthread, args=(ser,))
    thread.start()

    count = 10
    while count > 0:
        strcmd = '[test' + str(count) + ']'
        print('send data=' + strcmd)
        ser.write(strcmd.encode())
        time.sleep(1)
        count = count - 1

    alivethread = False

def write(word, test=True, START='Y'):
    WORD = '*' + START + ',' + word + '\n'
    #print(len(WORD))
    Trans = WORD.encode('utf-8')
    ser.write(Trans)

    if test:
        line = ''
        while True:
            c = ser.read()
            line = line + str(c.decode())
        
            if c == b'\n':
                print(line)
                line = ''
                break

if __name__ == '__main__':
    test_main()
