#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

#define SENSOR_SUELO A0
#define BOMBA 7

DHT dht(DHTPIN, DHTTYPE);

// 🔥 Límites de humedad (ajusta según tu sensor)
int seco = 700;
int humedo = 500;

bool regando = false;

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(BOMBA, OUTPUT);

  // 🔴 IMPORTANTE: relevador activo en LOW
  digitalWrite(BOMBA, HIGH); // bomba apagada al iniciar
}

void loop() {
  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();
  int suelo = analogRead(SENSOR_SUELO);

  // Validar DHT11
  if (isnan(humedad) || isnan(temperatura)) {
    Serial.println("{\"error\":\"DHT11 fallo\"}");
    delay(2000);
    return;
  }

  // 🌱 CONTROL INTELIGENTE CON HISTÉRESIS

  // 👉 Si está seco → encender bomba
  if (suelo > seco && !regando) {
    digitalWrite(BOMBA, LOW);  // 🔥 ENCENDER (activo en LOW)
    regando = true;
  }

  // 👉 Si ya está húmedo → apagar bomba
  if (suelo < humedo && regando) {
    digitalWrite(BOMBA, HIGH); // ❌ APAGAR
    regando = false;
  }

  // 📡 Enviar datos JSON
  Serial.print("{");
  Serial.print("\"temperatura\":");
  Serial.print(temperatura);
  Serial.print(",\"humedad\":");
  Serial.print(humedad);
  Serial.print(",\"suelo\":");
  Serial.print(suelo);
  Serial.print(",\"bomba\":");
  Serial.print(regando ? 1 : 0);
  Serial.println("}");

  delay(2000);
}
