#include <DHT.h>

//JOYSTICK CONFIG START
/**
Unused config for axis changes in joystick
#define JOYSTICK_X A0
#define JOYSTICK_Y A1
**/
#define JOYSTICK_SWITCH 2
//JOYSTICK CONFIG END

//SENSOR CONFIG START
DHT dht(3, DHT22);
//SENSOR CONFIT END

void setup() {
  Serial.begin(9600);
  pinMode(JOYSTICK_SWITCH, INPUT_PULLUP);
  dht.begin();
}

void loop() {
  int joystick_state = get_state();;

  if (joystick_state == 0) {
    Serial.println("Humidity: ");
    Serial.println(dht.readHumidity());

    Serial.println("Temperature: ");
    Serial.println(dht.readTemperature());
  }
}

int get_state()
{
  int switch_state = digitalRead(JOYSTICK_SWITCH);

  return switch_state;
}
