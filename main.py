import board
import neopixel
import time

NEOPIXEL_PIN = board.D2
LED_COUNT = 30

pixels = neopixel.NeoPixel(board.NEOPIXEL, NEOPIXEL_PIN)

delay = 1
r, g, b, h = 0, 0, 0, 0
delta = 3 #amount that the hue changes (hue determines which color it is)
# 0 <= h <= 360; 0 <= s, v<=1
def set_color(H, S, V):
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
    global h
    global delta
    s = 0.5 # saturation value
    v = 0.5 # value
    for i in range(LED_COUNT):
        if h >= 360 or h < 0:
            delta *= -1
        h+=delta
        pixels[i] = set_color(h, s, v)
    pixels.show()
while 1:
    loop()
    time.sleep(delay)
