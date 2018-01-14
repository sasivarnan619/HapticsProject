void setup() {
Serial.begin(9600); // set the baud rate
pinMode(6, OUTPUT);
pinMode(9, OUTPUT);
pinMode(10, OUTPUT);
pinMode(11, OUTPUT);
Serial.println("Ready"); // print "Ready" once
}
int frame_count = 0;
void loop() {
if(Serial.available()){ // only send data back if data has been sent
frame_count = Serial.read(); // read the incoming data
Serial.println(frame_count); // send the data back in a new line so that it is not all one long line
if(frame_count % 15 == 0){
  Serial.println ("hi");
  analogWrite(6, 255);
  analogWrite(9, 255);
  analogWrite(10, 255);
  analogWrite(11, 100);
}
else if(frame_count % 15 <=5 && frame_count % 15 >0){
  Serial.println ("i am top 5");
  analogWrite(6, 255);
  analogWrite(9, 255);
  analogWrite(10, 255);
  analogWrite(11, 100);
}
else if(frame_count % 15 > 5 && frame_count % 15 <=10){
  Serial.println ("i am top 10");
  analogWrite(6, 255);
  analogWrite(9, 255);
  analogWrite(10, 100);
  analogWrite(11, 100);
}
else if((frame_count % 15 > 10 && frame_count % 15 < 15) || frame_count == 0){
  Serial.println ("i am top 15");
  analogWrite(6, 255);
  analogWrite(9, 100);
  analogWrite(10, 100);
  analogWrite(11, 100);
}
}
//delay(100); // delay for 1/10 of a second
}
