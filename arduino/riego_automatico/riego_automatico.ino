#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

#define SENSOR_SUELO A0
#define BOMBA 7

DHT dht(DHTPIN, DHTTYPE);

int seco = 650;
int humedo = 400;

bool regando = false;
bool modoManual = false;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(BOMBA, OUTPUT);
  digitalWrite(BOMBA, HIGH); // Bomba apagada al inicio
}

void loop() {
  // =========================
  // COMANDOS DESDE PYTHON
  // =========================
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    if (comando == "bomba:ON") {
      digitalWrite(BOMBA, LOW);   // Enciende bomba (LOW activa relé)
      regando = true;
      modoManual = true;
      Serial.println("{\"bomba\":1,\"modo\":\"manual\",\"accion\":\"ON\"}");
    }
    else if (comando == "bomba:OFF") {
      digitalWrite(BOMBA, HIGH);  // Apaga bomba
      regando = false;
      modoManual = true;
      Serial.println("{\"bomba\":0,\"modo\":\"manual\",\"accion\":\"OFF\"}");
    }
    else if (comando == "auto") {
      modoManual = false;
      Serial.println("{\"modo\":\"automatico\",\"accion\":\"AUTO\"}");
    }
  }

  // =========================
  // LECTURA DE SENSORES
  // =========================
  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();
  int suelo = analogRead(SENSOR_SUELO);

  if (isnan(humedad) || isnan(temperatura)) {
    // Si hay error, solo envía datos del suelo y bomba
    Serial.print("{\"temperatura\":0,\"humedad\":0,\"suelo\":");
    Serial.print(suelo);
    Serial.print(",\"bomba\":");
    Serial.print(regando ? 1 : 0);
    Serial.println("}");
    delay(2000);
    return;
  }

  // =========================
  // CONTROL AUTOMÁTICO
  // =========================
  if (!modoManual) {
    if (suelo > seco && !regando) {
      digitalWrite(BOMBA, LOW);
      regando = true;
    }
    else if (suelo < humedo && regando) {
      digitalWrite(BOMBA, HIGH);
      regando = false;
    }
  }

  // =========================
  // ENVÍO DE DATOS (SIEMPRE CON EL ESTADO ACTUAL DE LA BOMBA)
  // =========================
  Serial.print("{");
  Serial.print("\"temperatura\":");
  Serial.print(temperatura);
  Serial.print(",\"humedad\":");
  Serial.print(humedad);
  Serial.print(",\"suelo\":");
  Serial.print(suelo);
  Serial.print(",\"bomba\":");
  Serial.print(regando ? 1 : 0);  // ¡IMPORTANTE! Usar la variable regando
  Serial.println("}");

  delay(2000);
}