from RPi import GPIO
import signal
import time

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class Selector_screen_btn:

    def __init__(self, select_btn, down_btn, up_btn):
        GPIO.setmode(GPIO.BCM)

        self.selected = False
        self.index = 0
        
        self.select_btn = select_btn
        self.down_btn = down_btn
        self.up_btn = up_btn
        
        GPIO.setup(select_btn,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(down_btn,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(up_btn,GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(select_btn, GPIO.FALLING, callback=self.select_btn_callback, bouncetime=100)
        GPIO.add_event_detect(down_btn, GPIO.FALLING, callback=self.down_btn_callback, bouncetime=100)
        GPIO.add_event_detect(up_btn, GPIO.FALLING, callback=self.up_btn_callback, bouncetime=100)
        
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
         
        # Clear display.
        self.disp.fill(0)
        self.disp.show()
         
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new("1", (self.width, self.height))
         
        draw = ImageDraw.Draw(self.image)
         
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def select_btn_callback(self, channel):
        self.selected = True
        
    def down_btn_callback(self, channel):
        self.index = self.index - 1
        
    def up_btn_callback(self, channel):
        self.index = self.index + 1

    def draw_text_screen(self, line): 

        
        while(len(line)<4):
            line.append(" ")
         
        draw = ImageDraw.Draw(self.image)
        
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        # Write four lines of text.
        
        x = 0
        padding = -2
        top = padding
        bottom = self.height - padding
        font = ImageFont.load_default()   
        
        draw.text((x, top + 0), line[0], font=font, fill=255)
        draw.text((x, top + 8), line[1], font=font, fill=255)
        draw.text((x, top + 16), line[2], font=font, fill=255)
        draw.text((x, top + 25), line[3], font=font, fill=255)
     
        # Display image.
        self.disp.image(self.image)
        self.disp.show()
        time.sleep(0.1)
        
    def draw_text_screen_selector(self, lines):
        
        self.selected = False
        self.index = 0

        while self.selected == False:
            if self.index < 0:
                self.index = 0
            if self.index >= len(lines):
                self.index = len(lines)-1
                
            if self.index+4 > len(lines):
                to_draw = lines[len(lines)-4:len(lines)]
                if len(lines)<4:
                    to_draw[self.index] = "> "+to_draw[self.index]
                else:
                    to_draw[4-(len(lines)-self.index)] = "> "+to_draw[4-(len(lines)-self.index)]
                self.draw_text_screen(to_draw)
            else:
                to_draw = lines[self.index:self.index+4]
                to_draw[0] = "> "+to_draw[0]
                self.draw_text_screen(to_draw)
        return (self.index,lines[self.index])
    
