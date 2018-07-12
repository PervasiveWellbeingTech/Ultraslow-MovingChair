const int numOfActuators = 2;
const int relay1Pins[] = {5, 9};
const int relay2Pins[] = {6, 10};

void setup() { 
  //start serial connection
  Serial.begin(9600);

  for (int i = 0; i < numOfActuators; ++i) {
    // initialize each relay pin as an output
    pinMode(relay1Pins[i], OUTPUT);    
    pinMode(relay2Pins[i], OUTPUT);    
    
    // set the relay to low
    digitalWrite(relay1Pins[i], LOW); 
    digitalWrite(relay2Pins[i], LOW); 
  }
}

void moveWheelForward(int wheelNum) {
  digitalWrite(relay1Pins[wheelNum - 1], HIGH);
  digitalWrite(relay2Pins[wheelNum - 1], LOW);
}

void moveWheelBackward(int wheelNum) {
  digitalWrite(relay1Pins[wheelNum - 1], LOW);
  digitalWrite(relay2Pins[wheelNum - 1], HIGH);
}

void stopWheel(int wheelNum) {
  digitalWrite(relay1Pins[wheelNum - 1], LOW);
  digitalWrite(relay2Pins[wheelNum - 1], LOW);
}

void moveWheel(int wheelNum, int dir, int dutyCycle) {
  dutyCycle = max(dutyCycle, 0);
  dutyCycle = min(dutyCycle, 100);
  for (int i = 0; i < dutyCycle; ++i) {
    if (dir == 1) {
      moveWheelForward(wheelNum);
    } else {
      moveWheelBackward(wheelNum);
    }
  }

  for (int i = dutyCycle; i < 100; ++i) {
    stopWheel(wheelNum);
  }
}

void stopAll() {
  stopWheel(1);
  stopWheel(2);
}

void moveChair(int duration, int chairSpeed /* in percent */) {
  if (duration < 100) {
    duration = duration * 1000;
  }
  
  int startTime = millis();
  moveWheel(1, 1, chairSpeed);
  moveWheel(2, 1, chairSpeed);
  while(millis() <= startTime + duration) {
    // Wait
  }
  
  startTime = millis();
  moveWheel(1, 0, chairSpeed);
  moveWheel(2, 0, chairSpeed);
  while(millis() <= startTime + duration) {
    // Wait
  }
  
  stopAll();
}

void loop() {
//  takeSerialInput();
  moveChair(5, 100);
}

