int digit[10] = {0b0111111, 0b0000110, 0b1011011, 0b1001111, 0b1100110, 0b1101101, 0b1111101, 0b0000111, 0b1111111, 0b1101111};
int digit1, digit2, code;
bool is_ready;

void setup() {
  is_ready = false;
  code = -1;

  for (int i = 2; i < 9; i++)
  {
    pinMode(i, OUTPUT);
  }
  pinMode(9, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(!is_ready){
    digitalWrite(9, LOW);
    delay(500);
    digitalWrite(9, HIGH);
    delay(500);
  }
  digitalWrite(9, LOW);
  if (code!= -1){
    is_ready=true;
    digitalWrite(9, HIGH);
    digit2 = code / 10;
    digit1 = code % 10;
    for (int k = 0; k < 20; k++)
    {
      digitalWrite(12, HIGH);
      digitalWrite(13, LOW);
      displayDigit(digit2);
      delay(10);
      digitalWrite(13, HIGH);
      digitalWrite(12, LOW);
      displayDigit(digit1);
      delay(10);
    }
    digitalWrite(12, HIGH);
    digitalWrite(13, HIGH);
    delay(50);
  }
  if (Serial.available() > 0){
    String msg = Serial.readString();
    if (msg[0] == '@') {
      String sub_msg = msg.substring(1);
      code = sub_msg.toInt();
    }
    else {
      is_ready = false;
      code = -1;
    }
  }
}

void displayDigit(int num) {
  for (int i = 2; i < 9; i++)
  {
    digitalWrite(i, bitRead(digit[num], i - 2));
  }

}
