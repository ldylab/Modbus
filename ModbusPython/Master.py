from tkinter import *
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import tkinter.font as tkFont

press_state = True
play_time = 0

#按键按下的函数
def callback():
    global press_state, play_time
    if press_state == True:
        state = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 8)  # 这里可以修改需要读取的功能码
        print(state)
        w.create_oval(180, 30, 420, 270, fill='green')
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, output_value=1)  # 对其中的从机中一个数据进行修改
        press_state = False
        play_time = state[1]
        play_state = "开始"
    elif press_state == False:
        state = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 8)  # 这里可以修改需要读取的功能码
        print(state)
        w.create_oval(180, 30, 420, 270, fill='red')
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, output_value=0)  # 对其中的某一个数据进行修改
        press_state = True
        play_time = state[1]
        play_state = "停止"

    display_string = '主机：第'+ str(play_time) + '次运行' + play_state
    var.set(display_string)

#TK界面的设定
root = Tk()
fontStyle = tkFont.Font(family="MSYH", size=60)
fontStyle_Button = tkFont.Font(family="MSYH", size=20)

root.title('Master')

w = Canvas(root, width=600, height=300)
w.pack()
w.create_oval(180, 30, 420, 270, fill='red')  #绘制开始LED

frame1 = Frame(root)
frame2 = Frame(root)

var = StringVar()
var.set('主机：第0次运行停止')

textLabel = Label(frame1, textvariable=var, justify=LEFT, font=fontStyle)  # 左对齐
textLabel.pack(side=LEFT)

theButton = Button(frame2, text='开始/停止', command=callback, height = 3, width = 10, font=fontStyle_Button) #显示按钮
theButton.pack()

frame1.pack(padx=10, pady=10)
frame2.pack(padx=100, pady=30)

#modbus的初始化设定
master = modbus_rtu.RtuMaster(serial.Serial(port="com1", baudrate=9600, bytesize=8, parity='N', stopbits=1))
master.set_timeout(5.0)
master.set_verbose(True)
master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, 1)

if __name__ == "__main__":
    mainloop()

