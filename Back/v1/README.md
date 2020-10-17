# Back Slot_Counter v1

En esta rama el trabajamos con un módulo arduino (este ejemplo está realizado con un módulo nano) en el que se le agrega un sensor sonar y un pulsador para resetearlo.
Los mensajes que retorna:
<start idSensor='' idCarril=''>
	Indica el primer paso del coche y se pone el crono activo.
	Indica el id del sensor que se activa y el carril sobre el que trabaja
<infopaso idSensor='' idCarril='' lap='' timeLap='' bLap=''>
	Indica el paso de un coche
	lap: indica la vuelta que ha terminado
	timeLap: indica el tiempo en la vuelta que ha terminado
	blap: asterico para indicar que es la mejor vuelta en esta tanda
<reset>
	Evento generado cuando se pulsa en el botón de reseteo.
	Aparte de este evento retorna una información estadística de la tanda que ha terminado.
	<resumenTanda idSensor='' idCarril='' totalTime='' numTotalLap='' bestLap=''/>
	Este resmuen de la información creo que el nombre de los campos son descritivos.
