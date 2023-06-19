unsigned long inc = 0;
const int ledPin = 13;

void setup() {
  Serial.begin(9600);  // enable serial output
  pinMode(ledPin, OUTPUT);  // enable output on LED pin
  digitalWrite(ledPin, HIGH);
}

void loop() {
  Serial.print("Increment: ");
  Serial.println(inc);
  inc++;
  delay(100);
}
