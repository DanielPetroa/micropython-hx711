from utime import sleep_us, time
from machine import Pin
from micropython import const


class HX711Exception(Exception):
    #Excepción base para errores de HX711
    pass


class InvalidMode(HX711Exception):
    #Excepción lanzada cuando el modo es inválido
    pass


class DeviceIsNotReady(HX711Exception):
    # Excepción lanzada cuando el dispositivo no está listo
    pass


class HX711(object):
    
    # Controlador para Micropython del Convertidor Analógico a Digital de 24 bits HX711 de Avia Semiconductor

    CHANNEL_A_128 = const(1)  # Canal A con ganancia de 128
    CHANNEL_A_64 = const(3)   # Canal A con ganancia de 64
    CHANNEL_B_32 = const(2)   # Canal B con ganancia de 32

    DATA_BITS = const(24)          # Número de bits de datos
    MAX_VALUE = const(0x7fffff)    # Valor máximo posible
    MIN_VALUE = const(0x800000)    # Valor mínimo posible
    READY_TIMEOUT_SEC = const(5)   # Tiempo máximo de espera para que el dispositivo esté listo
    SLEEP_DELAY_USEC = const(80)   # Retardo para entrar en modo de bajo consumo

    def __init__(self, d_out: int, pd_sck: int, channel: int = CHANNEL_A_128):
        self.d_out_pin = Pin(d_out, Pin.IN)
        self.pd_sck_pin = Pin(pd_sck, Pin.OUT, value=0)
        self.channel = channel

    def __repr__(self):
        return "HX711 en canal %s, ganancia=%s" % self.channel

    def _convert_from_twos_complement(self, value: int) -> int:

        # Convierte un entero dado del formato de complemento a dos.

        if value & (1 << (self.DATA_BITS - 1)):
            value -= 1 << self.DATA_BITS
        return value

    def _set_channel(self):
        """
        La selección de entrada y ganancia se controla mediante
        el número de pulsos en el pin PD_SCK:
        3 pulsos para el Canal A con ganancia 64
        2 pulsos para el Canal B con ganancia 32
        1 pulso para el Canal A con ganancia 128
        """
        for i in range(self._channel):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)

    def _wait(self):
        
        # Si el HX711 no está listo dentro de READY_TIMEOUT_SEC, se lanzará la excepción DeviceIsNotReady.
 
        t0 = time()
        while not self.is_ready():
            if time() - t0 > self.READY_TIMEOUT_SEC:
                raise DeviceIsNotReady()

    @property
    def channel(self) -> tuple:
        
        # Obtiene el canal de entrada actual en forma de una tupla (Canal, Ganancia)
        
        if self._channel == self.CHANNEL_A_128:
            return 'A', 128
        if self._channel == self.CHANNEL_A_64:
            return 'A', 64
        if self._channel == self.CHANNEL_B_32:
            return 'B', 32

    @channel.setter
    def channel(self, value):
        """
        Establece el canal de entrada:
        HX711.CHANNEL_A_128 - Canal A con ganancia 128
        HX711.CHANNEL_A_64 - Canal A con ganancia 64
        HX711.CHANNEL_B_32 - Canal B con ganancia 32
        """
        if value not in (self.CHANNEL_A_128, self.CHANNEL_A_64, self.CHANNEL_B_32):
            raise InvalidMode('La ganancia debe ser una de HX711.CHANNEL_A_128, HX711.CHANNEL_A_64, HX711.CHANNEL_B_32')
        else:
            self._channel = value

        if not self.is_ready():
            self._wait()

        for i in range(self.DATA_BITS):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)

        self._set_channel()

    def is_ready(self) -> bool:
        
        #Cuando los datos de salida no están listos para ser recuperados, el pin de salida digital DOUT está en alto.

        return self.d_out_pin.value() == 0

    def power_off(self):
        """
        Cuando el pin PD_SCK cambia de bajo a alto
        y permanece en alto por más de 60 us,
        el HX711 entra en modo de bajo consumo.
        """
        self.pd_sck_pin.value(0)
        self.pd_sck_pin.value(1)
        sleep_us(self.SLEEP_DELAY_USEC)

    def power_on(self):
        
        # Cuando el pin PD_SCK vuelve a bajo, el HX711 se reinicia y entra en modo de operación normal.

        self.pd_sck_pin.value(0)
        self.channel = self._channel

    def read(self, raw=False):
        """
        Lee el valor actual para el canal actual con la ganancia actual.
        Si raw es True, la salida del HX711 no se convertirá
        del formato de complemento a dos.
        """
        if not self.is_ready():
            self._wait()

        raw_data = 0
        for i in range(self.DATA_BITS):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)
            raw_data = raw_data << 1 | self.d_out_pin.value()
        self._set_channel()

        if raw:
            return raw_data
        else:
            return self._convert_from_twos_complement(raw_data)
