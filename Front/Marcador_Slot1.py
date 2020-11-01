

from tkinter import *
from tkinter import ttk
from tkinter.font import Font
# Importamos la libreira de PySerial
import serial
import xml.etree.ElementTree as ET
import threading
import os
import constantes


#variales generales
tamañoFuenteTextoLog = 20
tamañoFuenteTextoTime = 15
numeroPestaña = 0
#Metodos generales

def botonIncrementarFuente():
    global tamañoFuenteTextoLog
    global inputTextoLog
    tamañoFuenteTextoLog+=1
    print("tamaño fuente:"+str(tamañoFuenteTextoLog))
    inputTextoLog.config(font = Font(family="Verdana", size=tamañoFuenteTextoLog))
    inputTextoLog.see(END)
    

def botonDecrementarFuente():
    global tamañoFuenteTextoLog
    global inputTextoLog
    tamañoFuenteTextoLog-=1
    print("tamaño fuente:"+str(tamañoFuenteTextoLog))
    inputTextoLog.config(font = Font(family="Verdana", size=tamañoFuenteTextoLog))
    inputTextoLog.see(END)
    

def botonResetLog():
    global contenedorTiempos
    print("Reset")
    
    inputTextoLog.config(state='normal')
    inputTextoLog.delete("1.0","end")        
    inputTextoLog.config(state='disabled')
    #ahora toca incializar todos los componentes
    while len(contenedorTiempos) > 0 : contenedorTiempos.pop()
    frameTextoTime1.changeTime("--:--")
    frameTextoTime2.changeTime("--:--")
    frameTextoTime3.changeTime("--:--")
    frameTextoTime4.changeTime("--:--")
    frameTextoTime5.changeTime("--:--")
    frameTextoTime6.changeTime("--:--")
    frameTextoTime7.changeTime("--:--")
    frameTextoTime8.changeTime("--:--")
    frameTextoTime9.changeTime("--:--")
    frameTextoTime10.changeTime("--:--")

    frameTextoMinLap.changeTime("--:--")
    frameTextoAVGLap.changeTime("--:--")
    frameTextoAVGALLLap.changeTime("--:--")
    frameTextoWorstLap.changeTime("--:--")
    frameTextoTotal.changeTime("--:--")
    frameNumLaps.changeTime("--:--")


def resize_it(event):
    global ventana # Main Window
    global frameLog 
    global frameTablaTiempos 
    widthG = (event.width*4)/8
    widthS = (event.width*3)/8
    #Reconfigure the main window's and frames' dimensions  
    print("Tamaño de la ventana wid:%f  height:%f"%(event.width,event.height))    
    frameLog.configure(width=widthG, height=event.height)
    frameTablaTiempos.configure(width=widthS, height=event.height)
    print("Tamaño de la ventana G:%f  S:%f"%((widthG),(widthS)))    
    ventana.configure(width=event.width, height=event.height)
    


contenedorTiempos = []


class ConectorPuertoSerie(threading.Thread):
    global  contenedorTiempos  
    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()
    def __del__(self): 
        print('Destructor called, Employee deleted.') 

    def run(self):
        global inputTextoLog
        #empezamos con la lectura del puerto
        # Abrimos el puerto del arduino a 9600
        PuertoSerie = serial.Serial('/dev/ttyUSB0', 9600)
        loop_active = True
        reinicioVentana = 0
        while loop_active:
            # leemos hasta que encontarmos el final de linea
            #ventana.update()
            reinicioVentana +=1 
            sCadenaPuertoSerie = PuertoSerie.readline()
            # Mostramos el valor leido y eliminamos el salto de linea del final
            print("sCadenaPuertoSerie"+str(sCadenaPuertoSerie.decode('utf-8')))
            textoMostrar = sCadenaPuertoSerie.decode('utf-8').strip()
            print(textoMostrar)
                                    
            if reinicioVentana > 25:
                reinicioVentana = 0
                inputTextoLog.config(state='normal')
                inputTextoLog.delete("1.0","end")        
                inputTextoLog.config(state='disabled')
                #botonResetLog()

            inputTextoLog.config(state='normal')
            inputTextoLog.insert(END,str(textoMostrar)+"\n")
            inputTextoLog.see(END)
            inputTextoLog.config(state='disabled')
            #Pasamos al manejo de los tiempos
            self.procesarTiempo(textoMostrar)

    def procesarTiempo(self,entradaArduino):
        try:
            root = ET.fromstring(entradaArduino)
            print("Procesar tiempo, entrada parseada:",root)
            if root != None:
                hijo = root.find("reset")
                print("Reset:",hijo)
                if hijo != None:
                    #reseteamos todo el chiringuito
                    botonResetLog()
                    
                hijo = root.find("infoPaso")
                print("infoPaso:",hijo)
                if hijo != None:
                    tiempo = hijo.get("timeLap")
                    print("Tiempo reicibido",tiempo)
                    contenedorTiempos.append(float(tiempo))
                    print("contenedorTiempos:",contenedorTiempos)
                    contenedorTiempos.sort()
                    print("contenedorTiemposss:",contenedorTiempos)
                    numTiempos = 0
                    totalTiempo = 0.0
                    tiempoMedioMejor = 0.0
                    tiempoMin = 0.0
                    for time in contenedorTiempos:
                        numTiempos += 1
                        totalTiempo = totalTiempo + time
                        print("Time reicibido",time)
                        if numTiempos == 1:
                            frameTextoTime1.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"BEST")
                        if numTiempos == 2:
                            frameTextoTime2.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 3:
                            frameTextoTime3.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 4:
                            frameTextoTime4.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 5:
                            frameTextoTime5.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 6:
                            frameTextoTime6.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 7:
                            frameTextoTime7.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 8:
                            frameTextoTime8.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 9:
                            frameTextoTime9.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos == 10:
                            frameTextoTime10.changeTime(self.formatTime(time))
                            self.lanzarSonido(tiempo,time,"GEN")
                        if numTiempos <= 10:
                            tiempoMedioMejor = tiempoMedioMejor + time
                    print("tiempoMedioMejor:",tiempoMedioMejor)
                    frameTextoTotal.changeTime(self.formatTime(totalTiempo))
                    frameNumLaps.changeTime(len(contenedorTiempos))
                    frameTextoMinLap.changeTime(self.formatTime(tiempoMin))
                    print("numTiempos:",numTiempos)   
                    if 0 < numTiempos < 10:
                        print("frameTextoAVGLapG :%f  S:%f"%((tiempoMedioMejor),(numTiempos)))
                        frameTextoAVGLap.changeTime(self.formatTime(tiempoMedioMejor / numTiempos))
                    elif numTiempos > 10:
                        print("frameTextoAVGLapG :%f  S:%f"%((tiempoMedioMejor),(10)))
                        frameTextoAVGLap.changeTime(self.formatTime(tiempoMedioMejor / 10))
                    if numTiempos > 0:
                        print("numTiempos>0:")  
                        frameTextoAVGALLLap.changeTime(self.formatTime(totalTiempo/len(contenedorTiempos)))
                        frameTextoWorstLap.changeTime(self.formatTime(contenedorTiempos[-1]))
        except:
            print("Problema de parseo sale por pantalla")

    def formatTime(self,time):
        tiempoFormateado =  '{:06.3f}'.format(time)
        return tiempoFormateado

    def lanzarSonido(self,tiempo,tiempoAlmacenado,modo):
        print("lanzarSonido:",tiempo,tiempoAlmacenado)
        if (float(tiempo) == tiempoAlmacenado):
            if(modo == "BEST"):
               os.system('play -nq -t alsa synth {} sine {}'.format(0.1, 640))
               os.system('play -nq -t alsa synth {} sine {}'.format(0.1, 640))
               os.system('play -nq -t alsa synth {} sine {}'.format(0.1, 640))
            if(modo == "GEN"):
                os.system('play -nq -t alsa synth {} sine {}'.format(0.1, 640))

                    

    

class FrameTextoTime(ttk.Frame):
    global wCalculado
    def __init__(self, master,texto):
        self.frameTextoTime = ttk.Frame(master, style="styleFrameTextoTime.TFrame", width=wCalculado )
        self.frameTextoTime.pack(expand=True, fill=BOTH, side=TOP, anchor=N)
        self.labelTextoTimeInfo = LabelTextoTimeInfo(self.frameTextoTime,texto)
        self.labelTextoTimeHijo = LabelTextoTime(self.frameTextoTime)

    def changeTime(self,time):
        print('FrameTextoTime.changeTime:') 
        self.labelTextoTimeHijo.changeTime(time)

class LabelTextoTime(ttk.Label):
    def __init__(self, frame):
        self.labelTextoTime = ttk.Label(frame,text="--:--",style="styleLabelTextoTime.TLabel")
        self.labelTextoTime.pack(expand=True, fill=BOTH, side=TOP, anchor=N,pady=1,padx=1)

    def changeTime(self,time):
        print('LabelTextoTime.changeTime:') 
        self.labelTextoTime['text'] = time

class LabelTextoTimeInfo(ttk.Label):
    def __init__(self, frame,texto):
        self.labelTextoTime = ttk.Label(frame,text=texto,style="styleLabelTextoTimeInfo.TLabel")
        self.labelTextoTime.pack(expand=False,  side=TOP, anchor=NW,pady=3,padx=3)
        


# Configuración de la raíz
ventana = Tk()
ventana.title("Slot counter 2.0")
ventana.resizable(1,1)
w, h = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
#w = 320
#h = 480
wCalculado = w/10
hCalculado = h/25
print("W:%f  H:%f"%((w),(h)))    
print("Calculado W:%f  H:%f"%((wCalculado),(hCalculado))) 
ventana.geometry("%dx%d+0+0" % (w, h))
#Estilos
style = ttk.Style()
style.configure("styleFrameTextoTime.TFrame", background='white',bd=2,relief=RIDGE)
style.configure("styleLabelTextoTime.TLabel", background='white',font = ("Verdana", 24),anchor="CENTER")
style.configure("styleLabelTextoTimeInfo.TLabel", background='white',font = ("Verdana", 10),anchor="NW")
style.configure("styleLabelTexto.TLabel", background='white',font = ("Verdana", 20),anchor="CENTER",relief=RIDGE)
#red  blue green2  orange red   ,foreground='orange red'
#label.config(bg="gray")

frameGeneral = Frame(ventana)
frameGeneral.config(cursor="pirate")
frameGeneral.config(bg="lightblue")
frameGeneral.config(bd=10)
frameGeneral.config(relief="sunken")
frameGeneral.pack(fill='both', expand=1)



labelTituloPestañaLog = Label(frameGeneral,text="Ventana de trabajo:")
labelTituloPestañaLog.pack(anchor=NW)


botonIncFont = Button(frameGeneral, text="+", command=botonIncrementarFuente,width=50)
botonIncFont.pack()
botonDecFont = Button(frameGeneral, text="-", command=botonDecrementarFuente,width=50)
botonDecFont.pack()
botonReset = Button(frameGeneral, text="Reset", command=botonResetLog,width=50)
botonReset.pack()


frameDatos = Frame(frameGeneral)
frameDatos.config(bg='Blue')
frameDatos.pack(fill='both',expand=1)

#####Create a blue (second) Frame
frameTablaTiempos = Frame(frameDatos,  bg='blue', width=wCalculado*2)
frameTablaTiempos.pack(side='left', expand=True, fill=BOTH)

####Create a red (first) Frame
frameLog = Frame(frameDatos, bg='red', width=wCalculado*8)
frameLog.pack(side='left', expand=TRUE, fill=BOTH)

scrollFrameLog = Scrollbar(frameLog) 
scrollFrameLog.pack(side = RIGHT, fill = Y) 
inputTextoLog = Text(frameLog, wrap = NONE, yscrollcommand = scrollFrameLog.set) 
inputTextoLog.config(font = Font(family="Verdana", size=tamañoFuenteTextoLog))
scrollFrameLog.config(command=inputTextoLog.yview) #importante es el enlace entre el text y el scroll

inputTextoLog.pack(side=TOP, fill='both',expand=1)
inputTextoLog.see(END)
inputTextoLog.config(state='disabled')



#####Create a table tiempos específicos





frameTablaAVGLaps = Frame(frameTablaTiempos, bg='khaki', width=wCalculado)
frameTablaAVGLaps.pack(side=LEFT, expand=YES, fill=BOTH)
ttk.Label(frameTablaAVGLaps,text="AVG Laps:",style="styleLabelTexto.TLabel").pack(anchor=N,side=TOP,fill=X,expand=NO)
frameTablaAVGLapsCont = Frame(frameTablaAVGLaps, bg='khaki3', width=wCalculado)
frameTablaAVGLapsCont.pack(expand=YES, fill=BOTH,anchor=N,side=TOP)
frameTextoMinLap = FrameTextoTime(frameTablaAVGLapsCont,"Min Lap")
frameTextoAVGLap = FrameTextoTime(frameTablaAVGLapsCont,"Avg Best Lap")
frameTextoAVGALLLap = FrameTextoTime(frameTablaAVGLapsCont,"Avg All Lap")
frameTextoWorstLap = FrameTextoTime(frameTablaAVGLapsCont,"Worst Lap")
frameTextoTotal = FrameTextoTime(frameTablaAVGLapsCont,"Total Time")
frameNumLaps = FrameTextoTime(frameTablaAVGLapsCont,"Num Laps")

frameTablaBestLaps = Frame(frameTablaTiempos, bg='cyan', width=wCalculado)
frameTablaBestLaps.pack(side=LEFT, expand=YES, fill=BOTH)
ttk.Label(frameTablaBestLaps,text="Best Laps:",style="styleLabelTexto.TLabel").pack(anchor=N,side=TOP,fill=X,expand=NO)
frameTablaBestLapsCont = Frame(frameTablaBestLaps, bg='cyan4', width=wCalculado)
frameTablaBestLapsCont.pack(expand=YES, fill=BOTH,anchor=N,side=LEFT)
frameTextoTime1 = FrameTextoTime(frameTablaBestLapsCont,"Lap 1")
frameTextoTime2 = FrameTextoTime(frameTablaBestLapsCont,"Lap 2")
frameTextoTime3 = FrameTextoTime(frameTablaBestLapsCont,"Lap 3")
frameTextoTime4 = FrameTextoTime(frameTablaBestLapsCont,"Lap 4")
frameTextoTime5 = FrameTextoTime(frameTablaBestLapsCont,"Lap 5")
frameTextoTime6 = FrameTextoTime(frameTablaBestLapsCont,"Lap 6")
frameTextoTime7 = FrameTextoTime(frameTablaBestLapsCont,"Lap 7")
frameTextoTime8 = FrameTextoTime(frameTablaBestLapsCont,"Lap 8")
frameTextoTime9 = FrameTextoTime(frameTablaBestLapsCont,"Lap 9")
frameTextoTime10 = FrameTextoTime(frameTablaBestLapsCont,"Lap 10")






ventana.update()

 
# Finalmente bucle de la aplicación
THLectorPuertoSerie = ConectorPuertoSerie(ventana)
def _delete_window():
    print ("delete_window")
    try:
        ventana.destroy()
    except:
        pass

def _destroy(event):
    print ("destroy")

ventana.protocol("WM_DELETE_WINDOW", _delete_window)
ventana.bind("<Destroy>", _destroy)

#ventana.bind('<Configure>', resize_it)
ventana.mainloop()