# Arquitectura del Sistema

## Vista general

Arduino → Python → MCP → LM Studio

---

## Componentes

### Arduino

Captura datos del entorno y controla la bomba.

### Python

Actúa como intermediario entre hardware y software.

### MCP (FastMCP)

Convierte funciones en herramientas accesibles vía API.

### LM Studio

Cliente que consume las herramientas.

---

## Flujo detallado

1. Sensores detectan condiciones
2. Arduino procesa los datos
3. Envía datos en formato JSON
4. Python recibe datos por serial
5. MCP expone funciones
6. LM Studio consulta los datos

---

## Comunicación

* Arduino ↔ Python → Serial
* Python ↔ Cliente → HTTP (MCP)

---
