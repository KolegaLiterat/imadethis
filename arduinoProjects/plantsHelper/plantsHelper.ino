#include <DHT.h>
#include <LedControl.h>

//JOYSTICK CONFIG START
/**
Unused config for axis changes in joystick
#define JOYSTICK_X A0
#define JOYSTICK_Y A1
**/
#define JOYSTICK_SWITCH 2
//JOYSTICK CONFIG END

//SENSOR CONFIG START
DHT dht(3, DHT11);
//SENSOR CONFIT END

//LED MATRIX CONFIG START
LedControl led_matrix = LedControl(12,10,11,0);

byte cloud[8] = {
  B00011100,
  B00111100,
  B01111110,
  B11111111,
  B11111111,
  B00000000,
  B01001001,
  B10010010,
  };
//LED MATRIX CONFIG STOP

void setup() {
  Serial.begin(9600);
  
  pinMode(JOYSTICK_SWITCH, INPUT_PULLUP);
  
  dht.begin();

  led_matrix.shutdown(0,false);
  led_matrix.setIntensity(0,15);
  led_matrix.clearDisplay(0);
}

void loop() {
  int joystick_state = get_state();

  if (joystick_state == 0) {
    Serial.println("Humidity: ");
    Serial.println(dht.readHumidity());

    Serial.println("Temperature: ");
    Serial.println(dht.readTemperature());

    print_picture(cloud);
    delay(1000);
    led_matrix.clearDisplay(0);
  }
}

int get_state()
{
  int switch_state = digitalRead(JOYSTICK_SWITCH);

  return switch_state;
}

void print_picture(byte character [])
{ 
  for(int i = 0; i < 8; i++)
  {
    led_matrix.setRow(0, i, character[i]);
  }
}
