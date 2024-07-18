# micropython-hx711
Este repositorio contiene un proyecto de medición de peso utilizando el convertidor analógico-digital HX711 y el microcontrolador ESP32. El objetivo principal es sensar el peso de un objeto y realizar la calibración necesaria para obtener medidas precisas en kilogramos.

#Contenido del Repositorio
Librería HX711: Una clase en Python que facilita la interacción con el sensor HX711.
Script de Lectura de Peso: Un script que utiliza la librería HX711 para calibrar y leer el peso, mostrando los resultados en la consola cada 5 segundos.

#Archivos Principales
  hx711.py:
    Implementación de la clase HX711 para interactuar con el sensor de peso.
    Incluye métodos para calibración, lectura de datos y conversión de las lecturas a unidades de peso reales.
    
  main.py:
    Script principal que calibra la balanza y lee el peso de manera continua.
    Muestra el peso en kilogramos en la consola cada 5 segundos.

#Instrucciones de Uso
  Configuración de Pines: Ajusta los pines D_OUT_PIN y PD_SCK_PIN en main.py según tu configuración de hardware.
  Calibración:
    Al iniciar el script, asegúrate de que la balanza esté vacía para obtener la tara.
    Luego, coloca un peso conocido en la balanza para calcular el factor de escala.
  Ejecución: Ejecuta main.py para comenzar a leer el peso continuamente.

#Requisitos
Microcontrolador ESP32
Sensor de peso HX711
