from utime import sleep
from hx711 import HX711  

# Pines donde conectaste el HX711
D_OUT_PIN = 16  
PD_SCK_PIN = 17  

# Inicializa el HX711
hx711 = HX711(d_out=D_OUT_PIN, pd_sck=PD_SCK_PIN)

# Valores de calibración
tara = 0
factor_escala = 1

def calibrar():
    global tara, factor_escala

    # Paso 1: Obtén la lectura de tara (sin peso)
    print("Por favor, asegúrate de que no haya peso en la balanza.")
    sleep(2)
    tara = hx711.read()
    print(f'Lectura de tara: {tara} unidades')

    # Paso 2: Obtén la lectura con un peso conocido
    peso_conocido = float(input("Ingresa el peso conocido en kg: "))
    print("Coloca el peso conocido en la balanza.")
    sleep(5)
    lectura_con_peso = hx711.read()
    print(f'Lectura con peso conocido: {lectura_con_peso} unidades')

    # Calcular el factor de escala
    factor_escala = (lectura_con_peso - tara) / peso_conocido
    print(f'Factor de escala calculado: {factor_escala}')

def leer_peso():
    try:
        lectura = hx711.read()  # Lee el valor actual del HX711
        peso = (lectura - tara) / factor_escala  # Convierte a peso en kg
        print(f'Peso: {peso:.2f} kg')
    except HX711Exception as e:
        print(f'Error al leer el peso: {e}')

def main():
    calibrar()  # Calibrar al inicio

    while True:
        leer_peso()
        sleep(5)  # Espera 5 segundos antes de la siguiente lectura

if __name__ == '__main__':
    main()
