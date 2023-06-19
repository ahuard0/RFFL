/*
 * SerialLoopbackString
 * Receives a string from the serial port, checks for a header and replaces it, 
 * then loops back the string data back onto the serial port.
 */

String inputString = "";      // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

const int ledPin = 13;
String receiveData = "";

void setup() {
  Serial.begin(9600);  // enable serial output
  inputString.reserve(200); // reserve 200 bytes for the inputString:

  pinMode(ledPin, OUTPUT);  // enable output on LED pin
  digitalWrite(ledPin, LOW);

  for (int i=0; i<=13; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  while (Serial.available()>0) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
      Serial.flush();
    }
  }

  if (stringComplete) {
    stringComplete = false;
    processRead();
    inputString = "";
  }

  delay(50);
}

void processRead() {
  inputString.trim(); // remove any \r \n whitespace at the end of the String
  // Check for Header
  if(inputString.charAt(0)=='$' && inputString.charAt(1)=='|') {  // Header Originated at Host ($)
    receiveData = inputString.substring(2, (int)inputString.length());
    if (receiveData.compareTo("_LED_ON")==0) {
      digitalWrite(ledPin, HIGH);
    }
    else if (receiveData.compareTo("_LED_OFF")==0) {
      digitalWrite(ledPin, LOW);
    }
    else if (receiveData.compareTo("_LOOPBACK")==0) {
      Serial.println("This is a loopback test.");
    }
  }
}
