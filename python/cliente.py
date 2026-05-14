# cliente.py - Versión robusta
import requests
import os
import time
from datetime import datetime

URL_ESTADO = "http://localhost:8080/estado"

def main():
    print("\n" + "=" * 60)
    print("   📱 MONITOR DEL INVERNADERO IA")
    print("=" * 60)
    
    while True:
        try:
            response = requests.get(URL_ESTADO, timeout=3)
            if response.status_code == 200:
                estado = response.json()
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n" + "=" * 60)
                print("     🤖 INVERNADERO INTELIGENTE (IA) 🤖")
                print("=" * 60)
                print(f"📅 {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 60)
                print(f"🌡️  Temperatura: {estado.get('temperatura', 0)}°C")
                print(f"💧  Humedad: {estado.get('humedad', 0)}%")
                print(f"🌱  Suelo: {estado.get('suelo', 0)} - {estado.get('estado_suelo', '?')}")
                
                bomba = estado.get('bomba', 'apagada')
                if bomba == "encendida":
                    print(f"🚰  Bomba: 🔴 ENCENDIDA")
                else:
                    print(f"🚰  Bomba: ⚪ APAGADA")
                
                print("-" * 60)
                print("🤔 ÚLTIMA DECISIÓN DE LA IA:")
                print(f"   🎯 Acción: {estado.get('ultima_decision_ia', '...')}")
                print(f"   💡 Razón: {estado.get('razon_ia', '...')}")
                print(f"   ⏱️  Hora: {estado.get('timestamp', '...')}")
                print("-" * 60)
                print("🔄 Actualizando cada 2 segundos...")
                print("🌐 Web: http://localhost:8080")
                print("=" * 60)
            else:
                print("⚠️ Servidor no responde...")
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar al servidor")
            print("   ¿El servidor está corriendo?")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    main()