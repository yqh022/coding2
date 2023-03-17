# final project
In the project I combined sounds and then visualised the mixed music. The model is imported and can be controlled to rotate the viewpoint as the mouse
moves. The points on the mesh of the model can be controlled by the mouse to present the flow effect. The sphere inside the model can be moved to 
control its rotation and its size is controlled by data transferred from the Arduino. Small cones that rotate in specific directions can move 
closer or farther away by moving the mouse. The cones are also connected to Arduino to control the diverging and converging motion, and can change
color depending on the value of the potentiometer.
## code
Setup Sound
```ruby
   ofxMaxiSettings::setup(sampleRate, 2, bufferSize);   
    myClock.setTempo(10);
    myClock.setTicksPerBeat(4);
    mySample.load(ofToDataPath("lizi.wav"));
```
Connecting ports to Arduino serial devices
```ruby
 serial.listDevices();
    vector <ofSerialDeviceInfo> deviceList = serial.getDeviceList();
    int baud = 9600;
    serial.setup("/dev/cu.usbmodem14201", baud);
```
```ruby
ofDisableArbTex();

    //this makes sure that the back of the model doesn't show through the front
    ofEnableDepthTest();

    //now we load our model
    model.loadModel("model/ABPK-Veins.3ds");

    model.setPosition(ofGetWidth()*.5, ofGetHeight() * 0.05, 30);

    light.enable();
    light.setPosition(model.getPosition() + glm::vec3(0, 0, 200));
 ```
