# coding2-openframework1.1-boid
## boid.cpp
```ruby
/*
 *  boid.cpp
 *  boids
 *
 *  Created by Marco Gillies on 05/10/2010.
 *  Copyright 2010 Goldsmiths, University of London. All rights reserved.
 *
 */

#include "boid.h"
#include "ofMain.h"

Boid::Boid()
{
	separationWeight = 3.0f;
	cohesionWeight = 0.9f;
	alignmentWeight = 0.2f;
	
	separationThreshold = 50;
	neighbourhoodSize = 100;
	
	position = ofVec3f(ofRandom(0, 200), ofRandom(0, 200));
	velocity = ofVec3f(ofRandom(-2, 2), ofRandom(-2, 2));
}

Boid::Boid(ofVec3f &pos, ofVec3f &vel)
{
	separationWeight = 1.0f;
	cohesionWeight = 0.2f;
	alignmentWeight = 0.1f;
	
	separationThreshold = 10;
	neighbourhoodSize = 100;
	
	position = pos;
	velocity = vel;
}

Boid::~Boid()
{
	
}

float Boid::getSeparationWeight()
{
	return separationWeight;
}
float Boid::getCohesionWeight()
{
	return cohesionWeight;
}

float Boid::getAlignmentWeight()
{
	return alignmentWeight;
}


float Boid::getSeparationThreshold()
{
	return separationThreshold;
}

float Boid::getNeighbourhoodSize()
{
	return neighbourhoodSize;
}


void Boid::setSeparationWeight(float f)
{
	separationWeight = f;
}
void Boid::setCohesionWeight(float f)
{
	cohesionWeight = f;
}

void Boid::setAlignmentWeight(float f)
{
	alignmentWeight = f;
}


void Boid::setSeparationThreshold(float f)
{
	separationThreshold = f;
}

void Boid::setNeighbourhoodSize(float f)
{
	neighbourhoodSize = f;
}


ofVec3f Boid::getPosition()
{
	return position;
}

ofVec3f Boid::getVelocity()
{
	return velocity;
}

ofVec3f Boid::separation(std::vector<Boid *> &otherBoids)
{
	// finds the first collision and avoids that
	// should probably find the nearest one
	// can you figure out how to do that?
    
    ofVec3f v(0,0,0); // create v
    
	for (int i = 0; i < otherBoids.size(); i++)
	{	
		if(position.distance(otherBoids[i]->getPosition()) < separationThreshold)
		{
			//ofVec3f v = position -  otherBoids[i]->getPosition();
            v = position -  otherBoids[i]->getPosition();
			v.normalize();
			//return v;
		}
	}
    return v; // return v
}

ofVec3f Boid::cohesion(std::vector<Boid *> &otherBoids)
{
	ofVec3f average(0,0,0);
	int count = 0;
	for (int i = 0; i < otherBoids.size(); i++)
	{
		if (position.distance(otherBoids[i]->getPosition()) < neighbourhoodSize)
		{
			average += otherBoids[i]->getPosition();
			count += 1;
		}
	}
	average /= count;
	ofVec3f v =  average - position;
	v.normalize();
	return v;
}

ofVec3f Boid::alignment(std::vector<Boid *> &otherBoids)
{
	ofVec3f average(0,0,0);
	int count = 0;
	for (int i = 0; i < otherBoids.size(); i++)
	{
		if (position.distance(otherBoids[i]->getPosition()) < neighbourhoodSize)
		{
			average += otherBoids[i]->getVelocity();
			count += 1;
		}
	}
	average /= count;
	ofVec3f v =  average - velocity;
	v.normalize();
	return v;
}

void Boid::update(std::vector<Boid *> &otherBoids, ofVec3f &min, ofVec3f &max)
{
	velocity += separationWeight*separation(otherBoids);
	velocity += cohesionWeight*cohesion(otherBoids);
	velocity += alignmentWeight*alignment(otherBoids);
	
	walls(min, max);
	position += velocity;
}

void Boid::walls(ofVec3f &min, ofVec3f &max)
{
	if (position.x < min.x){
		position.x = min.x;
		velocity.x *= -1;
	} else if (position.x > max.x){
		position.x = max.x;
		velocity.x *= -1;
	}
	
	if (position.y < min.y){
		position.y = min.y;
		velocity.y *= -1;
	} else if (position.y > max.y){
		position.y = max.y;
		velocity.y *= -1;
	}
	
	
}

void Boid::draw()
{
	ofSetColor(123, 162, 63);
	ofCircle(position.x, position.y, 25);
}
```
## boid.h
```ruby
/*

 *
 */

#ifndef _BOID
#define _BOID
#include <vector>
#include "ofMain.h"

class Boid
{
// all the methods and variables after the
// private keyword can only be used inside
// the class
protected:	
	ofVec3f position;
	ofVec3f velocity;
	
	float separationWeight;
	float cohesionWeight;
	float alignmentWeight;
	
	float separationThreshold;
	float neighbourhoodSize;
	
	ofVec3f separation(std::vector<Boid *> &otherBoids);
	ofVec3f cohesion(std::vector<Boid *> &otherBoids);
	ofVec3f alignment(std::vector<Boid *> &otherBoids);
	
// all the methods and variables after the
// public keyword can only be used by anyone
public:	
	Boid();
	Boid(ofVec3f &pos, ofVec3f &vel);
	
	~Boid();
	
	ofVec3f getPosition();
	ofVec3f getVelocity();
	
	
	float getSeparationWeight();
	float getCohesionWeight();
	float getAlignmentWeight();
	
	float getSeparationThreshold();
	float getNeighbourhoodSize();
	
	void setSeparationWeight(float f);
	void setCohesionWeight(float f);
	void setAlignmentWeight(float f);
	
	void setSeparationThreshold(float f);
	void setNeighbourhoodSize(float f);
	
	void update(std::vector<Boid *> &otherBoids, ofVec3f &min, ofVec3f &max);
	
	void walls(ofVec3f &min, ofVec3f &max);
	
	virtual void draw();
};

#endif

```
## main.cpp
```ruby
#include "ofMain.h"
#include "testApp.h"

//========================================================================
int main( ){

    ofSetupOpenGL(1024,768, OF_WINDOW);            // <-------- setup the GL context

    // this kicks off the running of my app
    // can be OF_WINDOW or OF_FULLSCREEN
    // pass in width and height too:
    ofRunApp( new testApp());

}
```
## miniboid.cpp
```ruby
//
//  miniboid.cpp
//  mySketch-week3-1
//
// 
//

#include "miniboid.hpp"

miniboid::miniboid()
{
    separationWeight = 1.2f;
    cohesionWeight = 1.2f;
    alignmentWeight = 0.2f;
    
    separationThreshold = 30;
    neighbourhoodSize = 80;
    
    position = ofVec3f(ofRandom(0, 200), ofRandom(0, 200));
    velocity = ofVec3f(ofRandom(-2, 2), ofRandom(-2, 2));
}

void miniboid::draw(){
    ofSetColor(87, 76, 87);
    ofCircle(position.x, position.y, 10);
}

```
## miniboid.hpp
```ruby
/
//  miniboid.hpp
//  mySketch-week3-1
//
//  
//

#ifndef miniboid_hpp
#define miniboid_hpp

#include <stdio.h>
#include "boid.h"


class miniboid : public Boid {
public:
    miniboid();
    void draw();
};

#endif /* miniboid_hpp */

```
## testApp.cpp
```ruby
#include "testApp.h"

testApp::~testApp()
{
	for (int i = 0; i < boids.size(); i++)
	{
		delete boids[i];
	}
}

//--------------------------------------------------------------
void testApp::setup(){
	
	
	int screenW = ofGetScreenWidth();
	int screenH = ofGetScreenHeight();

	ofBackground(247, 217, 76);
	
	// set up the boids
	for (int i = 0; i < 50; i++)
    {
        boids.push_back(new miniboid());
        boids.push_back(new Boid());
    }

}


//--------------------------------------------------------------
void testApp::update(){
	
    ofVec3f min(0, 0);
	ofVec3f max(ofGetWidth(), ofGetHeight());
	for (int i = 0; i < boids.size(); i++)
	{
		boids[i]->update(boids, min, max);
	}
}

//--------------------------------------------------------------
void testApp::draw(){

	for (int i = 0; i < boids.size(); i++)
	{
		boids[i]->draw();
	}

}


//--------------------------------------------------------------
void testApp::keyPressed(int key){
 
}

//--------------------------------------------------------------
void testApp::keyReleased(int key){
    
}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){
    
}

//--------------------------------------------------------------
void testApp::mouseDragged(int x, int y, int button){
    
}

//--------------------------------------------------------------
void testApp::mousePressed(int x, int y, int button){
	
}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){
    
}

//--------------------------------------------------------------
void testApp::windowResized(int w, int h){
    
}

```
## testApp.h
```ruby
#ifndef _TEST_APP
#define _TEST_APP


#include "ofMain.h"
#include <vector>
#include "boid.h"
#include "miniboid.hpp"

class testApp : public ofBaseApp{
	
public:
    ~testApp();
	
    void setup();
    void update();
    void draw();
    
    void keyPressed(int key);
    void keyReleased(int key);
    void mouseMoved(int x, int y );
    void mouseDragged(int x, int y, int button);
    void mousePressed(int x, int y, int button);
    void mouseReleased(int x, int y, int button);
    void windowResized(int w, int h);

    std::vector<Boid *> boids;
	
};

#endif	

```
