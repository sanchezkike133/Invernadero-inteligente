<div align="center">

# GOBIERNO DEL ESTADO DE MÉXICO  

## UNIVERSIDAD MEXIQUENSE DEL BICENTENARIO  
### UNIDAD DE ESTUDIOS SUPERIORES  
### SAN JOSÉ DEL RINCÓN  

---

**ABRIL DE 2026**

</div>


# Documentación del Sistema de Invernadero Inteligente

---

## 1. Descripción general

Este sistema automatiza el riego de plantas utilizando sensores y control inteligente.

Permite monitorear:

* Temperatura
* Humedad ambiental
* Humedad del suelo

Y activar automáticamente una bomba de agua.

---

## 2. Componentes

### Hardware

* Arduino
* Sensor DHT11
* Sensor de humedad del suelo
* Módulo relevador
* Bomba de agua

### Software

* Python
* FastMCP
* Comunicación Serial

---

## 3. Conexiones del sistema

### Sensor DHT11 (Temperatura y humedad del aire)
- VCC → 5V de Arduino  
- GND → GND de Arduino  
- DATA → Pin digital D2  

---

### Sensor de humedad de suelo
- VCC → 5V de Arduino  
- GND → GND de Arduino  
- AO (Salida analógica) → Pin A0  

---

### Módulo de relé (bomba de agua)
- VCC → 5V de Arduino  
- GND → GND de Arduino  
- IN → Pin digital D7  

---

### Bomba de agua (alimentación externa)
- COM → Positivo de la fuente de la bomba  
- NO (Normally Open) → Positivo de la bomba  
- Negativo de la bomba → Directo a la fuente de alimentación  

---

## Importante
- El relé trabaja en modo **activo en LOW**
- La bomba debe usar **fuente externa (no Arduino)**
- Todas las tierras (GND) deben estar en común

---

## Resumen de pines

| Componente              | Pin Arduino |
|------------------------|------------|
| DHT11 DATA             | D2         |
| Sensor de suelo (AO)   | A0         |
| Relé (bomba)           | D7         |


![Diagrama](/images/img1.jpeg)

---

## 4. Módulos del sistema

### 4.1 Arduino

Funciones:

* Lectura de sensores
* Control de la bomba
* Envío de datos en formato JSON

---

### 4.2 Servidor Python

Funciones:

* Lectura del puerto serial
* Procesamiento de datos
* Exposición de herramientas (API)

---

### 4.3 Cliente (LM Studio)

Funciones:

* Consumir datos del sistema
* Consultar estado del riego
* Obtener clima

---

## 5. Flujo del sistema

1. Arduino lee sensores
2. Envía datos por Serial en JSON
3. Python recibe los datos
4. FastMCP expone herramientas
5. LM Studio consulta la información

---

## 6. Lógica de riego

El sistema usa histéresis:

* Si el suelo está seco → activa la bomba
* Si está húmedo → la apaga

Esto evita activaciones constantes.

---

## 7. Ejemplo de datos

```json
{
  "temperatura": 25,
  "humedad": 60,
  "suelo": 650,
  "bomba": 1
}