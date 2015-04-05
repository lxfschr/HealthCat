#include <SoftwareSerial.h>
#include <Servo.h> 

//Servo
int pos = 0;
Servo bowlServo;
Servo feedServo;

//Scale
int scalePin = 0;

//load scale variables
float loadA = .453592; // kg
int analogvalA = 527.02; // analog reading taken with load A on the load cell
float loadB = .907185; // kg
int analogvalB = 715.12; // analog reading taken with load B on the load cell
float analogValueAverage = 0;
long time = 0; //
int timeBetweenReadings = 200; // We want a reading every 200 ms;

//RFID variables
const char command_scan[]={
  0x43,0x04,0x01,0xcd};//scan for IDs
const char command_powerOff[]={
  0x18,0x03,0x00};//power off antenna
const char command_powerOn[]={
  0x18,0x03,0xFF};//power on antenna
unsigned char  incomingByte;
SoftwareSerial Serial1 = SoftwareSerial(2,3);

void setup(){
  Serial.begin(4800);
  Serial1.begin(9600);
  Serial1.write(command_powerOn);
  feedServo.attach(5);
  feedServo.write(120);
  delay(2000);
  feedServo.detach();


}

void loop() 
{
    int analogValue = analogRead(0);

  // running average - We smooth the readings a little bit
  analogValueAverage = 0.99*analogValueAverage + 0.01*analogValue;
  float load;
  // Is it time to print?
  if(millis() > time + timeBetweenReadings){
    float load = (((analogToLoad(analogValueAverage)+0.63898)/2)*1000)-348.5;

//    Serial.print("analogValue: ");Serial.println(analogValueAverage);
//    Serial.print("             load: ");Serial.println(load,5);
    time = millis();
  }
//  
//  float load = getWeight();
  if (Serial.available()>0)
  {
    incomingByte = Serial.read();

    switch (incomingByte){
    case 'w':
      Serial.println(load,5);
      time = millis();
      break;
    case 'o':
      openBowl();
      break;
    case 'c':
      closeBowl();
      break;
    case 'f':
      feed();
      break;
    case 's':
      isOpen();
      break;
    case 'r':
      RFID();
      break;
    }
  }        
}

//RFID CONTROLL
void RFID()
{
  String received;
  delay(250);
  Serial1.write(command_scan);

  while(Serial1.available())
  {
    incomingByte = Serial1.read();
    if(incomingByte < 0x10) received += "0" + String(incomingByte, HEX);
    else received += String(incomingByte, HEX);
  }
  if(received.length() > 14){
    Serial.println(received);
  }
}

//BOWL MECHANICAL CONTROLS
void openBowl()
{
  bowlServo.attach(4);
  delay(500);
  while(pos <= 180) // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    bowlServo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(25);                       // waits 15ms for the servo to reach the position 
    //    Serial.print("ROTATING COUNTERCLOCK: ");
    //    Serial.println(bowlServo.read());
    pos += 1;
  } 
  delay(300);
  bowlServo.detach();
}


void closeBowl()
{
  bowlServo.attach(4);
  delay(500);
  while( pos>=0)     // goes from 180 degrees to 0 degrees 
  {                                
    bowlServo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(25);                       // waits 15ms for the servo to reach the position 
    //    Serial.print("ROTATING CLCOK: ");
    //    Serial.println(bowlServo.read());
    pos-=1;
  } 
  delay(300);
  bowlServo.detach();
}

void feed()
{
  feedServo.attach(5);
  delay(500);
  while( pos>=90)     // goes from 90 degrees to 0 degrees 
  {                                
    feedServo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
    pos-=2;
  } 
  delay(300);
  while(pos <= 120) // goes from 0 degrees to 90 degrees 
  {                                  // in steps of 1 degree 
    feedServo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
    pos += 2;
  } 
  delay(300);
  feedServo.detach();
}


//SCALE
//float getWeight()
//{
//  int analogValue = analogRead(0);
//
//  // running average - We smooth the readings a little bit
//  analogValueAverage = 0.99*analogValueAverage + 0.01*analogValue;
//
//  // Is it time to print?
//  if(millis() > time + timeBetweenReadings){
//    float load = (((analogToLoad(analogValueAverage)+0.63898)/2)*1000)-348.5;
//
////    Serial.print("analogValue: ");Serial.println(analogValueAverage);
////    Serial.print("             load: ");Serial.println(load,5);
//    time = millis();
//    return load;
//  }
//  
//}


//scale helper functions
float analogToLoad(float analogval){
  // using a custom map-function, because the standard arduino map function only uses int
  float load = mapfloat(analogval, analogvalA, analogvalB, loadA, loadB);
  return load;
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

boolean isOpen()
{
  if (bowlServo.read() > 90){ 
    Serial.println('1');
  }
  else{ Serial.println('0');}
}

