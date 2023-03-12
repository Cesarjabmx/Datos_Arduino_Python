import tkinter as tk
import serial.tools.list_ports
import functools
import serial,time,collections
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread

isReceiving= False 
isRun = True 
datos = 0.0
muestraD = 100
data = collections.deque([0]*muestraD, maxlen=muestraD)
xmin = 0
xmax = muestraD
ymin = -5
ymax = 5 

def Iniciar():
    global datos
    global isReceiving
    global isRun
    isReceiving = True
    isRun = True   
    thread.start() 
    anim = animacion.FuncAnimation(fig, plotData,  fargs=(muestraD,lines),interval = 100, blit = False )
    plt.show()

def DatosA():
    time.sleep(1)
    serialObj.reset_input_buffer()
    while (isRun):
        global isReceive
        global datos 
        #datos = float(serialObj.readline().decode('utf-8'))
        leer=serialObj.readline()
        manejar=str(leer)
        voltaje=manejar.split(' ')[7]
        vl=voltaje[0:4]
        datos=float(vl)
        print(datos)
        isReceive = True    


def plotData(self,muestraD,lines):
    data.append(datos)
    lines.set_data(range(muestraD), data)
    labelx.set("VOL:" + str(datos)) 
thread = Thread(target = DatosA) 

def Salir():
    global isRun
    isRun = False 
    thread.join()
    arduino.close()
    time.sleep(1)
    raiz.destroy()
    raiz.quit()
    print("proceso finalizado")
    
def Terminar():  
    global isRun
    global isReceiving 
    isRun = False 
    isReceiving = False
    time.sleep(0.5)
    thread.join(timeout=0.3)
    arduino.close()
    datos=00.0

fig = plt.figure(facecolor="0.55",figsize=(6, 4), clear=True, dpi=100)
ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
plt.title("Grafica - 0 - 5 Voltios",color='red',size=16, family="Tahoma")
ax.set_xlabel("Muestras")
ax.set_ylabel("Señal")
lines = ax.plot([] ,[], 'r')[0]

def Limpiar():
    fig.clf()

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()

root = tk.Tk()
root.config(bg='grey')
root.geometry("1100x480")
root.title("LDR con arduino")
root.resizable(1,1)

lienzo = FigureCanvasTkAgg(fig, master = root )
lienzo._tkcanvas.grid(row = 0,column = 0, padx = 1,pady = 1)
frame = tk.Frame(root, width = 130,height = 402, bg = "#7003FC")
frame.grid(row = 0,column = 1, padx = 1,pady = 2)
frame.grid_propagate(False)
frame.config(relief = "sunken")
labelx = tk.StringVar(root, "VOL: 0.00")

label = tk.Label(frame,textvariable = labelx, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="center")
label.grid(row=0,column=0, padx=5,ipady=8, pady=10)
Iniciar = tk.Button(frame,command= Iniciar, text= "Iniciar ",bg="blue",fg="white", font="Helvetica 14 bold",width=9,justify="center")
Iniciar.grid(row=1,column=0, padx=5,pady=5)


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

comButton.place(x=100, y=420)
dataCanvas = tk.Canvas(root, width=400, height=200, bg='white')
dataCanvas.grid(row=0, column=1, rowspan=100)
dataCanvas.place(x=750,y=50)

vsb = tk.Scrollbar(root, orient='vertical', command=dataCanvas.yview)
vsb.grid(row=0, column=2, rowspan=100, sticky='ns')
vsb.place(x=800,y=50)


dataCanvas.config(yscrollcommand = vsb.set)

dataFrame = tk.Frame(dataCanvas, bg="white")
dataCanvas.create_window((10,0),window=dataFrame,anchor='nw')

def checkSerialPort():
    if serialObj.isOpen() and serialObj.in_waiting:
        recentPacket = serialObj.readline()
        #print(recentPacket)
        recentPacketString = recentPacket.decode('utf').rstrip('\n')
        tk.Label(dataFrame, text=recentPacketString).pack()
       

while True:
    root.update()
    checkSerialPort()
    dataCanvas.config(scrollregion=dataCanvas.bbox("all"))
