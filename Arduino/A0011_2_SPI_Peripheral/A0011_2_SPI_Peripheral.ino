/*
 * A0011-2
 * SPI Demo, Qty 2 Arduino Boards, Peripheral
 * Andrew Huard
 * 4/17/2023 
 *
 * Broadcasts a string message between boards over the SPI link, then print it to the serial port.
 *
 * This sketch implements the message receiver, which receives the message over the SPI link and 
 * prints it to the serial port.
 *
 * The peripheral device will serve as the slave device in this demo.
 *
 * Caution: Arduino Yun USB power source is very noisy and interferes with SPI communications.
 * To fix this, power the Yun externally off the +5V bus.  Arduino Uno is noise free and can 
 * serve as the +5V rail for the Arduino Yun.
 *
 * Code adapted from Arduino Documentation: Introduction to SPI:
 *    https://docs.arduino.cc/tutorials/generic/introduction-to-the-serial-peripheral-interface
 */

#include<SPI.h>

// Ports for Arduino Uno
#define DATAOUT    11  // COPI (MOSI)
#define DATAIN     12  // CIPO (MISO)
#define SPICLOCK   13  // SCK
#define CHIPSELECT 10  // CS_N

// Ports for Arduino Yun
//#define DATAOUT    16  // COPI (MOSI)
//#define DATAIN     14  // CIPO (MISO)
//#define SPICLOCK   15  // SCK
//#define CHIPSELECT 10  // CS_N

//opcodes (Different for Each Application, See Device Datasheet or can be arbitrary)
#define READ  3
#define WRITE 2

byte clr;     // dummy variable used to clear the bus
byte inByte;  // varable used to store input messages as they come in

byte data = 0;  // simulate reading and writing to this data store as if it were a real SPI device (e.g., the wiper on a digital potentiometer)

void setup() {
  Serial.begin(9600);  // open the Arduino Serial Monitor and set the baud rate to match, this will let you see the output

  pinMode(DATAOUT, INPUT);     // MOSI is input for Peripherals
  pinMode(DATAIN, OUTPUT);     // MISO is output for Peripherals
  pinMode(SPICLOCK, INPUT);    // SCK is input for Peripherals
  pinMode(CHIPSELECT, INPUT);  // CS_N is input for Peripherals

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

  SPCR = (0<<SPIE)|(1<<SPE)|(0<<DORD)|(0<<MSTR)|(0<<CPOL)|(0<<CPHA)|(1<<SPR1)|(1<<SPR1);  // SPCR = 01000011, use this to control the bus settings
  
  clr=SPSR;  // clear spurious data from prior runs (see Arduino docs)
  clr=SPDR;  // clear spurious data from prior runs (see Arduino docs)
}

void loop() {

  SPI.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));  // reserves the SPI bus, COPI/CIPO seems to behave better on the oscilloscope when using this.
  inByte = SPI.transfer(0x00);  // send the dummy byte 0x00 to CIPO since we're reading only and simultaneously read from COPI
  SPI.endTransaction();  // release the SPI bus, do this after every set of byte transfers as soon as possible, you can always reserve the SPI bus again if needed

  if(inByte==WRITE) {
    Serial.print("Write: ");  // Send the command byte written by the controller and received by the peripheral to the Serial Monitor in Arduino IDE
    Serial.print(inByte);
    Serial.print(", ");

    SPI.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));  // reserves the SPI bus, COPI/CIPO seems to behave better on the oscilloscope when using this.
    data = SPI.transfer(0x00);  // send the dummy byte 0x00 to CIPO since we're reading only and simultaneously read from COPI
    SPI.endTransaction();  // release the SPI bus, do this after every set of byte transfers as soon as possible, you can always reserve the SPI bus again if needed

    Serial.println(data);  // Send the data written by the controller and received by the peripheral to the Serial Monitor in Arduino IDE
  } 
  else if(inByte==READ) {
    Serial.print("Read: ");  // Send the command byte read by the controller and sent by the peripheral to the Serial Monitor in Arduino IDE
    Serial.print(inByte);
    Serial.print(", ");

    SPI.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));  // reserves the SPI bus, COPI/CIPO seems to behave better on the oscilloscope when using this.
    clr = SPI.transfer(data);   // performs simultaneous read and write; 0xFF is a dummy write value
    SPI.endTransaction();  // release the SPI bus, do this after every set of byte transfers as soon as possible, you can always reserve the SPI bus again if needed
    Serial.println(data);  // Send the data read by the controller and sent by the peripheral to the Serial Monitor in Arduino IDE
  } 
  else {}  // do nothing if no command is recognized, could be noise on the bus we want to skip
}