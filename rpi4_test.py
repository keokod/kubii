raspistill -o image01.jpg -t 5000
libcamera-hello
https://www.youtube.com/watch?v=-NxpCirSqm4

from gpiozero import LED
from time import sleep
pin3 = LED(2) #on branche une led sur la patte gpio2 et la variable se nomme pin3 broche n3 
pin4 = LED(3)
pin7 = LED(4) 

pin11 = LED(17)
pin13 = LED(27)
pin15 = LED(22)

pin19 = LED(10)
pin21 = LED(9)
pin23 = LED(11)

pin27 = LED(0)
pin29 = LED(5)
pin31 = LED(6)

pin33 = LED(13)
pin35 = LED(19)
pin37 = LED(26)

pin40 = LED(21)
pin38 = LED(20)
pin36 = LED(16)

pin32 = LED(12)

pin28 = LED(1)
pin26 = LED(7)
pin24 = LED(8)
pin22 = LED(25)

pin16 = LED(23)
pin18 = LED(24)

pin12 = LED(18)
pin10 = LED(15)
pin8 = LED(14)


while True:
    pin3.on()
    sleep(0.3)
    pin3.off()
    sleep(0.3)
    pin4.on()
    sleep(0.3)
    pin4.off()
    sleep(0.3)
    pin7.on()
    sleep(0.3)
    pin7.off()
    sleep(0.3)
    
    pin11.on()
    sleep(0.3)
    pin11.off()
    sleep(0.3)
    pin13.on()
    sleep(0.3)
    pin13.off()
    sleep(0.3)
    pin15.on()
    sleep(0.3)
    pin15.off()
    sleep(0.3)
    
    pin19.on()
    sleep(0.3)
    pin19.off()
    sleep(0.3)
    pin21.on()
    sleep(0.3)
    pin21.off()
    sleep(0.3)
    pin23.on()
    sleep(0.3)
    pin23.off()
    sleep(0.3)
    
    pin27.on()
    sleep(0.3)
    pin27.off()
    sleep(0.3)
    pin29.on()
    sleep(0.3)
    pin29.off()
    sleep(0.3)
    pin31.on()
    sleep(0.3)
    pin31.off()
    sleep(0.3)
    
    pin33.on()
    sleep(0.3)
    pin33.off()
    sleep(0.3)
    pin35.on()
    sleep(0.3)
    pin35.off()
    sleep(0.3)
    pin37.on()
    sleep(0.3)
    pin37.off()
    sleep(0.3)
    
    pin40.on()
    sleep(0.3)
    pin40.off()
    sleep(0.3)
    pin38.on()
    sleep(0.3)
    pin38.off()
    sleep(0.3)
    pin36.on()
    sleep(0.3)
    pin36.off()
    sleep(0.3)
    
    pin32.on()
    sleep(0.3)
    pin32.off()
    sleep(0.3)
    
        
    pin28.on()
    sleep(0.3)
    pin28.off()
    sleep(0.3)
    pin26.on()
    sleep(0.3)
    pin26.off()
    sleep(0.3)
    pin24.on()
    sleep(0.3)
    pin24.off()
    sleep(0.3)
    pin22.on()
    sleep(0.3)
    pin22.off()
    sleep(0.3)
    
    pin18.on()
    sleep(0.3)
    pin18.off()
    sleep(0.3)
    pin16.on()
    sleep(0.3)
    pin16.off()
    sleep(0.3)
        
    pin12.on()
    sleep(0.3)
    pin12.off()
    sleep(0.3)
    pin10.on()
    sleep(0.3)
    pin10.off()
    sleep(0.3)
    pin8.on()
    sleep(0.3)
    pin8.off()
    sleep(0.3)

#test simple sur le gpio en ligne de commande avec le rpi5:
pinctrl set 2 op dh #met le gpio2 en hight 3.3V
pinctrl set 2 op dh #met le gpio2 en low 0V

#test gpio avec un raspberry pi 5
#utiliser pip pour installer libgpiod-dev et python3
sudo apt install libgpiod-dev python3-libgpiod
#voir le status gpiod:
sudo systemctl start pigpiod
sudo systemctl status pigpiod

from gpiozero import LED
from time import sleep
pin3 = LED(2) #on branche une led sur la patte gpio2 et la variable se nomme pin3 broche n3 
pin4 = LED(3)
pin7 = LED(4) 

pin11 = LED(17)
pin13 = LED(27)
pin15 = LED(22)

pin19 = LED(10)
pin21 = LED(9)
pin23 = LED(11)

pin27 = LED(0)
pin29 = LED(5)
pin31 = LED(6)

pin33 = LED(13)
pin35 = LED(19)
pin37 = LED(26)

pin40 = LED(21)
pin38 = LED(20)
pin36 = LED(16)

pin32 = LED(12)

pin28 = LED(1)
pin26 = LED(7)
pin24 = LED(8)
pin22 = LED(25)

pin16 = LED(23)
pin18 = LED(24)

pin12 = LED(18)
pin10 = LED(15)
pin8 = LED(14)


while True:
    pin3.on()
    sleep(0.3)
    pin3.off()
    sleep(0.1)
    pin4.on()
    sleep(0.1)
    pin4.off()
    sleep(0.1)
    pin7.on()
    sleep(0.1)
    pin7.off()
    sleep(0.1)
    
    pin11.on()
    sleep(0.1)
    pin11.off()
    sleep(0.1)
    pin13.on()
    sleep(0.1)
    pin13.off()
    sleep(0.1)
    pin15.on()
    sleep(0.1)
    pin15.off()
    sleep(0.1)
    
    pin19.on()
    sleep(0.1)
    pin19.off()
    sleep(0.1)
    pin21.on()
    sleep(0.1)
    pin21.off()
    sleep(0.1)
    pin23.on()
    sleep(0.1)
    pin23.off()
    sleep(0.1)
    
    pin27.on()
    sleep(0.1)
    pin27.off()
    sleep(0.1)
    pin29.on()
    sleep(0.1)
    pin29.off()
    sleep(0.1)
    pin31.on()
    sleep(0.1)
    pin31.off()
    sleep(0.1)
    
    pin33.on()
    sleep(0.1)
    pin33.off()
    sleep(0.1)
    pin35.on()
    sleep(0.1)
    pin35.off()
    sleep(0.1)
    pin37.on()
    sleep(0.1)
    pin37.off()
    sleep(0.1)
    
    pin40.on()
    sleep(0.1)
    pin40.off()
    sleep(0.1)
    pin38.on()
    sleep(0.1)
    pin38.off()
    sleep(0.1)
    pin36.on()
    sleep(0.1)
    pin36.off()
    sleep(0.1)
    
    pin32.on()
    sleep(0.1)
    pin32.off()
    sleep(0.1)
    
        
    pin28.on()
    sleep(0.1)
    pin28.off()
    sleep(0.1)
    pin26.on()
    sleep(0.1)
    pin26.off()
    sleep(0.1)
    pin24.on()
    sleep(0.1)
    pin24.off()
    sleep(0.1)
    pin22.on()
    sleep(0.1)
    pin22.off()
    sleep(0.1)
    
    pin18.on()
    sleep(0.1)
    pin18.off()
    sleep(0.1)
    pin16.on()
    sleep(0.1)
    pin16.off()
    sleep(0.1)
        
    pin12.on()
    sleep(0.1)
    pin12.off()
    sleep(0.1)
    pin10.on()
    sleep(0.1)
    pin10.off()
    sleep(0.1)
    pin8.on()
    sleep(0.1)
    pin8.off()
    sleep(0.1)



