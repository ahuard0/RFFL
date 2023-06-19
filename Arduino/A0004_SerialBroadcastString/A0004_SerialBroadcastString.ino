unsigned long inc = 0;
const int ledPin = 13;
signed long r = 0;

void setup() {
  Serial.begin(9600);  // enable serial output
  pinMode(ledPin, OUTPUT);  // enable output on LED pin
  digitalWrite(ledPin, HIGH);

  for (int i=0; i<=13; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  for (int i=0; i<=13; i++) {
    r = random(2);
    if (r>0) {
      digitalWrite(i, HIGH);
    }
    else {
      digitalWrite(i, LOW);
    }
  }
  
  r = random(2);
  if (r>0) {
    digitalWrite(ledPin, HIGH);
  }
  else {
    digitalWrite(ledPin, LOW);
  }

  Serial.print("#");
  for (int i=0; i<13; i++) {
    Serial.print("|");
    Serial.print(digitalRead(i));
  }

  for (int i=0; i<6; i++) {
    Serial.print("|");
    Serial.print(analogRead(i));
  }
  Serial.println("");
  delay(100);
}
