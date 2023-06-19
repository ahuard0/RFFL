/*
 * SerialLoopbackString
 * Receives a string from the serial port, checks for a header and replaces it, 
 * then loops back the string data back onto the serial port.
 */

String inputString = "";      // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

void setup() {
  Serial.begin(9600);  // enable serial output
  inputString.reserve(200); // reserve 200 bytes for the inputString
}

void loop() {
  while (Serial.available()>0) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
      Serial.flush();
    }
  }

  if (stringComplete) {
    stringComplete = false;
    Serial.print("#|");
    Serial.println(inputString);
    inputString = "";
  }

  delay(50);
}

