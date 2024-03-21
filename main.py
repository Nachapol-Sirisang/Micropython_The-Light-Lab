# -- Library --
from machine import Pin, ADC, SoftI2C
import random
import time
import utime
import ssd1306

# -- Set pin --
# Light sensor
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_2_5DB) # 2_5 / 6 / 11
adc.width(ADC.WIDTH_10BIT) # 9 / 10 / 11 / 12
R_LDR = 10000
V_LRD_Max = 3.3
LDR_Bit = 1023 # 1023 / 2047
RL10 = 20
Gamma = 0.7

# Display
i2c = SoftI2C(scl=Pin(27), sda=Pin(26))
oled = ssd1306.SSD1306_I2C(128, 64, i2c) # 128x64, 128x32, 72x40, 64x48 | 1 ตัว กว้าง 8 pixel สูง 10 pixel | 1 แถว 16 ตัว | เว้นบรรทัดทีละ 10 | ได้สูงสุด 6 แถว

# Button
button_pin = Pin(17, Pin.IN)

# Variable
item_index = [0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
problems = [
          ["Reading in a","dark room"],
          ["In a library"],
          ["In a bedroom"],
          ["Creating a warm", "and comfortable", "atmosphere in a", "living room"],
          ["At a computer"],
          ["In a ", "conference room"],
          ["In a living room"],
          ["Sleeping"],
          ["In a restaurant"],
          ["Exercising in", "a gym"],
          ["Doing artwork in", "a dining room"],
          ["Watching a movie", "in a theater"],
          ["Cooking in a", "kitchen"],
          ["Shopping in ", "a mall"],
          ["In a hotel room"],
          ["Working with", "machinery"],
          ["Creating an", "energetic", "atmosphere at a", "product display"],
          ["Reading in bed"],
          ["Applying makeup"],
          ["Sewing requires", "precision"]
     ]
answer = [[300, 500],
          [300, 500],
          [100, 250],
          [250, 500],
          [500, 750],
          [500, 750],
          [250, 500],
          [0, 50],
          [250, 500],
          [750, 1000],
          [250, 500],
          [250, 500],
          [500, 750],
          [500, 750],
          [100, 250],
          [800, 1000],
          [750, 1000],
          [100, 250],
          [500, 750],
          [750, 1000]
]
   
# -- Sub Function --
def clear_display():
  oled.fill(0)
  oled.show()

def random_problems(item_index_buffer_func):
    item_rand_func =[]
    for i in range(0,8,1):
        item_index_rand = random.choice(item_index_buffer_func)
        item_rand_func.append(item_index_rand)
        item_index_buffer_func.remove(item_index_rand)
    return item_rand_func

def print_display(LUX_round):
    oled.text("Light: {} LUX".format(LUX_round),54, 0)
    oled.show()
    
def print_console(LUX_round):
    print("Light: {} LUX".format(LUX_round))
    
# -- Main Function --
def display_gameSrart():
    oled.text('Welcome to', 25, 20) #(text, เว้นด้านหน้า, เว้นบรรทัด)
    oled.text('The Light Lab', 10, 40) 
    oled.show()
    time.sleep(5)
    clear_display()

def display_gameStartIn():
    oled.text('Push button ', 20, 25)
    oled.text('to Start', 30, 40)
    oled.show()
    while True:
        if button_pin.value() == 1:
            break
        utime.sleep_ms(50)
    sec = 3
    while sec > 0:
        clear_display()
        oled.text(str(sec), 60, 30) # ตัวเดียวกลางจอ
        oled.show()
        sec -= 1
        time.sleep(1)

def display_problem():
    # Reset Variable
    global score
    score = 0
    point = 1
    
    # Random problems
    item_index_buffer = item_index.copy()
    item_rand = random_problems(item_index_buffer)
    
    # Program

    # No.
    for item in item_rand:
        clear_display()
        ans_range1 = answer[item][0]
        ans_range2 = answer[item][1]
        
        # Print Problem
        oled.text('No. {}/8'.format(point), 0, 0)
        line = 10
        for msg in problems[item]:
            oled.text(msg, 0, line)
            line += 10
        oled.text('Push to answer', 0, 50)
        oled.show()

        while True:
            if button_pin.value() == 1:
                break
            LUX = sensor_read()
            utime.sleep_ms(250)

        clear_display()
        utime.sleep_ms(200)

        if LUX in range(ans_range1, ans_range2):
            score += 1
            
            oled.text('Good Job!', 27, 0)
            oled.text('You got 1 point', 4, 20)
            oled.text("AnsIs" + str(ans_range1) + "-" + str(ans_range2) + "LUX", 0, 30)
            oled.text('Push to continue', 0, 50)
            oled.show()

            while True:
                if button_pin.value() == 1:
                    clear_display()
                    break
                utime.sleep_ms(50)
        else:
            clear_display()
            oled.text('Almost There', 10, 0)
            oled.text("AnsIs" + str(ans_range1) + "-" + str(ans_range2) + "LUX", 0, 20)
            oled.text('Push to continue', 0, 50)
            oled.show()
            while True:
                sensor_read_val = sensor_read()
                oled.text("Now {} LUX".format(sensor_read_val), 20, 30)
                oled.show()
                if button_pin.value() == 1:
                    break
                utime.sleep_ms(250)
                oled.text("Now {} LUX".format(sensor_read_val), 20, 30, 0)
                oled.show()
        clear_display()
        point += 1
        time.sleep(1)
    time.sleep(1)

def display_endGame():
    oled.text("You got {} point".format(score), 5, 25)
    oled.text('Push to continue', 0, 50)
    if score > 4:
        oled.text('Nice One!', 28, 0)
    else:
        oled.text('Nice Try Dude', 12, 0)
    oled.show()
    while True:
        if button_pin.value() == 1:
            break
        utime.sleep_ms(50)

def sensor_read():
    sensor_value = adc.read()
    sensor_vol = sensor_value / LDR_Bit * V_LRD_Max
    try:
        sensor_R = R_LDR * (1 / ((V_LRD_Max / sensor_vol) - 1))
    except Exception:
        sensor_R = R_LDR
    LUX = pow(RL10 * 1e3 * pow(10, Gamma) / sensor_R,(1 / Gamma))
    LUX_round = round(LUX)
    return LUX_round


# -- Main --
if __name__ == "__main__":
    display_gameSrart()
    while True:
        display_gameStartIn()
        clear_display()
        display_problem()
        clear_display()
        display_endGame()
        clear_display()
        time.sleep(3)