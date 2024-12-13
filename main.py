import board
import neopixel
import time
import threading

message = ""

NEOPIXEL_PIN = board.D21
LED_COUNT = 30

pixels = neopixel.NeoPixel(NEOPIXEL_PIN, LED_COUNT)

delay = 0.05
r, g, b, h = 0, 0, 0, 0
delta = 1 #amount that the hue changes (hue determines which color it is)
# 0 <= h <= 360; 0 <= s, v<=1
def get_color(H, S, V):
    C = V * S
    X = C * (1-abs((int(H/60))%2-1))
    m = V - C
    r_prime, g_prime, b_prime = 0, 0, 0

    if h <= 60:
        r_prime, g_prime, b_prime = C, X, 0
    elif H <= 120:
        r_prime, g_prime, b_prime = X, C, 0
    elif H <= 180:
        r_prime, g_prime, b_prime = 0, C, X
    elif H <=240:
        r_prime, g_prime, b_prime = 0, X, C
    elif H <= 300:
        r_prime, g_prime, b_prime = X, 0, C
    else:
        r_prime, g_prime, b_prime = C, 0, X
    return constrain((r_prime + m) * 255, 0, 255), constrain((g_prime + m) * 255, 0, 255), constrain((b_prime + m) * 255, 0, 255)
def constrain(x, min_val, max_val):
    return min(max(x, min_val), max_val)

def loop():
    global message
    global h
    global delta
    s = 1 # saturation value
    v = 1 # value
    for i in range(LED_COUNT):
        if h >= 360 or h < 0:
            delta *= -1
        h+=delta
        if message == "OFF":
            pixels[i] = (0,0,0)
        else: 
            set_led(pixels,i,h,s,v)

def set_led(rpi, led, h_val, s_val, v_val):
    rpi[led] = get_color(h_val,s_val,v_val)
    
def background_task():
    while 1:
        loop()
        time.sleep(delay)

def take_input():
    global message
    while 1:
        message = input("Enter your command: ")
        print("You entered:", message)

if __name__ == "__main__":
    background_thread = threading.Thread(target=background_task)
    background_thread.daemon = True  # Make the thread a daemon so it exits when the main thread exits
    background_thread.start()
    take_input()


