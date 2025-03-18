long randNumber;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop() {
  randNumber = random(0, 10);
  Serial.println(randNumber);
  delay(1000);
}