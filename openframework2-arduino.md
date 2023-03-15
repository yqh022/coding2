# coding2-openframework2-arduino
##  main.cpp
```ruby
#include "ofMain.h"
#include "ofApp.h"

//========================================================================
int main( ){
	ofSetupOpenGL(1024,680,OF_WINDOW);			// <-------- setup the GL context

	// this kicks off the running of my app
	// can be OF_WINDOW or OF_FULLSCREEN
	// pass in width and height too:
	ofRunApp(new ofApp());

}

```
##  ofApp.cpp
```ruby
#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    ofSetVerticalSync(true);
    
    ofBackground(0);
    
    ofSetVerticalSync(true);

    // this uses depth information for occlusion
    // rather than always drawing things on top of each other
    ofEnableDepthTest();

    // ofBox uses texture coordinates from 0-1, so you can load whatever
    // sized images you want and still use them to texture your box
    // but we have to explicitly normalize our tex coords here
    ofEnableNormalizedTexCoords();

    // loads the OF logo from disk
    ofLogo.load("images.png");

    // draw the ofBox outlines with some weight
    ofSetLineWidth(8);
    
    
    ofSetLogLevel(OF_LOG_VERBOSE);
    font.load("monospace", 10);
    
    serial.listDevices();
    vector <ofSerialDeviceInfo> deviceList = serial.getDeviceList();
    
    // this should be set to whatever com port your serial device is connected to.
    // (ie, COM4 on a pc, /dev/tty.... on linux, /dev/tty... on a mac)
    // arduino users check in arduino app....
    int baud = 9600;
    //serial.setup(0, baud); //open the first device
    //serial.setup("COM4", baud); // windows example
    serial.setup("/dev/cu.usbmodem14201", baud); // mac osx example
    //serial.setup("/dev/ttyUSB0", baud); //linux example
}

//--------------------------------------------------------------
void ofApp::update(){
    if (serial.available() < 0) {
        sensorValue = "Arduino Error";
    }
    else {
        //While statement looping through serial messages when serial is being provided.
        while (serial.available() > 0) {
            //byte data is being writen into byteData as int.
            byteData = serial.readByte();
        
            //byteData is converted into a string for drawing later.
            sensorValue = "value: " + ofToString(byteData);
        }
    }
    cout << sensorValue << endl; // output the sensorValue
}

//--------------------------------------------------------------
void ofApp::draw(){
    ofSetColor(225);
    float time =ofGetElapsedTimef();
//    for (int x=1; x<20; x++){
//        for (int i=0; i<900; i+=5){
//
//            ofSetColor(45+127*sin(i *0.01 +timeValue+time), 127+127*sin(i*0.011 +timeValue+time), 127+127*sin(i*0.012 +timeValue+time));
//           // ofDrawCircle(ofGetWidth()/2+100*sin(i*0.01+time), 50+i, 50+40*sin(i*0.005+time));
//            ofDrawCircle(50*x + 100*sin(i *0.01 + timeValue +time+x), 50+i, 50+40*sin(i*0.005 +time+ timeValue));
//        }
//    }
    
    float movementSpeed = .1;
    float cloudSize = ofGetWidth() / 2;
    float maxBoxSize = 80;
    float spacing = 1;
    int boxCount = 10+timeValue;

    cam.begin();

    for(int i = 0; i < boxCount; i++) {
        ofPushMatrix();

        float t = (ofGetElapsedTimef() + i * spacing) * movementSpeed;
        glm::vec3 pos(
            ofSignedNoise(t, 0, 0),
            ofSignedNoise(0, t, 0),
            ofSignedNoise(0, 0, t));

        float boxSize = maxBoxSize * ofNoise(pos.x, pos.y, pos.z);

        pos *= cloudSize;
        ofTranslate(pos);
        ofRotateXDeg(pos.x);
        ofRotateYDeg(pos.y);
        ofRotateZDeg(pos.z);

        ofLogo.bind();
        ofFill();
        ofSetColor(255);
        ofDrawBox(boxSize);
        ofLogo.unbind();

        ofNoFill();
        ofSetColor(ofColor::fromHsb(sinf(t) * 128 + 128,127*sin(timeValue+time)+40 , timeValue));
        ofDrawBox(boxSize * 1.2f);

        ofPopMatrix();
    }
    cam.end();
    
        msg = "press key a, b or c :\n";
        font.drawString(msg, 40, 40);
        font.drawString("sensorValue: " + sensorValue, 40, 60);
    timeValue =byteData;
   
//    for (int x=1; x<20; x++){
//        for (int i=0; i<900; i+=5){
//
//            ofSetColor(45+127*sin(i *0.01 +timeValue+time), 127+127*sin(i*0.011 +timeValue+time), 127+127*sin(i*0.012 +timeValue+time));
//           // ofDrawCircle(ofGetWidth()/2+100*sin(i*0.01+time), 50+i, 50+40*sin(i*0.005+time));
//            ofDrawCircle(50*x + 100*sin(i *0.01 + timeValue +time+x), 50+i, 50+40*sin(i*0.005 +time+ timeValue));
//        }
//    }
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    switch (key) {
        case 'a':
            serial.writeByte('a');
            cout << "flash green LED" << endl;;
            break;
            
        case 'b':
            serial.writeByte('b');
            cout << "flash red LED" << endl;
            break;
            
        case 'c':
            serial.writeByte('c');
            cout << "flash white LED" << endl;
            break;
            
        default:
            break;
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------

```
##  ofApp.h
```ruby
#pragma once

#include "ofMain.h"

class ofApp : public ofBaseApp{

public:
    void setup();
    void update();
    void draw();
    
    void keyPressed  (int key);
    void keyReleased(int key);

    ofTrueTypeFont        font;
        
    ofSerial    serial;
    string sensorValue;
    int byteData;
    string msg;
    int timeValue;
    
    ofImage ofLogo; // the OF logo
    ofLight light; // creates a light and enables lighting
    ofEasyCam cam;
};

```
##  Arduino code
```ruby
int ledPin = 13;
int greenLedPin = 12;
int redLedPin = 11;
int sensorPin = 0;
int sensorValue = 0;

void setup()
{
  // start serial port at 9600 bps:
  Serial.begin(9600);
  pinMode (ledPin, OUTPUT);
}

void loop()
{
  sensorValue = analogRead(sensorPin);
  char inByte = 0;
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();

    if (inByte == 'a') {
      digitalWrite(greenLedPin, HIGH);
      delay(500);
      digitalWrite(greenLedPin, LOW);
    }

    if (inByte == 'b') {   
        digitalWrite(redLedPin, HIGH);
        delay(500);
        digitalWrite(redLedPin, LOW);
    }

    if (inByte == 'c') {
      for (int i = 0; i < 4; i++) {
        digitalWrite(ledPin, HIGH);
        delay(sensorValue+50);
        digitalWrite(ledPin, LOW);
        delay(sensorValue+50);
      }
    }
    // byte read, send three characters
    // Serial.print(inByte);
    
  }
   Serial.write(sensorValue);
}

```
