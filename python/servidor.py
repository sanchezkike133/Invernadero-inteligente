# servidor_ia.py - Versión SUPER ROBUSTA
import asyncio
import json
import serial
import time
import requests
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import sys

PUERTO_ARDUINO = 'COM6'
BAUDRATE = 9600


estado_actual = {
    'temperatura': 22.6,
    'humedad': 53.0,
    'suelo': 700,
    'bomba': 'apagada',
    'estado_suelo': '💧 HÚMEDO',
    'ultima_decision_ia': 'Iniciando...',
    'razon_ia': 'Sistema iniciado',
    'timestamp': '',
    'conexion_ok': True
}

arduino = None
ultimo_dato_valido = {'suelo': 700, 'temperatura': 22.6, 'humedad': 53.0, 'bomba': 0}
intentos_reconexion = 0

def conectar_arduino():
    global arduino, intentos_reconexion
    try:
        if arduino and arduino.is_open:
            arduino.close()
        
        arduino = serial.Serial(PUERTO_ARDUINO, BAUDRATE, timeout=2)
        time.sleep(2)
        arduino.reset_input_buffer()
        arduino.write(b"auto\n")
        print(f"✅ Arduino conectado en {PUERTO_ARDUINO}")
        intentos_reconexion = 0
        return True
    except Exception as e:
        print(f"❌ Error conectando Arduino: {e}")
        intentos_reconexion += 1
        return False

def leer_datos_arduino():
    global arduino, ultimo_dato_valido, intentos_reconexion
    
    try:
        if arduino and arduino.in_waiting:
            # Leer todas las líneas disponibles
            lineas = []
            while arduino.in_waiting:
                try:
                    linea = arduino.readline().decode().strip()
                    if linea.startswith('{') and linea.endswith('}'):
                        lineas.append(linea)
                except:
                    pass
            
            # Usar la última línea válida
            if lineas:
                ultima_linea = lineas[-1]
                datos = json.loads(ultima_linea)
                
                suelo = datos.get('suelo', 0)
                temperatura = datos.get('temperatura', 0)
                humedad = datos.get('humedad', 0)
                bomba = datos.get('bomba', 0)
                
                # Validar datos (suelo entre 300-900 es normal)
                if 300 < suelo < 900 and 10 < temperatura < 40 and 30 < humedad < 90:
                    ultimo_dato_valido = datos
                    intentos_reconexion = 0
                    return datos
                else:
                    print(f"   ⚠️ Dato inválido: suelo={suelo}, usando último válido")
                    return ultimo_dato_valido
        else:
            # No hay datos disponibles, intentar reconectar
            if intentos_reconexion < 3:
                print("   ⚠️ Arduino no responde, reconectando...")
                conectar_arduino()
            return ultimo_dato_valido
            
    except Exception as e:
        print(f"   ❌ Error lectura: {e}")
        return ultimo_dato_valido

def enviar_comando_arduino(comando):
    global arduino
    try:
        if arduino and arduino.is_open:
            arduino.write(f"{comando}\n".encode())
            print(f"📤 {comando}")
            time.sleep(0.1)  # Pequeña pausa
            return True
    except:
        pass
    return False

def consultar_ia(suelo, temperatura, humedad, bomba_actual):
    print("   🤖 Consultando a GROQ...")
    
    prompt = f"""Decide si activar la bomba de riego.

Datos actuales:
- Sensor suelo: {suelo}
- Temperatura: {temperatura}°C
- Humedad ambiente: {humedad}%
- Estado bomba: {bomba_actual}

REGLAS:
- Suelo > 600 = HÚMEDO → DESACTIVAR bomba
- Suelo < 450 = SECO → ACTIVAR bomba  
- Entre 450-600 = MANTENER

RESPONDE EXACTAMENTE:
DECISION: [ACTIVAR o DESACTIVAR o MANTENER]
RAZON: [explicación corta]"""

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100
    }
    
    try:
        response = requests.post(GROQ_URL, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            respuesta = response.json()['choices'][0]['message']['content']
            decision = "MANTENER"
            razon = respuesta[:100]
            for linea in respuesta.split('\n'):
                if 'DECISION:' in linea:
                    decision = linea.split('DECISION:')[1].strip().upper()
            return decision, razon
    except Exception as e:
        print(f"   ❌ Error IA: {e}")
    return None, None

def decision_local(suelo):
    if suelo > 600:
        return "DESACTIVAR", f"Suelo HÚMEDO ({suelo})"
    elif suelo < 450:
        return "ACTIVAR", f"Suelo SECO ({suelo})"
    else:
        return "MANTENER", f"Suelo NORMAL ({suelo})"

async def ciclo_principal():
    global estado_actual
    
    while True:
        try:
            print(f"\n{'='*50}")
            print(f"🔄 Ciclo - {datetime.now().strftime('%H:%M:%S')}")
            
            # Leer Arduino
            datos = leer_datos_arduino()
            
            if datos:
                # Actualizar estado
                estado_actual['suelo'] = datos.get('suelo', 700)
                estado_actual['temperatura'] = datos.get('temperatura', 22.6)
                estado_actual['humedad'] = datos.get('humedad', 53.0)
                estado_actual['bomba'] = 'encendida' if datos.get('bomba', 0) == 1 else 'apagada'
                
                # Clasificar suelo
                suelo = estado_actual['suelo']
                if suelo > 600:
                    estado_actual['estado_suelo'] = "💧 HÚMEDO"
                elif suelo < 450:
                    estado_actual['estado_suelo'] = "🌵 SECO"
                else:
                    estado_actual['estado_suelo'] = "🌱 NORMAL"
                
                print(f"   📊 Suelo: {suelo} - {estado_actual['estado_suelo']}")
                print(f"   🌡️ Temp: {estado_actual['temperatura']}°C")
                print(f"   💧 Humedad: {estado_actual['humedad']}%")
                
                # Decisión IA o Local
                decision, razon = consultar_ia(suelo, estado_actual['temperatura'], 
                                               estado_actual['humedad'], estado_actual['bomba'])
                
                if decision is None:
                    decision, razon = decision_local(suelo)
                    print(f"   🧠 Usando decisión LOCAL")
                else:
                    print(f"   🤖 Usando decisión IA")
                
                estado_actual['ultima_decision_ia'] = decision
                estado_actual['razon_ia'] = razon
                estado_actual['timestamp'] = datetime.now().strftime('%H:%M:%S')
                
                print(f"   📝 Decisión: {decision}")
                print(f"   💬 Razón: {razon}")
                
                # Ejecutar comando
                if decision == "ACTIVAR" and estado_actual['bomba'] == 'apagada':
                    enviar_comando_arduino("bomba:ON")
                    estado_actual['bomba'] = 'encendida'
                elif decision == "DESACTIVAR" and estado_actual['bomba'] == 'encendida':
                    enviar_comando_arduino("bomba:OFF")
                    estado_actual['bomba'] = 'apagada'
            
        except Exception as e:
            print(f"❌ Error en ciclo principal: {e}")
        
        await asyncio.sleep(5)

class EstadoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/estado':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(estado_actual).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            suelo = estado_actual['suelo']
            suelo_color = "color: blue;" if suelo > 600 else "color: red;" if suelo < 450 else "color: green;"
            
            html = f"""
            <html>
            <head><title>Invernadero IA</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body {{ font-family: Arial; margin: 50px; text-align: center; background: #1a1a1a; color: white; }}
                .dato {{ font-size: 24px; margin: 20px; padding: 10px; background: #2a2a2a; border-radius: 10px; }}
                .seco {{ color: #ff6b6b; }}
                .humedo {{ color: #6b9fff; }}
                .normal {{ color: #6bff6b; }}
                .bomba-on {{ color: #ff4444; }}
                .bomba-off {{ color: #888888; }}
            </style>
            </head>
            <body>
                <h1>🤖 INVERNADERO INTELIGENTE CON IA</h1>
                <div class="dato">🌡️ Temperatura: {estado_actual['temperatura']}°C</div>
                <div class="dato">💧 Humedad: {estado_actual['humedad']}%</div>
                <div class="dato">🌱 Suelo: <span style="{suelo_color}">{estado_actual['suelo']} - {estado_actual['estado_suelo']}</span></div>
                <div class="dato">🚰 Bomba: <b class="{'bomba-on' if estado_actual['bomba']=='encendida' else 'bomba-off'}">{'🔴 ENCENDIDA' if estado_actual['bomba']=='encendida' else '⚪ APAGADA'}</b></div>
                <div class="dato">🤔 Decisión IA: <b>{estado_actual['ultima_decision_ia']}</b></div>
                <div class="dato">💡 Razón: {estado_actual['razon_ia']}</div>
                <hr>
                <p>🔄 Actualizado: {estado_actual['timestamp']}</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        pass

def iniciar_servidor_http():
    server = HTTPServer(('localhost', 8080), EstadoHandler)
    print("✅ Web: http://localhost:8080")
    server.serve_forever()

async def main():
    print("\n" + "=" * 60)
    print("   🤖 INVERNADERO INTELIGENTE - VERSIÓN ROBUSTA")
    print("=" * 60)
    
    print("\n📊 CONFIGURACIÓN:")
    print(f"   Puerto: {PUERTO_ARDUINO}")
    print(f"   Sensor: valores >600 = HÚMEDO | <450 = SECO")
    print(f"   IA: GROQ Mixtral")
    print("=" * 60)
    
    # Conectar Arduino
    conectar_arduino()
    
    # Iniciar servidor web
    http_thread = threading.Thread(target=iniciar_servidor_http, daemon=True)
    http_thread.start()
    
    print("\n✅ SISTEMA OPERATIVO")
    print("   Web: http://localhost:8080")
    print("   Cliente: python cliente.py")
    print("=" * 60 + "\n")
    
    await ciclo_principal()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido por el usuario")
        if arduino and arduino.is_open:
            arduino.close()
        sys.exit(0)