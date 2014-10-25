#!/usr/bin/python
# graphicsmagick
# python-game
#sudo python-dev python-pip ; sudo pip install wiringpi2

import picamera
import time
from time import sleep
import os
import subprocess
import pygame
import random
import RPi.GPIO as GPIO
import wiringpi2 as wiringpi
import pifacedigitalio as p 
p.init()


wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(25, 1)
wiringpi.pinMode(24, 1)
wiringpi.pinMode(22, 1)
camera = picamera.PiCamera()

WIDTH=800
HEIGHT=600

def dotext(countdown,FONTSIZE,LEFT):
    screen.fill(black)
    text = countdown 
    font = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    font_surf = font.render(text, True, textcol)
    font_rect = font_surf.get_rect()
    font_rect.left = LEFT
    font_rect.top = 150
    screen.blit(font_surf, font_rect)
    camera.preview_alpha = 200
    pygame.display.update()


# INIT CAMERA
def initcamera():
#    camera = picamera.PiCamera()
    camera.vflip = False
    camera.hflip = False
    camera.brightness = 60
    camera.led = False
    camera.image_effect = 'none' 
    camera.start_preview()

def changeeffect(EFFECT):
  #  camera = picamera.PiCamera()
    #camera.stop_preview()
    camera.stop_preview()
 #   camera.close()
#    sleep(2)
#    camera.vflip = True
#    camera.hflip = False
#    camera.brightness = 60
#    camera.led = False
    camera.image_effect = EFFECT
    camera.start_preview()

effects = ['solarize','oilpaint','hatch','gpen','pastel','washedout','posterise','negative','sketch','emboss','colorswap','cartoon','none']
effectnumber = 0
initcamera()
# BUILD A SCREEN
pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
black = pygame.Color(0, 0, 0)
textcol = pygame.Color(255, 255, 255)
#screen.fill(black)
p.digital_write(3,1) #turn on
p.digital_write(4,1) #turn on

while True:
# my_input = wiringpi.digitalRead(25)
 my_input = p.digital_read(0)
 effect = p.digital_read(1)
# shutoff = wiringpi.digitalRead(24)
 shutoff = p.digital_read(2)
# effect = wiringpi.digitalRead(22)
 if shutoff == 1:
#  restart = "service shutterpi stop" 	 
#  subprocess.call(restart)
  pygame.quit()
  break
 if effect == 1:
  effect = effects[effectnumber] 
  effectnumber = (effectnumber + 1) % len(effects)
 # dotext('', 150, 150)
  changeeffect(effect)
  dotext(effect, 100, 150)
  sleep(1)
  dotext('', 150, 150)
 if my_input == 1:
  p.digital_write(3,0) #turn off
  p.digital_write(4,0) #turn off
  count=0
  while (count < 4):
     camera.start_preview()
     # TAKE A PHOTO
     now = time.strftime("%Y%m%d%H%M%S")
     name=now + ".jpg"
     sleep(1)
     dotext('Ready..', 150, 150)
     sleep(1)
     dotext('3', 300, 300)
     sleep(1)
     dotext('2', 300, 300)
     sleep(1)
     dotext('1', 300, 300)
     sleep(1)
     dotext('Smile :)', 150, 150)
     sleep(1)
     dotext('', 200, 200)
     p.digital_write(0,1)
     p.digital_write(1,1)
     sleep(0.1)
     p.digital_write(0,0)
     p.digital_write(1,0)
     playsound = "/usr/bin/play /home/pi/camera-shutter.oga &"
     #os.system(playsound)
     subprocess.call(playsound,shell=True)
     #sleep(.5)
     camera.capture(name, format='jpeg', resize=(WIDTH,HEIGHT))
     p.digital_write(0,1)
     p.digital_write(1,1)
     sleep(0.1)
     p.digital_write(0,0)
     p.digital_write(1,0)
          #camera.stop_preview()
 
     #READ IMAGE AND PUT ON SCREEN
     #img = pygame.image.load(name)
     #screen.blit(img, (0, 0))
     #pygame.display.update()    
     makeborder = "gm convert " + name + " -border 8x2 new-" + name
     os.system(makeborder) 
     # WAIT A BIT
     #sleep(1)
     count+=1
 # camera.start_preview()
  # CEATE PHOTOBOOTH STRIPS OF PHOTOS
  dotext('thinking..', 150, 100)
  singlestrip = "gm convert $(ls new*.jpg) -append singlestrip.jpg"
  os.system(singlestrip)
  doublestrip = "gm convert singlestrip.jpg singlestrip.jpg +append strip-" + now + ".jpg"
  os.system(doublestrip)
  # DELETE TEMPORARY FILES
  cleanup = "rm new*.jpg *strip.jpg"
  os.system(cleanup)
  dotext('printing..', 150, 100)
  printing = "lp"
  #os.system(printing)
  dotext('', 150, 150)
  changeeffect('none')
  p.digital_write(3,1) #turn on
  p.digital_write(4,1) #turn on

  # CLOSE CLEANLY AND EXIT
 sleep(0.5)
# pygame.quit()
