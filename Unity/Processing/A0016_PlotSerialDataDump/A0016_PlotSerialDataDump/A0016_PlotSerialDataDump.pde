/*
 * Plot Serial Data Dump
 * Andrew Huard
 * 6/19/2023
 *
 * This sketch accepts serial data from the serial port and plots the 
 * data as a scrolling plot similar to an oscilloscope display.  The 
 * serial data consists of an ASCII text representation of a set of 
 * integers, one integer per line.
 *
 * Example:
 *    "405\n555\n123\n1023\n"
 */

import processing.serial.*;
import java.util.Arrays;

Serial port;               // Serial port object
int[] dataPoints;          // Array to store the received data
int dataLength = 1000;      // Length of data array
int currentIndex = 0;      // Current index in the data array

void setup() {
  size(800, 400);
  background(255);
  
  // Set up the serial port
  String[] portList = Serial.list();
  print("Ports Available: ");
  for (int i = 0; i < portList.length; i++) {
    print(portList[i]);
    if (i + 1 < portList.length)
      print(",");
    else
      println("");
  }
  
  String portName = "COM8";    // Change the index if needed
  print("Connecting to: ");
  println(portName);
  port = new Serial(this, portName, 115200);
  
  dataPoints = new int[dataLength];
  
  // Initialize the data array with zeros
  Arrays.fill(dataPoints, 0);
}

void draw() {
  // Read data from the serial port
  while (port.available() > 0) {
    String data = port.readStringUntil('\n');
    if (data != null) {
      data = data.trim();
      try {
        int value = Integer.parseInt(data);
        
        // Shift the existing data points
        for (int i = 0; i < dataLength - 1; i++) {
          dataPoints[i] = dataPoints[i + 1];
        }
        
        // Add the new data point
        dataPoints[dataLength - 1] = value;
      }
      catch(Exception e) {
        continue;
      }
    }
  }
  
  // Clear the background
  background(255);
  
  // Plot the data points
  float xStep = width / (float) dataLength;
  float yStep = height / 1023.0;
  float x = 0;
  for (int i = 1; i < dataPoints.length; i++) {
    float y1 = height - dataPoints[i - 1] * yStep;
    float y2 = height - dataPoints[i] * yStep;
    line(x, y1, x + xStep, y2);
    x += xStep;
  }
}
