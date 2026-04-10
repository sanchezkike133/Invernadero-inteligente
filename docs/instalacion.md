# Instalación del Sistema de Invernadero Inteligente

## Descripción

Este proyecto implementa un sistema de riego automático para un invernadero, utilizando Arduino para el control físico y Python para el procesamiento de datos.

---

## 1. Requisitos

### Hardware

* Arduino
* Sensor DHT11
* Sensor de humedad del suelo
* Módulo relevador
* Bomba de agua

### Software

* Arduino IDE
* Python 3.x
* LM Studio
* Git

---

## 2. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/invernadero-inteligente.git
cd invernadero-inteligente
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configuración del Arduino

1. Abrir Arduino IDE
2. Cargar el archivo:

```
arduino/riego_automatico.ino
```

3. Conectar el Arduino a la computadora
4. Verificar el puerto (por ejemplo: COM3)
5. Subir el código

---

## 5. Ejecución del servidor (Python)

Ejecutar el archivo:

```bash
python python/serve.py
```

Esto iniciará el servidor del sistema de invernadero.

---

## 6. Configuración de LM Studio

1. Abrir LM Studio
2. Configurar el archivo MCP ubicado en:

```
config/mcp.json
```

3. Verificar que la URL sea:

```
http://127.0.0.1:8000/mcp
```

---

## 7. Funcionamiento del sistema

1. El Arduino mide:

   * Temperatura
   * Humedad
   * Humedad del suelo

2. Envía los datos por puerto serial

3. Python recibe y procesa la información

4. El servidor expone herramientas mediante MCP

5. LM Studio consulta los datos del invernadero

---

## 8. Verificación

Si todo funciona correctamente:

* El Arduino enviará datos en formato JSON
* Python mostrará datos en consola
* LM Studio podrá consultar:

  * Estado del riego
  * Clima
  * Datos del sistema

---

## 9. Problemas comunes

### No hay datos

* Verificar conexión del Arduino
* Revisar puerto serial (COM)

### Error en Python

* Revisar dependencias instaladas
* Confirmar nombre del archivo `serve.py`

### LM Studio no conecta

* Verificar que el servidor esté corriendo
* Revisar URL MCP

---

## Resultado

Al finalizar, tendrás un sistema de invernadero capaz de:

* Regar automáticamente
* Monitorear condiciones ambientales
* Ser consultado desde LM Studio

---
