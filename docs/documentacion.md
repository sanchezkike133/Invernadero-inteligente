<div align="center">

# GOBIERNO DEL ESTADO DE MÉXICO  

## UNIVERSIDAD MEXIQUENSE DEL BICENTENARIO  
### UNIDAD DE ESTUDIOS SUPERIORES  
### SAN JOSÉ DEL RINCÓN  


---

**ABRIL DE 2026**

</div>


# Documentación del Sistema de Invernadero Inteligente

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

## 3. Módulos del sistema

### 3.1 Arduino

Funciones:

* Lectura de sensores
* Control de la bomba
* Envío de datos en formato JSON

---

### 3.2 Servidor Python

Funciones:

* Lectura del puerto serial
* Procesamiento de datos
* Exposición de herramientas (API)

---

### 3.3 Cliente (LM Studio)

Funciones:

* Consumir datos del sistema
* Consultar estado del riego
* Obtener clima

---

## 4. Flujo del sistema

1. Arduino lee sensores
2. Envía datos por Serial en JSON
3. Python recibe los datos
4. FastMCP expone herramientas
5. LM Studio consulta la información

---

## 5.Lógica de riego

El sistema usa histéresis:

* Si el suelo está seco → activa la bomba
* Si está húmedo → la apaga

Esto evita activaciones constantes.

---

## 6.Ejemplo de datos

```json
{
  "temperatura": 25,
  "humedad": 60,
  "suelo": 650,
  "bomba": 1
}
```

---

## 7.Consideraciones

* Ajustar valores del sensor de suelo
* Verificar puerto serial (COM)
* Mantener misma velocidad de comunicación (9600)

---
