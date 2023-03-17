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
Loading models, using model textures
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
 Sound visualization
 ```ruby
ofDrawRectangle(0, 1, 1,waveform[2] * ofGetHeight()/1.); //first line
    for(int i = 1; i < (ofGetHeight() + 1); ++i) {
        ofDrawRectangle(i, waveform[i] * ofGetHeight()/10., i + 1, waveform[i+1] * ofGetHeight()/10.,waveform[i+2] * ofGetHeight()/20.);
    }
```
Controls the movement and rotation of the cones
```ruby
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
```
get the position of the model，save the current view，restore the view position，get the model attributes，
```ruby
void ofApp::drawWithModel(){

    glm::vec3 position = model.getPosition();
    ofPushMatrix();
    ofTranslate(position);
    ofRotateDeg(-ofGetMouseX(), 0, 1, 0);
    ofRotateDeg(90,1,0,0);
    ofTranslate(-position);
    model.drawFaces();
    ofPopMatrix();
}

void ofApp::drawWithMesh(){
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

    if(bHasTexture) texture.bind();
    material.begin();
    mesh.drawFaces();
    material.end();
    if(bHasTexture) texture.unbind();

    ofPopMatrix();

}
```
every time the mouse is dragged, track the change
accumulate the changes inside of curRot through multiplication

```ruby
void ofApp::mouseDragged(int x, int y, int button){
    glm::vec2 mouse(x,y);
    glm::quat yRot = glm::angleAxis(ofDegToRad(x-lastMouse.x)*dampen, glm::vec3(0,1,0));
    glm::quat xRot = glm::angleAxis(ofDegToRad(y-lastMouse.y)*dampen, glm::vec3(-1,0,0));
    curRot = xRot * yRot * curRot;
    lastMouse = mouse;
}
```
