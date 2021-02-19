import keyboard
import time

iterations = int(sys.argv[1])
mouse.click()
time.sleep(1)
keyboard.send('ctrl+f')
time.sleep(1)
keyboard.send('2')
time.sleep(2)
keyboard.send('0')
time.sleep(2)
keyboard.send('2')
time.sleep(2)
keyboard.send('enter')
time.sleep(2)

for _ in range(iterations-2):
    keyboard.send('ctrl+enter')
    time.sleep(0.1)
    keyboard.send('ctrl+g')
    time.sleep(0.3)

