/*
 * CommandAndControlData
 * Receives commands over the serial port and transmits back data when requested.
 *
 *    Commands:
 *      _SINGLE_READ : Read a Single Sample, returns 13 digital pins and 6 analog pin values
 *      _BROADCAST : Begins streaming read data consisting of 13 digital pins and 6 analog pin values
 *        _BROADCAST_ON : LED (Pin 13) will activate indicating streaming is active
 *        _BROADCAST_OFF : Disable streaming
 *      _D : Turn On/Off Digital Outputs: ON->Logic High (1), OFF->Logic Low (0)
 *        _D0_ON / _D0_OFF
 *        _D1_ON / _D1_OFF
 *        ...
 *        _D13_ON / D13_OFF
 */

String inputString = "";      // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

bool broadcastDataPins = false;
const int ledPin = 13;
String receiveData = "";
signed long r = 0;
bool initialized = false;

void setup() {
  Serial.begin(9600);  // enable serial output
  inputString.reserve(200); // reserve 200 bytes for the inputString buffer

  pinMode(ledPin, OUTPUT);  // enable output on LED pin
  digitalWrite(ledPin, LOW);  // set LED initial state to OFF

  for (int i=0; i<=13; i++) {  // Setup digital pins as outputs
    pinMode(i, OUTPUT);
  }
}

void loop() {
  while (Serial.available()>0) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    if (inChar != -1)
      inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
      Serial.flush();
    }
    delay(5);
  }

  if (stringComplete) {  // Called when a command is received
    stringComplete = false;  // Reset for receiving the next command
    processRead();  // Read the command
    inputString = "";  // Reset the buffer
  }

  if (!initialized) {  // Initialize the digital outputs to the LOW state.
    for (int i=0; i<13; i++) {
      digitalWrite(i, LOW);
    }
    initialized = true;
  }

  if (broadcastDataPins) {  // Broadcasting, if enabled
    broadcastPinData();
  }

  delay(50);  // Necessary to avoid lag
}

void processRead() {
  inputString.trim(); // remove any \r \n whitespace at the end of the String
  // Check for Header
  if(inputString.charAt(0)=='$' && inputString.charAt(1)=='|') {  // Header Originated at Host ($)
    receiveData = inputString.substring(2, (int)inputString.length());
    if (receiveData.compareTo("_BROADCAST_ON")==0) {
      broadcastDataPins = true;
      digitalWrite(ledPin, HIGH);
    }
    else if (receiveData.compareTo("_BROADCAST_OFF")==0) {
      broadcastDataPins = false;
      digitalWrite(ledPin, LOW);
    }
    else if (receiveData.compareTo("_SINGLE_READ")==0) {
      broadcastPinData();
    }
    else if (receiveData.compareTo("_D0_ON")==0) {
      digitalWrite(0, HIGH);
    }
    else if (receiveData.compareTo("_D0_OFF")==0) {
      digitalWrite(0, LOW);
    }
    else if (receiveData.compareTo("_D1_ON")==0) {
      digitalWrite(1, HIGH);
    }
    else if (receiveData.compareTo("_D1_OFF")==0) {
      digitalWrite(1, LOW);
    }
    else if (receiveData.compareTo("_D2_ON")==0) {
      digitalWrite(2, HIGH);
    }
    else if (receiveData.compareTo("_D2_OFF")==0) {
      digitalWrite(2, LOW);
    }
    else if (receiveData.compareTo("_D3_ON")==0) {
      digitalWrite(3, HIGH);
    }
    else if (receiveData.compareTo("_D3_OFF")==0) {
      digitalWrite(3, LOW);
    }
    else if (receiveData.compareTo("_D4_ON")==0) {
      digitalWrite(4, HIGH);
    }
    else if (receiveData.compareTo("_D4_OFF")==0) {
      digitalWrite(4, LOW);
    }
    else if (receiveData.compareTo("_D5_ON")==0) {
      digitalWrite(5, HIGH);
    }
    else if (receiveData.compareTo("_D5_OFF")==0) {
      digitalWrite(5, LOW);
    }
    else if (receiveData.compareTo("_D6_ON")==0) {
      digitalWrite(6, HIGH);
    }
    else if (receiveData.compareTo("_D6_OFF")==0) {
      digitalWrite(6, LOW);
    }
    else if (receiveData.compareTo("_D7_ON")==0) {
      digitalWrite(7, HIGH);
    }
    else if (receiveData.compareTo("_D7_OFF")==0) {
      digitalWrite(7, LOW);
    }
    else if (receiveData.compareTo("_D8_ON")==0) {
      digitalWrite(8, HIGH);
    }
    else if (receiveData.compareTo("_D8_OFF")==0) {
      digitalWrite(8, LOW);
    }
    else if (receiveData.compareTo("_D9_ON")==0) {
      digitalWrite(9, HIGH);
    }
    else if (receiveData.compareTo("_D9_OFF")==0) {
      digitalWrite(9, LOW);
    }
    else if (receiveData.compareTo("_D10_ON")==0) {
      digitalWrite(10, HIGH);
    }
    else if (receiveData.compareTo("_D10_OFF")==0) {
      digitalWrite(10, LOW);
    }
    else if (receiveData.compareTo("_D11_ON")==0) {
      digitalWrite(11, HIGH);
    }
    else if (receiveData.compareTo("_D11_OFF")==0) {
      digitalWrite(11, LOW);
    }
    else if (receiveData.compareTo("_D12_ON")==0) {
      digitalWrite(12, HIGH);
    }
    else if (receiveData.compareTo("_D12_OFF")==0) {
      digitalWrite(12, LOW);
    }
    else if (receiveData.compareTo("_D13_ON")==0) {
      digitalWrite(13, HIGH);
    }
    else if (receiveData.compareTo("_D13_OFF")==0) {
      digitalWrite(13, LOW);
    }
  }
}

// Reads the digital and analog pin values and outputs to the serial buffer
void broadcastPinData() {
  Serial.print("#");
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
