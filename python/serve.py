from fastmcp import FastMCP
import serial
import json
import time

mcp = FastMCP("invernadero")

# Conexión con Arduino
arduino = serial.Serial("COM6", 9600, timeout=2)
time.sleep(2)
arduino.reset_input_buffer()

data_cache = None


def leer_serial():
    global data_cache
    try:
        linea = arduino.readline().decode("utf-8").strip()
        print("DEBUG RAW:", linea)

        if linea.startswith("{") and linea.endswith("}"):
            data = json.loads(linea)
            print("DEBUG JSON:", data)
            data_cache = data
            return data

    except Exception as e:
        print("Error:", e)

    return data_cache


# 🔹 TOOL 1: Obtener todos los datos
@mcp.tool()
def obtener_datos():
    """
    Obtiene todos los datos del Arduino incluyendo:
    - humedad del suelo (suelo)
    - temperatura
    - humedad ambiental
    - estado de la bomba (bomba: 0 apagada, 1 encendida)
    """
    data = leer_serial()

    if data:
        return {
            "status": "ok",
            "datos": data
        }

    return {
        "status": "error",
        "mensaje": "No se reciben datos del Arduino"
    }


# 🔹 TOOL 2: Estado del riego
@mcp.tool()
def estado_riego():
    """
    Analiza la humedad del suelo y determina si se necesita riego.
    """
    data = leer_serial()

    if not data or "suelo" not in data:
        return {"status": "error", "mensaje": "Sin datos"}

    suelo = data["suelo"]

    if suelo > 650:
        return {"estado": "seco", "accion": "regar"}
    else:
        return {"estado": "humedo", "accion": "no regar"}


# 🔹 TOOL 3: Clima
@mcp.tool()
def clima():
    """
    Devuelve la temperatura y humedad ambiental del invernadero.
    """
    data = leer_serial()

    if not data:
        return {"status": "error", "mensaje": "Sin datos"}

    return {
        "temperatura": data.get("temperatura", 0),
        "humedad": data.get("humedad", 0)
    }


# 🔹 TOOL 4: Estado del robot (MEJORADO)
@mcp.tool()
def estado_robot():
    """
    Indica el estado general del robot, incluyendo:
    conexión, temperatura, humedad, estado del suelo y bomba de riego.
    """
    data = leer_serial()

    if not data:
        return {
            "estado": "desconectado"
        }

    # 🔹 Interpretación de bomba
    bomba_estado = data.get("bomba", None)

    if bomba_estado == 1:
        bomba = "encendida"
    elif bomba_estado == 0:
        bomba = "apagada"
    else:
        bomba = "desconocido"

    # 🔹 Interpretación del suelo
    suelo_valor = data.get("suelo", 0)

    if suelo_valor > 650:
        estado_suelo = "seco"
    elif suelo_valor > 300:
        estado_suelo = "normal"
    else:
        estado_suelo = "muy humedo"

    return {
        "estado": "conectado",
        "temperatura": data.get("temperatura"),
        "humedad": data.get("humedad"),
        "suelo_valor": suelo_valor,
        "estado_suelo": estado_suelo,
        "bomba": bomba
    }


# 🔹 TOOL 5: Humedad del suelo
@mcp.tool()
def humedad_suelo():
    """
    Devuelve el valor actual de la humedad del suelo.
    """
    data = leer_serial()

    if not data or "suelo" not in data:
        return {"status": "error", "mensaje": "Sin datos"}

    return {
        "suelo": data["suelo"]
    }


# Ejecutar servidor
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)