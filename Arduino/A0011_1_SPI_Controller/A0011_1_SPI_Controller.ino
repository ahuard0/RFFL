/*
 * A0011-1
 * SPI Demo, Qty 2 Arduino Boards, Controller
 * Andrew Huard
 * 4/17/2023 
 *
 * Broadcasts a string message between boards over the SPI link, then print it to the serial port.
 *
 * This sketch implements the message broadcaster, which sends the message over the SPI link.
 *
 * The controller will serve as the master device in this demo.
 *
 * Caution: Arduino Yun USB power source is very noisy and interferes with SPI communications.
 * To fix this, power the Yun externally off the +5V bus.  Arduino Uno is noise free and can 
 * serve as the +5V rail for the Arduino Yun
 *
 * Code adapted from Arduino Documentation: Introduction to SPI
 *    https://docs.arduino.cc/tutorials/generic/introduction-to-the-serial-peripheral-interface
 */

#include<SPI.h>

// Ports for Arduino Uno
//#define DATAOUT    11  // COPI (MOSI)
//#define DATAIN     12  // CIPO (MISO)
//#define SPICLOCK   13  // SCK
//#define CHIPSELECT 10  // CS_N

// Ports for Arduino Yun
#define DATAOUT    16  // COPI (MOSI)
#define DATAIN     14  // CIPO (MISO)
#define SPICLOCK   15  // SCK
#define CHIPSELECT 10  // CS_N

//opcodes (Different for Each Application, See Device Datasheet or can be arbitrary)
#define READ  3
#define WRITE 2

// variables for input and output
byte out;
byte in;

int count = 0;  // the message being sent, will increment from 0-255 each message (make this whatever you want)

void setup() {
  Serial.begin(9600);

  pinMode(DATAOUT, OUTPUT);     // MOSI is input for Peripherals
  pinMode(DATAIN, INPUT);       // MISO is output for Peripherals
  pinMode(SPICLOCK, OUTPUT);    // SCK is input for Peripherals
  pinMode(CHIPSELECT, OUTPUT);  // CS_N is input for Peripherals

  // SPI Control Register (SPCR)
  // | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
  // | SPIE | SPE  | DORD | MSTR | CPOL | CPHA | SPR1 | SPR0 |
  // SPIE - Enables the SPI interrupt when 1
  // SPE  - Enables the SPI when 1
  // DORD - Sends data least Significant Bit First when 1, most Significant Bit first when 0
  // MSTR - Sets the Arduino in controller mode when 1, peripheral mode when 0
  // CPOL - Sets the data clock to be idle when high if set to 1, idle when low if set to 0
  // CPHA - Samples data on the falling edge of the data clock when 1, rising edge when 0
  // SPR1 and SPR0 - Sets the SPI speed, 00 is fastest (4MHz) 11 is slowest (250KHz)  

  SPCR = (0<<SPIE)|(1<<SPE)|(0<<DORD)|(1<<MSTR)|(0<<CPOL)|(0<<CPHA)|(1<<SPR1)|(1<<SPR1);  // SPCR = 01010011
  
  byte clr;
  clr=SPSR;  // clear spurious data from prior runs (see Arduino docs)
  clr=SPDR;  // clear spurious data from prior runs (see Arduino docs)

  digitalWrite(CHIPSELECT, HIGH); // disable write (CS_N is active low)
}

void loop() {
  if (count > 255)  // increment the message from 0-255
    count = 0;
  out = count++;

  digitalWrite(CHIPSELECT, LOW); // disable write (CS_N is active low)
  SPI.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));  // reserves the SPI bus, COPI/CIPO seems to behave better on the oscilloscope when using this.
  SPI.transfer(WRITE);  // send the WRITE command to the SPI bus (COPI)
  SPI.transfer(out);    // send the data byte to COPI
  SPI.endTransaction();  // release the SPI bus, do this after every set of byte transfers as soon as possible, you can always reserve the SPI bus again if needed
  digitalWrite(CHIPSELECT, HIGH); // disable write (CS_N is active low)

  delay(50);  // can transmit as fast as you want, even with no delay, but this is here to make reading easier on the peripheral side since we're doing Serial.Println() which takes a longer time

  digitalWrite(CHIPSELECT, LOW); // disable write (CS_N is active low)
  SPI.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));   // reserves the SPI bus, COPI/CIPO seems to behave better on the oscilloscope when using this.
  SPI.transfer(READ);  // send the READ command to the SPI bus
  in = SPI.transfer(0x00);  // send the dummy byte 0x00 to COPI since we're reading only and simultaneously read from CIPO
  SPI.endTransaction();  
  digitalWrite(CHIPSELECT, HIGH); // disable write (CS_N is active low)

  delay(50);  // can transmit as fast as you want, even with no delay, but this is here to make reading easier on the peripheral side since we're doing Serial.Println() which takes a longer time
}
