from serial import Serial # from pyserial package
from serial.tools.list_ports import comports
from time import sleep
from colorama import Fore, Back, Style, init

low_sig_thrsh = 0.1
high_sig_thrsh = 1.7


s = None
def connect():
    i = 0
    while True:
        if i == 1:
            print("Waiting for port...")
        elif i > 1:
            print(".", end="")
        ports = comports()
        i += 1
        for port in ports:
            print("VID:", port.vid)
            if port.vid == 0x303A:
                global s
                s = Serial(port.name, rtscts=False,
                            dsrdtr=False,
                            xonxoff=False,
                            write_timeout=2,
                            )
                print("opened")
                return
        sleep(0.5)


def sendRecord(name):
    # print("sending")
    global s
    s.write((name + "\n\r").encode())
    s.flush()
    # print("sent")
    # xx = s.read_all().decode()
    # print(xx)
    while True:
        line = s.readline().decode("utf-8", errors="ignore").strip()
        if not line:
            continue

        # Check prefix
        if not line.startswith("V6RecDone"):
            continue

        # Expected format: V6RecDone,<float>,<float>
        parts = line.split(",")
        if len(parts) != 3:
            print(f"Malformed line: {line}")
            continue

        try:
            value1 = float(parts[1])
            value2 = float(parts[2])
        except ValueError:
            print(f"Failed to parse floats: {line}")
            continue

        print(Fore.GREEN + f"REC OK!\n[min(signal): {value1}FS, max(signal) {value2}]")

        # if value2-value1 < low_sig_thrsh:
        #     print(Fore.RED + f"WEAK SIGNAL? Peak-to-peak amplitude was {low_sig_thrsh}FS")
        #
        # if value2 - value1 > 1.8:
        #     print(Fore.RED + f"MIC CLIPPING? Peak-to-peak amplitude was > {high_sig_thrsh}FS")
        # if value1 > 0.99 or value2 > 0.99:
        #     print(Fore.RED + f"ADC CLIPPING DETECTED!")

        break
    print("done!")
