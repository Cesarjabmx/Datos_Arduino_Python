import tkinter as tk
import serial.tools.list_ports
import functools

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()

root = tk.Tk()
root.config(bg='grey')
root.geometry("838x208")
root.title("LDR con arduino")
root.resizable(0,0)

def initComPort(index):
    currentPort = str(ports[index])
    comPortVar = str(currentPort.split(' ')[0])
    print(comPortVar)
    serialObj.port = comPortVar
    serialObj.baudrate = 9600
    serialObj.open()

for onePort in ports:
    comButton = tk.Button(root, text=onePort, font=('Calibri', '13'), height=1, width=45, command = functools.partial(initComPort, index = ports.index(onePort)))
    comButton.grid(row=ports.index(onePort), column=0)

dataCanvas = tk.Canvas(root, width=400, height=200, bg='white')
dataCanvas.grid(row=0, column=1, rowspan=100)

vsb = tk.Scrollbar(root, orient='vertical', command=dataCanvas.yview)
vsb.grid(row=0, column=2, rowspan=100, sticky='ns')

dataCanvas.config(yscrollcommand = vsb.set)

dataFrame = tk.Frame(dataCanvas, bg="white")
dataCanvas.create_window((10,0),window=dataFrame,anchor='nw')

def checkSerialPort():
    if serialObj.isOpen() and serialObj.in_waiting:
        recentPacket = serialObj.readline()
        #print(recentPacket)
        recentPacketString = recentPacket.decode('utf').rstrip('\n')
        tk.Label(dataFrame, text=recentPacketString).pack()

def leerDatos():
    if serialObj.isOpen() and serialObj.in_waiting:
        leer=serialObj.readline()
        manejar=str(leer)
        sensor=manejar.split(' ')[4]
        voltaje=manejar.split(' ')[7]
        otput=manejar.split(' ')[10]
        vl=voltaje[0:4]
        invol=float(vl)
        print(invol)
       

while True:
    root.update()
    checkSerialPort()
    #leerDatos()
    dataCanvas.config(scrollregion=dataCanvas.bbox("all"))