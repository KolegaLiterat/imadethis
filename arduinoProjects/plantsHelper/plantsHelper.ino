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
  
byte sparkle[8] = {
  B00100100,
  B00100001,
  B01110000,
  B11111010,
  B01110010,
  B00100111,
  B10100010,
  B00001010,
  };

byte umbrella[8] = {
  B00111100,
  B01111110,
  B11111111,
  B11111111,
  B00001000,
  B00001000,
  B00101000,
  B00010000,
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
    int humidity = dht.readHumidity();
    
    if (check_humidity(humidity) == 1) {
      print_picture(cloud);
    } else if (check_humidity(humidity) == 2) {
      print_picture(sparkle);
    } else if (check_humidity(humidity) == 3) {
      print_picture(umbrella);
    }
    
    Serial.println("Humidity: ");
    Serial.println(humidity);

    Serial.println("Temperature: ");
    Serial.println(dht.readTemperature());

    clear_screens();
  }
}

int get_state()
{
  int switch_state = digitalRead(JOYSTICK_SWITCH);

  return switch_state;
}

int check_humidity(int humidity) {
  int state = 0;
  
  if (humidity < 50) {
    return state = 1;
  } else if (humidity >= 50 && humidity <= 60) {
    return state = 2;
  } else if (humidity > 60) {
    return state = 3;
  }
}

void print_picture(byte character [])
{ 
  for(int i = 0; i < 8; i++)
  {
    led_matrix.setRow(0, i, character[i]);
  }
}

void clear_screens()
{
  delay(1500);
  led_matrix.clearDisplay(0);
}
