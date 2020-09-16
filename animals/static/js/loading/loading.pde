/*
  Arc Length parametrization of curves by Jakub Valtar

  This example shows how to divide a curve into segments
  of an equal length and how to move along the curve with
  constant speed.

  To demonstrate the technique, a cubic Bézier curve is used.
  However, this technique is applicable to any kind of
  parametric curve.
*/

BezierCurve curve;

PVector[] points;

float t = 0.0;
float tStep = 0.004;

final int POINT_COUNT = 80;

int borderSize = 40;

// create an array of ball objects
Ball [] theBalls = new Ball[100];

// keep track of how many balls we have already created
int maxBalls = 100;
int numBalls = 0;
int currentBall = 0;

void setup() {
  size(400, 252, P2D);
  
  frameRate(60);
  smooth(8);
  textAlign(CENTER);
  textSize(16);
  strokeWeight(2);
  
  PVector a = new PVector(   40, 300);
  PVector b = new PVector( 440,   0);
  PVector c = new PVector(-200,   0);
  PVector d = new PVector( 280, 300);

  curve = new BezierCurve(a, b, c, d);
  
  points = curve.points(POINT_COUNT);
}


void draw() {
  
  // Show static value when mouse is pressed, animate otherwise
  if (mousePressed) {
    int a = constrain(mouseX, borderSize, width - borderSize);
    t = map(a, borderSize, width - borderSize, 0.0, 1.0);
    background(random(0,255),random(0,255),random(0,255));
  } else {
    t += tStep;
    if (t > 1.0) {
      t = 0.0;
      background(random(0,255),random(0,255),random(0,255));
    }
    else background(255);
  }
  
  labelStyle();
  text("LECTOR ACTIVADO\nACERQUE LA CARAVANA", width/2 + 80, height/4 );
  
  // draw curve and circle using standard parametrization
  pushMatrix();
    translate(width/4 - borderSize, 0);    
    PVector pos1 = curve.pointAtParameter(t);
    // create a ball at this position
    theBalls[ currentBall ] = new Ball(this, pos1.x, pos1.y);
    
    // increase to keep track of the next ball
    currentBall++;
    
    // also increase our total balls used, if necessary
    if (numBalls < theBalls.length)
    {
      numBalls++;
    }
    
    // did we just use our last slot? if so, we can reuse old slots
    if (currentBall >= theBalls.length)
    {
      currentBall = 0;
    }
  popMatrix();
  
  // move and draw all balls that have been created
  for (int i = 0; i < numBalls; i++)
  {
    theBalls[i].fade();
    theBalls[i].move();
    theBalls[i].display();
  }
}

/* paste additional classes here.  remove the "public" declaration from the class definition and any import statements */

class Ball
{
  // instance vars
  private float x;
  private float y;
  private float size;
  private float myRed;
  private float myGreen;
  private float myBlue;
  private float myAlpha;
  private float speedX;
  private float speedY;
  
  // store a reference to the canvas
  private PApplet canvas;
  
  Ball(PApplet canvas, float x, float y)
  {
    // store a ref to the canvas
    this.canvas = canvas;
  
    // store x and y
    this.x = x;
    this.y = y;
    
    // randomize our size
    size = this.canvas.random(35,75);
    
    // randomize our color
    myRed = this.canvas.random(0,255);
    myGreen = this.canvas.random(0,255);
    myBlue = this.canvas.random(0,255);
    myAlpha = this.canvas.random(0,255);
    
    // randomize our speed
    speedX = this.canvas.random(-2, 2);
    speedY = this.canvas.random(-2, 2);
  }
  
  // move our ball
  void move()
  {
    // update position based on speed
    x += speedX;
    y += speedY;
    
    // bounce
    if (x > width)
    {
      x = width;
      speedX *= -1;
    }
    if (y > height)
    {
      y = height;
      speedY *= -1;
    }
    if (x < 0)
    {
      x = 0;
      speedX *= -1;
    }
    if (y < 0)
    {
      y = 0;
      speedY *= -1;
    }
  }
  
  // display our ball
  void display()
  {
    // use our reference to the canvas to draw our ball
    this.canvas.noStroke();
    this.canvas.fill(myRed, myGreen, myBlue, myAlpha);
    this.canvas.ellipse(x,  y,  size,  size);
  }
  
  // fade method - allows a ball to fade out of existence
  void fade()
  {
    if (myAlpha > 0)
    {
      myAlpha -= 3;
    }
    else
    {
      myAlpha = 0;
    }
  } 
}


// Styles -----

void labelStyle() {
  noStroke();
  fill(120);
}

/*
  This class represents a cubic Bézier curve.

  getPointAtParameter() method works the same as bezierPoint().

  Points returned from this method are closer to each other
  at places where the curve bends and farther apart where the
  curve runs straight.

  On the orther hand, getPointAtFraction() and getPointAtLength()
  return points at fixed distances. This is useful in many scenarios:
  you may want to move an object along the curve at some speed
  or you may want to draw dashed Bézier curves.
*/


class BezierCurve {
  
  private final int SEGMENT_COUNT = 100;
  
  private PVector v0, v1, v2, v3;
  
  private float arcLengths[] = new float[SEGMENT_COUNT + 1]; // there are n segments between n+1 points
  
  private float curveLength;
  
  
  BezierCurve(PVector a, PVector b, PVector c, PVector d) {
    v0 = a.get(); // curve begins here
    v1 = b.get();
    v2 = c.get();
    v3 = d.get(); // curve ends here
    
    // The idea here is to make a handy look up table, which contains
    // parameter values with their arc lengths along the curve. Later,
    // when we want a point at some arc length, we can go through our
    // table, pick the place where the point is going to be located and
    // interpolate the value of parameter from two surrounding parameters
    // in our table.

    // we will keep current length along the curve here
    float arcLength = 0;
    
    PVector prev = new PVector();
    prev.set(v0);
    
    // i goes from 0 to SEGMENT_COUNT
    for (int i = 0; i <= SEGMENT_COUNT; i++) {
      
      // map index from range (0, SEGMENT_COUNT) to parameter in range (0.0, 1.0)
      float t = (float) i / SEGMENT_COUNT;
      
      // get point on the curve at this parameter value
      PVector point = pointAtParameter(t);
      
      // get distance from previous point
      float distanceFromPrev = PVector.dist(prev, point);
      
      // add arc length of last segment to total length
      arcLength += distanceFromPrev;
      
      // save current arc length to the look up table
      arcLengths[i] = arcLength;
      
      // keep this point to compute length of next segment
      prev.set(point);
    }
    
    // Here we have sum of all segment lengths, which should be
    // very close to the actual length of the curve. The more
    // segments we use, the more accurate it becomes.
    curveLength = arcLength;
  }
  
  
  // Returns the length of this curve
  float length() {
    return curveLength;
  }
  
  
  // Returns a point along the curve at a specified parameter value.
  PVector pointAtParameter(float t) {
    PVector result = new PVector();
    result.x = bezierPoint(v0.x, v1.x, v2.x, v3.x, t);
    result.y = bezierPoint(v0.y, v1.y, v2.y, v3.y, t);
    result.z = bezierPoint(v0.z, v1.z, v2.z, v3.z, t);
    return result;
  }

  
  
  // Returns a point at a fraction of curve's length.
  // Example: pointAtFraction(0.25) returns point at one quarter of curve's length.
  PVector pointAtFraction(float r) {
    float wantedLength = curveLength * r;
    return pointAtLength(wantedLength);
  }
  
  
  // Returns a point at a specified arc length along the curve.
  PVector pointAtLength(float wantedLength) {
    wantedLength = constrain(wantedLength, 0.0, curveLength);
    
    // look up the length in our look up table
    int index = java.util.Arrays.binarySearch(arcLengths, wantedLength);
    
    float mappedIndex;
    
    if (index < 0) {
      // if the index is negative, exact length is not in the table,
      // but it tells us where it should be in the table
      // see https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html#binarySearch-float:A-float-
      
      // interpolate two surrounding indexes
      int nextIndex = -(index + 1);
      int prevIndex = nextIndex - 1;
      float prevLength = arcLengths[prevIndex];
      float nextLength = arcLengths[nextIndex];
      mappedIndex = map(wantedLength, prevLength, nextLength, prevIndex, nextIndex);
      
    } else {
      // wanted length is in the table, we know the index right away
      mappedIndex = index;
    }
    
    // map index from range (0, SEGMENT_COUNT) to parameter in range (0.0, 1.0)
    float parameter = mappedIndex / SEGMENT_COUNT;
    
    return pointAtParameter(parameter);
  }
  

  // Returns an array of equidistant point on the curve
  PVector[] equidistantPoints(int howMany) {
    
    PVector[] resultPoints = new PVector[howMany];
    
    // we already know the beginning and the end of the curve
    resultPoints[0] = v0.get();
    resultPoints[howMany - 1] = v3.get(); 
    
    int arcLengthIndex = 1;
    for (int i = 1; i < howMany - 1; i++) {
      
      // compute wanted arc length
      float fraction = (float) i / (howMany - 1);
      float wantedLength = fraction * curveLength;
      
      // move through the look up table until we find greater length
      while (wantedLength > arcLengths[arcLengthIndex] && arcLengthIndex < arcLengths.length) {
        arcLengthIndex++;
      }
      
      // interpolate two surrounding indexes
      int nextIndex = arcLengthIndex;
      int prevIndex = arcLengthIndex - 1;
      float prevLength = arcLengths[prevIndex];
      float nextLength = arcLengths[nextIndex];
      float mappedIndex = map(wantedLength, prevLength, nextLength, prevIndex, nextIndex);
      
      // map index from range (0, SEGMENT_COUNT) to parameter in range (0.0, 1.0)
      float parameter = mappedIndex / SEGMENT_COUNT;
      
      resultPoints[i] = pointAtParameter(parameter);
    }
    
    return resultPoints;
  }
  
  
  // Returns an array of points on the curve.
  PVector[] points(int howMany) {
    
    PVector[] resultPoints = new PVector[howMany];
    
    // we already know the first and the last point of the curve
    resultPoints[0] = v0.get();
    resultPoints[howMany - 1] = v3.get();
    
    for (int i = 1; i < howMany - 1; i++) {
      
      // map index to parameter in range (0.0, 1.0)
      float parameter = (float) i / (howMany - 1);
      
      resultPoints[i] = pointAtParameter(parameter);
    }
    
    return resultPoints;
  }
  
}
