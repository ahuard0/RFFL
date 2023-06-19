/*
 * SendBinaryFields
 * Sends digital and analog pin values as binary data
 *  This code can be used to send binary data to another Arduino or device.
 *  The output of this code will not be human readable.  It must be parsed byte-wise.
 */

const char HEADER = 'H'; // a single character header to indicate the start of a message

void setup() {
  Serial.begin(9600);
  for (int i=2; i<=13; i++) {
    pinMode(i, INPUT);
    digitalWrite(i, HIGH);
  }
}

void loop() {
  Serial.write(HEADER);  // send the header

  // put the bit values of the pins into an integer
  int values = 0;
  int bit = 0;

  for (int i=2; i<13; i++) {
    bitWrite(values, bit, digitalRead(i));  // set the bit to 0 or 1 depending on value of the given pin increment to the next bit
    bit = bit + 1;
  }
  sendBinary(values);

  for (int i=0; i<6; i++) {
    values = analogRead(i);
    sendBinary(values); // send the integer
  }
  delay(1000);
}

// function to send the given integer value to the serial port
void sendBinary(int value) {
  Serial.write(lowByte(value));  // send the low byte
  Serial.write(highByte(value));  // send the high byte
}
