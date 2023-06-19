/*
 * SerialBroadcastCount
 * Transmits pin data and the current sample count iteration.
 *
 */

const int ledPin = 13;
bool initialized = false;
int count = 0;
bool statePin13 = false;

void setup() {
  Serial.begin(9600);  // enable serial output

  pinMode(ledPin, OUTPUT);  // enable output on LED pin
  digitalWrite(ledPin, LOW);  // set LED initial state to OFF

  for (int i=0; i<=13; i++) {  // Setup digital pins as outputs
    pinMode(i, OUTPUT);
  }
}

void loop() {
  if (!initialized) {  // Initialize the digital outputs to the LOW state.
    for (int i=0; i<13; i++) {
      digitalWrite(i, LOW);
    }
    initialized = true;
  }

  if (statePin13 == true) {
    statePin13 = false;
    digitalWrite(ledPin, LOW);
  }
  else {
    statePin13 = true;
    digitalWrite(ledPin, HIGH);
  }

  broadcastPinData();

  delay(500);  // Necessary to avoid lag


}

// Reads the digital and analog pin values and outputs to the serial buffer
void broadcastPinData() {
  count++;
  Serial.print("#");
  Serial.print("|");
  Serial.print(count);
  for (int i=0; i<=13; i++) {
    Serial.print("|");
    Serial.print(digitalRead(i));
  }

  for (int i=0; i<6; i++) {
    Serial.print("|");
    Serial.print(analogRead(i));
  }
  Serial.println("");
}
