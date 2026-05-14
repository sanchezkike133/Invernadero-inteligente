# monitoreo_estabilidad.py
import serial
import time

arduino = serial.Serial('COM6', 9600, timeout=2)
time.sleep(2)

print("📊 MONITOREO DE ESTABILIDAD (30 segundos)")
print("=" * 50)

for i in range(30):
    arduino.write(b"estado\n")
    time.sleep(0.3)
    if arduino.in_waiting:
        linea = arduino.readline().decode().strip()
        print(f"{i+1:2d}: {linea}")
    time.sleep(1)

arduino.close()