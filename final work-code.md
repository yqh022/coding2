# coding2-final work-code
## main.cpp
```ruby
#include "ofMain.h"
#include "ofApp.h"

//========================================================================
int main( ){
	ofSetupOpenGL(1024,768,OF_WINDOW);			// <-------- setup the GL context

	// this kicks off the running of my app
	// can be OF_WINDOW or OF_FULLSCREEN
	// pass in width and height too:
	ofRunApp(new ofApp());

}

```
## ofApp.cpp
```ruby
#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    
    //Initialize the drawing variables
    for (int i = 0; i < ofGetWidth(); ++i) {
        waveform[i] = 0;
    }
    waveIndex = 0;
    
   
    int sampleRate = 44100; /* Sampling Rate */
    int bufferSize= 512; 
    ofxMaxiSettings::setup(sampleRate, 2, bufferSize);
    
    myClock.setTempo(10);
    myClock.setTicksPerBeat(4);
    
    mySample.load(ofToDataPath("lizi.wav"));
      
    ofSoundStreamSettings settings;
    settings.setOutListener(this);
    settings.sampleRate = sampleRate;
    settings.numOutputChannels = 2;
    settings.numInputChannels = 0;
    settings.bufferSize = bufferSize;
    soundStream.setup(settings);
    
    ofSetFrameRate(60);
    ofSetVerticalSync(true);
    ofBackground(50, 50, 50, 0);
    
    ofSetLogLevel(OF_LOG_VERBOSE);
    font.load("monospace", 10);
    
    serial.listDevices();
    vector <ofSerialDeviceInfo> deviceList = serial.getDeviceList();
    
  
    int baud = 9600;
    //serial.setup(0, baud); //open the first device
    //serial.setup("COM4", baud); // windows example
    serial.setup("/dev/cu.usbmodem14201", baud); // mac osx example
    //serial.setup("/dev/ttyUSB0", baud); //linux example
    
    

 
    ofDisableArbTex();

    //this makes sure that the back of the model doesn't show through the front
    ofEnableDepthTest();

    //now we load our model
    model.loadModel("model/ABPK-Veins.3ds");

    model.setPosition(ofGetWidth()*.5, ofGetHeight() * 0.05, 30);

    light.enable();
    light.setPosition(model.getPosition() + glm::vec3(0, 0, 200));
    
    //this slows down the rotate a little bit
    dampen = .4;
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
        msg = "press key a, b or c :\n";
        font.drawString(msg, 20, 30);
        font.drawString("sensorValue: " + sensorValue, 40, 60);
    timeValue =byteData;
    float time =ofGetElapsedTimef();
    
    
    /////////////// waveform
    ofBackground(210, 195, 241);
    
    
    //translate so that 0,0 is the center of the screen
    ofPushMatrix();
    ofTranslate(ofGetWidth()/2, ofGetHeight()/2, 40);

    auto axis = glm::axis(curRot);
    //apply the quaternion's rotation to the viewport and draw the sphere
    ofRotateDeg(ofRadToDeg(glm::angle(curRot)), axis.x, axis.y, axis.z);
    /// You can actually use the folling line instead, just showing this other option as example
    ///    ofRotateRad(glm::angle(curRot), axis.x, axis.y, axis.z);
    
   
    ofSetColor(245,229,215);
    //ofDrawCone(60, 80, 100, 30, 60);
    //ofDrawCone(160, 80, 100, 30, 60);
    ofDrawSphere(0, 0, 0, 240-timeValue);
   
    for (int x=1; x<20; x++){
        for (int i=0; i<900; i+=5){
            
            ofSetColor(127+127*sin(i *0.01 +time), 127+127*sin(i*0.011 +time), 127+127*sin(i*0.012 +time+x));
           // ofDrawCircle(ofGetWidth()/2+100*sin(i*0.01+time), 50+i, 50+40*sin(i*0.005+time));
            //ofDrawCone(50*x + 100*tan(i *0.01 + time +x), 50+i, 50+40*sin(i*0.005 + time),10);
        }
    }
  

    
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
        ofRotateXDeg(pos.y);
        ofRotateYDeg(pos.x);
        ofRotateZDeg(pos.z);

        ofLogo.bind();
        ofNoFill();
        ofSetColor(timeValue,timeValue,255,100);
        ofDrawCone(boxSize/3, timeValue, 10, 20, 20);
        ofLogo.unbind();

        ofNoFill();
        ofSetColor(ofColor::fromHsb(cosf(t) * 128 + 128, 255, 255));
        //ofDrawSphere(boxSize * 1.1f/2, boxSize * 1.1f/2, 20);

        ofPopMatrix();
    }

    cam.end();
    
    
    ofPopMatrix();
    
    
    
    
    ofTranslate(0, ofGetHeight()/2);
    ofSetColor(255,255,255,20);
    ofNoFill();
    ofSetLineWidth(2);
    
    ofDrawRectangle(0, 1, 1,waveform[2] * ofGetHeight()/1.); //first line
    for(int i = 1; i < (ofGetHeight() + 1); ++i) {
        ofDrawRectangle(i, waveform[i] * ofGetHeight()/10., i + 1, waveform[i+1] * ofGetHeight()/10.,waveform[i+2] * ofGetHeight()/20.);
    }
    
    
    
    ofSetColor(200, 20, 25,30);

    //first let's just draw the model with the model object
    //drawWithModel();

    //then we'll learn how to draw it manually so that we have more control over the data
    drawWithMesh();
    
    
   
}

//draw the model the built-in way
void ofApp::drawWithModel(){

    //get the position of the model
    glm::vec3 position = model.getPosition();

    //save the current view
    ofPushMatrix();

    //center ourselves there
    ofTranslate(position);
    ofRotateDeg(-ofGetMouseX(), 0, 1, 0);
    ofRotateDeg(90,1,0,0);
    ofTranslate(-position);

    //draw the model
    model.drawFaces();

    //restore the view position
    ofPopMatrix();
}

//draw the model manually
void ofApp::drawWithMesh(){

    //get the model attributes we need
    glm::vec3 scale = model.getScale();
    glm::vec3 position = model.getPosition();
    float normalizedScale = model.getNormalizedScale();
    ofVboMesh mesh = model.getMesh(0);
    ofTexture texture;
    ofxAssimpMeshHelper& meshHelper = model.getMeshHelper( 0 );
    bool bHasTexture = meshHelper.hasTexture();
    if( bHasTexture ) {
        texture = model.getTextureForMesh(0);
    }

    ofMaterial material = model.getMaterialForMesh(0);

    ofPushMatrix();

    //translate and scale based on the positioning.
    ofTranslate(position);
    ofRotateDeg(-ofGetMouseX(), 0, 1, 0);
    ofRotateDeg(90,1,0,0);


    ofScale(normalizedScale, normalizedScale, normalizedScale);
    ofScale(scale.x,scale.y,scale.z);

    //modify mesh with some noise
    float liquidness = 5;
    float amplitude = mouseY/100.0;
    float speedDampen = 5;
    auto &verts = mesh.getVertices();

    for(unsigned int i = 0; i < verts.size(); i++){
        verts[i].x += ofSignedNoise(verts[i].x/liquidness, verts[i].y/liquidness,verts[i].z/liquidness, ofGetElapsedTimef()/speedDampen)*amplitude;
        verts[i].y += ofSignedNoise(verts[i].z/liquidness, verts[i].x/liquidness,verts[i].y/liquidness, ofGetElapsedTimef()/speedDampen)*amplitude;
        verts[i].z += ofSignedNoise(verts[i].y/liquidness, verts[i].z/liquidness,verts[i].x/liquidness, ofGetElapsedTimef()/speedDampen)*amplitude;
    }

    //draw the model manually
    if(bHasTexture) texture.bind();
    material.begin();
    //mesh.drawWireframe(); //you can draw wireframe too
    mesh.drawFaces();
    material.end();
    if(bHasTexture) texture.unbind();

    ofPopMatrix();

}

//--------------------------------------------------------------
void ofApp::audioIn(ofSoundBuffer& input){
    std::size_t nChannels = input.getNumChannels();
    for (size_t i = 0; i < input.getNumFrames(); i++)
    {
        
        // handle input here
    }
}
//--------------------------------------------------------------
void ofApp::audioOut(ofSoundBuffer& output){
    std::size_t outChannels = output.getNumChannels();
    for (int i = 0; i < output.getNumFrames(); ++i){
        
        myClock.ticker();
        if (myClock.tick && ofRandom(1.0)>0.7){
            myFreq+=20;
        }
       
     
        float myOut = mySample.play(1.5);
        
        output[i * outChannels] = osc1.sinewave(myFreq+(osc2.sinewave(0.2))) * 0.5 + myOut/2;
        output[i * outChannels + 1] = output[i * outChannels];
        
        //Hold the values so the draw method can draw them
        waveform[waveIndex] =  output[i * outChannels];
        if (waveIndex < (ofGetWidth() - 1)) {
            ++waveIndex;
        } else {
            waveIndex = 0;
        }
    }
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
void ofApp::mouseMoved(int x, int y ){
    
}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){
    //every time the mouse is dragged, track the change
    //accumulate the changes inside of curRot through multiplication
    glm::vec2 mouse(x,y);
    glm::quat yRot = glm::angleAxis(ofDegToRad(x-lastMouse.x)*dampen, glm::vec3(0,1,0));
    glm::quat xRot = glm::angleAxis(ofDegToRad(y-lastMouse.y)*dampen, glm::vec3(-1,0,0));
    curRot = xRot * yRot * curRot;
    lastMouse = mouse;
}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){
    //store the last mouse point when it's first pressed to prevent popping
    lastMouse = glm::vec2(x,y);
}

```
## ofApp.h
```ruby
#pragma once

#include "ofMain.h"
#include "ofxMaxim.h"
#include "ofxAssimpModelLoader.h"
class ofApp : public ofBaseApp{
    
public:
    void setup() override;
    void update() override;
    void draw() override;
    
    void keyPressed(int key) override;
    void keyReleased(int key) override;
    void mouseMoved(int x, int y ) override;
    void mouseDragged(int x, int y, int button) override;
    void mousePressed(int x, int y, int button) override;
    void mouseReleased(int x, int y, int button) override;
    void mouseEntered(int x, int y) override;
    void mouseExited(int x, int y) override;
    void windowResized(int w, int h) override;
    void dragEvent(ofDragInfo dragInfo) override;
    void gotMessage(ofMessage msg) override;
    
    // For drawing
    float waveform[4096]; //make this bigger, just in case
    int waveIndex;
    
    ofSoundStream soundStream;
    
    /* ofxMaxi*/
    void audioIn(ofSoundBuffer& input) override; // not used in this example
    void audioOut(ofSoundBuffer& output) override;
    maxiOsc osc1;
    maxiOsc osc2;
    maxiClock myClock;
    float myFreq=0;
    maxiSample mySample;
    
    ofMesh mesh;
    //this is our model we'll draw
    ofxAssimpModelLoader model;
    
    ofLight light;
    
    //we added these functions to make it easier to switch between the two methods of drawing
    void drawWithModel();
    void drawWithMesh();
    
    //current state of the rotation
    glm::quat curRot;
    
    //a place to store the mouse position so we can measure incremental change
    glm::vec2 lastMouse;
    
    //slows down the rotation 1 = 1 degree per pixel
    float dampen;
    
    float movementSpeed = .1;
    float cloudSize = ofGetWidth() / 4;
    float maxBoxSize = 40;
    float spacing = 1;
    int boxCount = 50;
    ofImage ofLogo; // the OF logo
//    ofLight light; // creates a light and enables lighting
    ofEasyCam cam; // add mouse controls for camera movement
    
    
    
    ofTrueTypeFont        font;
        
    ofSerial    serial;
    string sensorValue;
    int byteData;
    string msg;
    int timeValue;
};

```

## Arduino code
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
    // Serial.print("£");
    // Serial.print("£");
    // Serial.print(inByte);
    
  }
   Serial.write(sensorValue);
}

```
