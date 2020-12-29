from tkinter import *
import serial
import time
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import tkinter.font as tkFont

PORT = "/dev/tty.usbserial-14310"

press_state = True
play_time = 0

def callback():
    global press_state, play_time
    if press_state == True:
        w.create_oval(180, 30, 420, 270, fill='green')
        logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 13, output_value=0))
        play_time_temp = master.execute(1, cst.READ_INPUT_REGISTERS, 100, 1)
        press_state = False
        play_time = play_time_temp[0]
        play_state = "开始"
    elif press_state == False:
        w.create_oval(180, 30, 420, 270, fill='red')
        logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 13, output_value=1))
        play_time_temp = master.execute(1, cst.READ_INPUT_REGISTERS, 100, 1)
        press_state = True
        play_time = play_time_temp[0]
        play_state = "停止"

    display_string = '第'+ str(play_time) + '次运行' + play_state
    var.set(display_string)

root = Tk()
fontStyle = tkFont.Font(family="Lucida Grande", size=60)
fontStyle_Button = tkFont.Font(family="Lucida Grande", size=30)

root.title('Canvas')

w = Canvas(root, width=600, height=300)
w.pack()

w.create_oval(180, 30, 420, 270, fill='red')  #正方形对应正圆（60-300=30-270）

frame1 = Frame(root)

frame2 = Frame(root)

var = StringVar()

var.set('第0次运行停止')

textLabel = Label(frame1,

                  textvariable=var,

                  justify=LEFT, font=fontStyle)  # 左对齐

textLabel.pack(side=LEFT)

theButton = Button(frame2, text='开始/停止运行', command=callback, height = 3, width = 10, font=fontStyle_Button) #显示按钮

theButton.pack()

frame1.pack(padx=10, pady=10)

frame2.pack(padx=100, pady=30)


#Modbus Master Init Setting
logger = modbus_tk.utils.create_logger("console")
#Connect to the slave setting the master
master = modbus_rtu.RtuMaster(
    serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
)
master.set_timeout(5.0)
master.set_verbose(True)
logger.info("connected")
time.sleep(2)

mainloop()
