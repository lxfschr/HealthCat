#include <SoftwareSerial.h>
#include <Servo.h> 

//Servo
int pos = 0;
Servo bowlServo;
Servo feedServo;

//Scale
int scalePin = 0;

//load scale variables
float aReading = 33.0;
float aLoad = 315.0; // gs.
float bReading = 378.0;
float bLoad = 1290.0; // gs.


const int numReadings = 50;

int readings[numReadings];      // the readings from the analog input
int index = 0;                  // the index of the current reading
float total = 0;                  // the running total
float load = 0;                // the average
float average = 0; 



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

 for (int thisReading = 0; thisReading < numReadings; thisReading++)
    readings[thisReading] = 0; 
}

void loop() 
{

    // subtract the last reading:
  total = total - readings[index];         
  // read from the sensor:
  // Calculate load based on A and B readings above
  float newReading = analogRead(0);
  load = ((bLoad - aLoad)/(bReading - aReading)) * (newReading - aReading) + aLoad;
  readings[index] = load; 
  // add the reading to the total:
  total= total + readings[index];       
  // advance to the next position in the array:  
  index = index + 1;                    

  // if we're at the end of the array...
  if (index >= numReadings)              
    // ...wrap around to the beginning: 
    index = 0;                           

  // calculate the average:
  average = total / numReadings;  
  
  
  if (Serial.available()>0)
  {
    incomingByte = Serial.read();

    switch (incomingByte){
    case 'w':
      Serial.println(average,2);
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

boolean isOpen()
{
  if (bowlServo.read() > 90){ 
    Serial.println('1');
  }
  else{ Serial.println('0');}
}
