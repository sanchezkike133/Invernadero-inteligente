# Invernadero Inteligente

Sistema de riego automático para un invernadero utilizando Arduino, Python y MCP.

---

## Descripción

Este proyecto permite monitorear condiciones ambientales y activar automáticamente el riego según la humedad del suelo.

El sistema integra:

* Arduino (sensores y control de bomba)
* Python (procesamiento de datos)
* MCP (exposición de herramientas)
* LM Studio (cliente)
* Modelo de IA local (Qwen3 1.7B)

---

## Integración de Inteligencia Artificial

Este proyecto utiliza el modelo **Qwen3 1.7B** ejecutado de forma local para procesamiento inteligente y automatización.

### Características del modelo

- Parámetros: 1.7B  
- Tamaño: ~1.67 GB  
- Contexto: hasta 32k tokens  
- Compatible con CPU  
- Soporte multilenguaje  

---

## Análisis del equipo

El sistema fue diseñado considerando el siguiente hardware:

- **Equipo:** Acer Aspire A515-57  
- **Procesador:** Intel Core i5-1235U (12ª generación)  
- **Núcleos / Hilos:** 10 / 12  
- **RAM:** 8 GB  
- **GPU:** Integrada (Intel Iris Xe)  

---

## ¿Por qué se usa Qwen3 1.7B?

### 🔹 Tamaño ligero
Permite ejecutarse en equipos con recursos limitados.

### 🔹 Compatible con CPU
No requiere tarjeta gráfica dedicada.

### 🔹 Uso eficiente de memoria
Funciona entre 2 y 4 GB de RAM.

### 🔹 Buen rendimiento
Adecuado para:
- Automatización
- Procesamiento de datos
- Comunicación con el sistema

---

## Limitaciones

- RAM limitada (8 GB)
- Posible saturación si hay muchos programas abiertos
- Sin GPU dedicada

---

## Recomendaciones

- Cerrar aplicaciones innecesarias antes de ejecutar el modelo
- Mantener al menos 3 GB de RAM libres
- Considerar ampliar a 16 GB de RAM

---

## Tecnologías utilizadas

* Arduino IDE
* Python
* FastMCP
* Comunicación Serial
* LM Studio
* Modelos de IA local

---

## Estructura del proyecto

* `arduino/` → Código del Arduino  
* `python/` → Servidor (`serve.py`)  
* `config/` → Configuración MCP (`mcp.json`)  
* `docs/` → Documentación  

---

## Ejecución

### 1. Subir código al Arduino

Abrir Arduino IDE y cargar:
