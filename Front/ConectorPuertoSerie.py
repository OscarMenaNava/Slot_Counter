import threading
import serial
import xml.etree.ElementTree as ET

class ConectorPuertoSerie(threading.Thread):
    def __init__(self, tk_root,procesarTiempo):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.procesarTiempo = procesarTiempo
        self.start()
    def __del__(self): 
        print('Destructor ConectorPuertoSerie called') 

    def run(self):
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
          
            #Pasamos al manejo de los tiempos
            self.procesarTiempo(textoMostrar)