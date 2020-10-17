#include <NewPing.h>
#include <LightChrono.h>
//vamos a hacer un contador de vueltas de scalextric básico, conteo de vueltas y tiempo de vuelta
//salida por la consola
//el control del paso se realiza con sonar
//no distingue entre carril, es para uso personal con un solo cruce

//información del sensor
int const IDENTIFICADOR_SENSOR = 111;
int const IDENTIFICAOR_CARRIL = 1;
//configuracion pines
int const TRIGGER_PIN = 9;
int const ECHO_PIN = 10;
int const INTERRUPTOR_REINICIO = 0;
//configuracion funcionamientos
int const MAX_DISTANCE = 10;
String const LOG_LEVEL_MID = "MID";//Estados posibles
String const LOG_LEVEL_DEBUG = "DEBUG";//Estados posibles, incluye este y el MID
String const LOG_LEVEL = "MID";//Estados a mostrar
int const COMIENZO_PISTA = 2;//límite más cercano de la pista al sensor
int const FIN_PISTA = 7;//límite más separado de la pista al sensor
int const CONTROL_SENIAL_FANTASMA = 2000;
int const CONTROL_BOTON_FANTASMA = 1000;

//variables

int num_vuelta = 0;//contador de vueltas llevadas
int tiempo_lectura = -1000;
int tiempo;
unsigned long tiempo_lectura_int_boton;
int distancia_leida;//lectura del sensor
NewPing sonar(TRIGGER_PIN, ECHO_PIN, FIN_PISTA);
LightChrono chrono_tanda; //crono general de la tanda
LightChrono chrono_vuelta;
boolean trabajando = false;
boolean reinicioTanda = false;
unsigned long tiempo_vuelta;//tiempo lectura en la vuelta
unsigned long tiempo_tanda;//tiempo tanda
unsigned long tiempo_mejor_vuelta  = 999999;//tiempo mejor en la tanda de vueltas

void setup() {
  ///pinMode(TRIGGER, OUTPUT);
  pinMode(INTERRUPTOR_REINICIO, INPUT_PULLUP);
  attachInterrupt(INTERRUPTOR_REINICIO, reiniciarTanda, HIGH);
  Serial.begin(9600);
  mensajeLOG(LOG_LEVEL_DEBUG,"Arrancado.......");
}
void mensajeLOG(String level ,String mensaje){
  boolean mostrarMensaje = false;
  if (LOG_LEVEL == LOG_LEVEL_DEBUG) mostrarMensaje = true;
  if (LOG_LEVEL == LOG_LEVEL_MID && LOG_LEVEL_MID == level) mostrarMensaje = true;
  if(mostrarMensaje){
    Serial.println(mensaje);
  }
}
void mensajeVueltaXML(int lap,unsigned long tiemeLap, char bLap){
    //<root><infoPaso  idSensor='' idCarril='' lap='' timeLap='' bLap=''/></root>
    String mensaje =String();
    mensaje.concat("<root>");
    mensaje.concat("<infoPaso ");
    mensaje.concat("idSensor='");mensaje.concat(IDENTIFICADOR_SENSOR);mensaje.concat("'   ");
    mensaje.concat("idCarril='");mensaje.concat(IDENTIFICAOR_CARRIL);mensaje.concat("'    ");
    mensaje.concat("lap='");mensaje.concat(lap);mensaje.concat("'   ");
    mensaje.concat("timeLap='");mensaje.concat(formatear3Dig(String(tiemeLap/1000)));mensaje.concat("."),mensaje.concat(formatear3Dig(String(tiemeLap-(tiemeLap/1000)*1000)));mensaje.concat("'   ");
    mensaje.concat("bLap='");mensaje.concat(bLap);mensaje.concat("'");
    mensaje.concat("/>");
    mensaje.concat("</root>");

    Serial.println(mensaje);
  
}
void mensajeStartXML(){
    //<root><start  idSensor="" idCarril=""/></root>
    String mensaje =String();
    mensaje.concat("<root>");
    mensaje.concat("<start ");
    mensaje.concat("idSensor='");mensaje.concat(IDENTIFICADOR_SENSOR);mensaje.concat("'   ");
    mensaje.concat("idCarril='");mensaje.concat(IDENTIFICAOR_CARRIL);mensaje.concat("'    ");
    mensaje.concat("/>");
    mensaje.concat("</root>");

    Serial.println(mensaje);
  
}
String formatear3Dig(String digito){
  String cadena = "";
  if (digito.length() == 0) cadena = "000";
  if (digito.length() == 1) cadena = "00" + digito;
  if (digito.length() == 2) cadena = "0" + digito;
  if (digito.length() == 3) cadena = digito;
  return cadena;
}

void reiniciarTanda(){
  unsigned long tiempo = millis();
  mensajeLOG(LOG_LEVEL_DEBUG,"Interrupcion");
  mensajeLOG(LOG_LEVEL_DEBUG,"tiempo: " + String(tiempo));
  mensajeLOG(LOG_LEVEL_DEBUG,"tiempo_lectura_int_boton: " + String(tiempo_lectura_int_boton));

  if ((tiempo - tiempo_lectura_int_boton) > CONTROL_BOTON_FANTASMA){
    tiempo_lectura_int_boton = tiempo;
    reinicioTanda = true;
  }
}
void loop(){
delay(1);

    distancia_leida = sonar.ping_cm();
    if (distancia_leida != 0){
        mensajeLOG(LOG_LEVEL_DEBUG,"Tenemos distancia");  
        //ha pasado objeto 
        if(!trabajando){
          mensajeLOG(LOG_LEVEL_DEBUG,"Ponemos chrono en marcha");
          mensajeStartXML();
          chrono_vuelta.restart();
          chrono_tanda.restart();
          trabajando = true;
        } else {
           if (chrono_vuelta.hasPassed(CONTROL_SENIAL_FANTASMA)){
              num_vuelta = num_vuelta + 1;
              tiempo_vuelta = chrono_vuelta.elapsed();
              tiempo_tanda = chrono_tanda.elapsed();
              char indicadorVueltaRapida =' ';
              if (tiempo_vuelta<tiempo_mejor_vuelta){
                  //estamos en vuelta rápida
                  indicadorVueltaRapida = '*';             
                  tiempo_mejor_vuelta = tiempo_vuelta;
              } 
              mensajeVueltaXML(num_vuelta,tiempo_vuelta,indicadorVueltaRapida);
              chrono_vuelta.restart();
          } else {
            mensajeLOG(LOG_LEVEL_DEBUG,"No ha pasado tiempo de seguridad");
          }
          
        }
      
    }
    //En el caso de que haya llegado la interrupción de reiniciar las tandas
    if (reinicioTanda){
      reinicioTanda = false;
       // generaremos una línea con la información del grupo de vueltas ue llevemos
      // num de vueltas realizadas
      // y el tiempo mejor de las vueltas
      // posibilidad del tiempo total
      //<root><resumenTanda  idSensor='' idCarril='' totalTime='' numTotalLap='' bestLap=''/></root>
      String mensaje =String();
      mensajeLOG(LOG_LEVEL_DEBUG,"Mandamos instrucción de reseteo");
      Serial.println("<root><reset /></root>");
      mensajeLOG(LOG_LEVEL_MID,"-----------------------------------------------------------------------------------------");
      mensajeLOG(LOG_LEVEL_DEBUG,"Reiniciamos el conteo");
      mensajeLOG(LOG_LEVEL_DEBUG,"Vueltas " + String(num_vuelta));
      mensajeLOG(LOG_LEVEL_DEBUG,"Best Lap " + String(tiempo_mejor_vuelta/1000) + "s " + String(tiempo_mejor_vuelta-(tiempo_mejor_vuelta/1000)*1000) + ".ms ");
      mensaje.concat("<root>");
      mensaje.concat("<resumenTanda ");
      mensaje.concat("idSensor='");mensaje.concat(IDENTIFICADOR_SENSOR);mensaje.concat("'   ");
      mensaje.concat("idCarril='");mensaje.concat(IDENTIFICAOR_CARRIL);mensaje.concat("'    ");
      mensaje.concat("totalTime='");mensaje.concat(formatear3Dig(String(tiempo_tanda/1000)));mensaje.concat("."),mensaje.concat(formatear3Dig(String(tiempo_tanda-(tiempo_tanda/1000)*1000)));mensaje.concat("'   ");
      mensaje.concat("numTotalLap='");mensaje.concat(num_vuelta);mensaje.concat("'   ");
      mensaje.concat("bestLap='");mensaje.concat(formatear3Dig(String(tiempo_mejor_vuelta/1000)));mensaje.concat("."),mensaje.concat(formatear3Dig(String(tiempo_mejor_vuelta-(tiempo_mejor_vuelta/1000)*1000)));mensaje.concat("'   ");
      mensaje.concat("/>");
      mensaje.concat("</root>");
      Serial.println(mensaje);
      mensajeLOG(LOG_LEVEL_MID,"-----------------------------------------------------------------------------------------");
      trabajando = false;
      num_vuelta = 0;
      tiempo_vuelta = 0;
      tiempo_tanda = 0;
      tiempo_mejor_vuelta  = 999999;
      
    }
}
