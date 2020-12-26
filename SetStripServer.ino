#include <WiFi.h>
#include <Adafruit_NeoPixel.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>

#define NUM_LEDS 60 
#define PIN 27
const char* ssid = "gigacube-CA1D";
const char* password = "rE8NgMm9L6Ai9hQG"; 
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);
WebServer server(80);

void setPixels(){
  int numberOfPixels=0;
  int red=255;
  int green=255;
  int blue=255;
  if (server.arg("total")!="")
    numberOfPixels=server.arg("total").toInt();
  if (server.arg("r")!="")
    red=server.arg("r").toInt();
  if (server.arg("g")!="")
    green=server.arg("g").toInt();  
  if (server.arg("b")!="")
    blue=server.arg("b").toInt();
  for (int i =0;i<numberOfPixels;i++){
       strip.setPixelColor(29-i,red,green,blue,50);
       strip.setPixelColor(30+i,red,green,blue,50);//  Set pixel's color (in RAM)
       strip.show();
       delay(8);
    }
  strip.clear();
  strip.show();
  server.send(200, "text/plain", "ok");
}

void theaterChaseRainbow() {
  int firstPixelHue = 0;     // First pixel starts at red (hue 0)
  for(int a=0; a<30; a++) {  // Repeat 30 times...
    for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      for(int c=b; c<strip.numPixels(); c += 3) {
        int      hue   = firstPixelHue + c * 65536L / strip.numPixels();
        uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show();
      delay(.25);               
      firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
    }
  }
  server.send(200, "text/plain", "ok");
}
void handleRoot() {
  String message="Commands: rainbow,setStrip";
  server.send(200, "text/plain", message);
}

void setup() {
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(50);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }
  server.on("/", handleRoot);
  server.on("/setStrip", setPixels);
  server.on("/rainbow", theaterChaseRainbow);
  server.begin();
}


void loop() {
  server.handleClient();
}
