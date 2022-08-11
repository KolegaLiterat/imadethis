/**
Unused config for axis changes in joystick
#define JOYSTICK_X A0
#define JOYSTICK_Y A1
**/
#define JOYSTICK_SWITCH 2

void setup() {
  Serial.begin(9600);
  pinMode(JOYSTICK_SWITCH, INPUT_PULLUP);

}

void loop() {
  int joystick_state = get_state();

  if (joystick_state == 0) {
    Serial.println("Change!");
  }
}

int get_state()
{
  int switch_state = digitalRead(JOYSTICK_SWITCH);

  return switch_state;
}
