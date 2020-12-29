import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import tkinter.font as tkFont
from tkinter import *
import time
import serial
import threading

PORT = 'com2'
LED_state = 0
LED_state_last = 0
play_times = 0

root = Tk()
fontStyle = tkFont.Font(family="MSYH", size=60)
fontStyle_Button = tkFont.Font(family="MSYH", size=30)

root.title('Slave')
frame1 = Frame(root)
frame2 = Frame(root)
var = StringVar()
textLabel = Label(frame1, textvariable=var, justify=LEFT, font=fontStyle)  # 左对齐
var.set('从机')
textLabel.pack(side=LEFT)
frame1.pack(padx=10, pady=10)

w = Canvas(root, width=600, height=300)
w.pack()

w.create_oval(180, 30, 420, 270, fill='green')  #正方形对应正圆（60-300=30-270）

frame1.pack(padx=10, pady=10)
frame2.pack(padx=100, pady=30)

def updata():
    global slave_1
    global LED_state, play_times, LED_state_last

    while True:
        slave_1.set_values('0', 1, play_times)
        LED_state = slave_1.get_values('0',0,10)
        print(LED_state)
        time.sleep(0.1)
        if LED_state[0] == 1:
            w.create_oval(180, 30, 420, 270, fill='green')
        elif LED_state[0] == 0:
            w.create_oval(180, 30, 420, 270, fill='red')

        if LED_state_last != LED_state[0] and LED_state_last == 1:
            play_times = play_times + 1

        LED_state_last = LED_state[0]

def main():
    global slave_1
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    server = modbus_rtu.RtuServer(serial.Serial(PORT, baudrate= 9600, bytesize=8, parity='N', stopbits=1))

    try:
        logger.info("running...")
        server.start()
        slave_1 = server.add_slave(1)
        slave_1.add_block('0', cst.HOLDING_REGISTERS, 0, 100)

        t = threading.Thread(target=updata) # 利用另一个线程来获得数据
        t.setDaemon(True)
        t.start()

        while True:
            mainloop() #绘图

    finally:
        server.stop()

if __name__ == "__main__":

    main()
