/*
 * 
 Created 8/1/20016
 by Abdel-Razzak Merheb
 Controls a remote control car via serial port

 Pins 10, 11, 12, and 13 are used to control the car


 The circuit:
 * The remote controller is connected to pins 10, 11, 12, and 13
 * Arduino UNO is used
 * The remote takes its vcc and GND from the Arduino board
 * Note: on most Arduinos there is already an LED on the board
 attached to pin 13.
 */

// constants won't change. They're used here to
// set pin numbers:
const int UpPin =  8;      // The pin used to control the forward move
const int DwnPin =  5;      // The pin used to control the backward move
const int RghtPin =  10;      // The pin used to control the right move
const int LftPin =  12;      // The pin used to control the left move

int CommandByte = 0;   // Command received via serial port

// Initialize pins
void setup() {
// sets the digital pins as output  
pinMode(UpPin, OUTPUT); 
pinMode(DwnPin, OUTPUT); 
pinMode(RghtPin, OUTPUT); 
pinMode(LftPin, OUTPUT);      

// Initialize serial port
Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

// Repeat
void loop() {
// Whenever a byte is received via serial port
while(Serial.available()) 
    {
        
      // Read the incoming byte:
      CommandByte = Serial.read();
      // Perform the commands

      // Forward command is received
      if (CommandByte == '1') 
        {
          
          Serial.println("Forward");
          // First be sure that Down button (go back) is unpressed, then send forward command
          digitalWrite(DwnPin, LOW);  // Stop backward
          digitalWrite(UpPin, HIGH); // Go forward
        }
        
      // delay(500);                  // waits for 500 m.seconds

          // Backward command is received
            if (CommandByte == '2') 
        {
          
          Serial.println("Back");
          // First be sure that Up button (go forward) is unpressed, then send backward command
          digitalWrite(UpPin, LOW); // Stop forward
          digitalWrite(DwnPin, HIGH); // Go backward
          
        }

         // Go right command is received
            if (CommandByte == '3') 
        {
          
          Serial.println("Right");
          // First be sure that Left button is unpressed, then send right command
          digitalWrite(LftPin, LOW); // Stop turning left
          digitalWrite(RghtPin, HIGH);  // Turn right
          
        }

        // Go left command is received
            if (CommandByte == '4') 
        {
          
          Serial.println("Left");
          // First be sure that right button is unpressed, then send left command
          digitalWrite(RghtPin, LOW); // Stop turning right
          digitalWrite(LftPin, HIGH); // Turn left
          
        }


        // Stop command is received
            if (CommandByte == '5') 
        {
          Serial.println("Stop");
          // Stop everything
          digitalWrite(UpPin, LOW); // Stop forward
          digitalWrite(DwnPin, LOW); // Stop backward
          digitalWrite(RghtPin, LOW); // Stop turning right
          digitalWrite(LftPin, LOW); // Stop turning left
          
        }        

      // delay(1000);                  // waits for a second
    }
}
