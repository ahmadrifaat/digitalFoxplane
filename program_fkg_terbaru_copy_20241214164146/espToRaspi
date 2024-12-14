#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Konfigurasi WiFi
const char* ssid = "Ygini";
const char* password = "dipakeji";

// Konfigurasi server
const char* host = "192.168.221.167"; // Ganti dengan IP Raspberry Pi
const uint16_t port = 8080;

// Objek MPU6050
Adafruit_MPU6050 mpu1;
Adafruit_MPU6050 mpu2;

void setup() {
  Serial.begin(9600);

  // Koneksi WiFi
  Serial.println("Menghubungkan ke WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi terhubung.");
  Serial.print("Alamat IP: ");
  Serial.println(WiFi.localIP());

  // Inisialisasi MPU6050 pertama
  if (!mpu1.begin(0x68)) {
    Serial.println("MPU6050 #1 tidak ditemukan!");
    while (1);
  }
  Serial.println("MPU6050 #1 terdeteksi.");

  // Inisialisasi MPU6050 kedua
  if (!mpu2.begin(0x69)) {
    Serial.println("MPU6050 #2 tidak ditemukan!");
    while (1);
  }
  Serial.println("MPU6050 #2 terdeteksi.");
}

void loop() {
  // Membuat objek WiFiClient
  WiFiClient client;

  // Menghubungkan ke server
  if (!client.connect(host, port)) {
    Serial.println("Gagal terhubung ke server.");
    delay(1000);
    return;
  }

  // Membaca data dari MPU6050 pertama
  sensors_event_t a1, g1, temp1;
  mpu1.getEvent(&a1, &g1, &temp1);

  float ax1 = a1.acceleration.x;
  float ay1 = a1.acceleration.y;

  // Membaca data dari MPU6050 kedua
  sensors_event_t a2, g2, temp2;
  mpu2.getEvent(&a2, &g2, &temp2);

  float ax2 = a2.acceleration.x;
  float ay2 = a2.acceleration.y;

  // Mengirim data kedua sensor secara bersamaan
  String jsonPayload = "{\"sensor1\":{\"ax\":" + String(ax1, 2) + ", \"ay\":" + String(ay1, 2) + "}, "
                       "\"sensor2\":{\"ax\":" + String(ax2, 2) + ", \"ay\":" + String(ay2, 2) + "}}\n";

  client.print(jsonPayload);

  // Tutup koneksi
  client.stop();

  delay(500); // Delay untuk stabilitas
}
