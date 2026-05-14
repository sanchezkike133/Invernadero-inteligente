import subprocess
import sys
import time
import os

print("=" * 50)
print("   🤖 INICIANDO INVERNADERO CON IA")
print("=" * 50)

# Cerrar procesos anteriores
os.system('taskkill /F /IM python.exe 2>nul')
time.sleep(2)

# Iniciar servidor con IA
print("📡 Iniciando servidor con IA...")
servidor = subprocess.Popen([sys.executable, "servidor_ia.py"])

print("⏳ Inicializando IA...")
for i in range(5):
    print(f"   [{i+1}/5]")
    time.sleep(1)

print("✅ Servidor IA listo!")

# Iniciar cliente
print("🖥️  Iniciando monitor...")
time.sleep(2)
cliente = subprocess.Popen([sys.executable, "cliente_ia.py"])

print("\n" + "=" * 50)
print("✅ SISTEMA CON IA OPERATIVO")
print("=" * 50)
print("🤖 La IA decide cuándo regar automáticamente")
print("📊 Evalúa el suelo cada 10 segundos")
print("🔴 Presiona CTRL+C para detener")
print("=" * 50 + "\n")

try:
    while True:
        time.sleep(1)
        if servidor.poll() is not None or cliente.poll() is not None:
            break
except KeyboardInterrupt:
    print("\n🛑 Deteniendo sistema IA...")
    servidor.terminate()
    cliente.terminate()
    time.sleep(2)
    os.system('taskkill /F /IM python.exe 2>nul')
    print("✅ Sistema IA detenido")