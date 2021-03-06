import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request
app = Flask(__name__)

millis = lambda: int(round(time.time() * 1000))
PI = 3.1415
DISTANCE_BETWEEN_WHEELS = 24
CONFIG_RATIO = 1

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   3 : {'name' : 'left wheel (+)', 'state' : GPIO.LOW},
   5 : {'name' : 'left wheel (-)', 'state' : GPIO.LOW},
   11 : {'name' : 'right wheel (+)', 'state' : GPIO.LOW},
   13 : {'name' : 'right wheel (-)', 'state' : GPIO.LOW}
}

positives = [3, 11]
negatives = [5, 13]

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
   }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

def moveWheelForward(wheelNum):
   GPIO.output(positives[wheelNum - 1], GPIO.HIGH)
   GPIO.output(negatives[wheelNum - 1], GPIO.LOW)

def moveWheelBackward(wheelNum):
   GPIO.output(positives[wheelNum - 1], GPIO.LOW)
   GPIO.output(negatives[wheelNum - 1], GPIO.HIGH)

def stopWheel(wheelNum):
   GPIO.output(positives[wheelNum - 1], GPIO.LOW)
   GPIO.output(negatives[wheelNum - 1], GPIO.LOW)


def moveWheel(wheelNum, dir, dutyCycle):
   dutyCycle = max(dutyCycle, 0)
   dutyCycle = min(dutyCycle, 100)
   for i in range(dutyCycle):
      if (dir == 1):
         moveWheelForward(wheelNum)
      else:
         moveWheelBackward(wheelNum)

   for i in range(dutyCycle, 100):
      stopWheel(wheelNum)

def stopAll():
   stopWheel(1)
   stopWheel(2)

def moveChairForward(chairSpeed):
   moveWheel(1, 1, chairSpeed)
   moveWheel(2, 1, chairSpeed)

def moveChairBackward(chairSpeed):
   moveWheel(1, 0, chairSpeed)
   moveWheel(2, 0, chairSpeed)

def turnChairLeft(degree):
   radius = DISTANCE_BETWEEN_WHEELS
   wheelSpeed = CONFIG_RATIO * (2 * PI * radius) * (degree / 360.0)
   moveWheel(2, 0, wheelSpeed)

def turnChairRight(degree):
   radius = DISTANCE_BETWEEN_WHEELS
   wheelSpeed = CONFIG_RATIO * (2 * PI * radius) * (degree / 360.0)
   moveWheel(1, 0, wheelSpeed)

def moveChairDemo(duration, chairSpeed):
   if (duration < 100):
      duration = duration * 1000

   startTime = millis()
   moveChairForward(chairSpeed)
   while(millis() <= startTime + duration):
      continue
  
   startTime = millis()
   moveChairBackward(chairSpeed)
   while(millis() <= startTime + duration):
      continue
  
   stopAll()

@app.route("/<mode>")
def action(mode):
   # If the action part of the URL is "on," execute the code indented below:
   if mode == "forward":
      moveChairForward(100)
      # Save the status message to be passed into the template:
      message = "Moving forward."
   if mode == "backward":
      moveChairBackward(100)
      message = "Moving backwards."
   if mode == "left":
      turnChairLeft(90)
      message = "Turning left."
   if mode == "right":
      turnChairRight(90)
      message = "Turning right."
   if mode == "stop":
      stopAll()
      message = "Stopping."
   if mode == "demo":
      moveChairDemo(10, 100)
      message = "Running demo."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<leftSpeed>/<rightSpeed>")
def action(leftSpeed, rightSpeed):
   leftSpeed = int(leftSpeed)
   rightSpeed = int(rightSpeed)

   moveWheel(1, 1, leftSpeed)
   moveWheel(2, 1, rightSpeed)

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
