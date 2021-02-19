import keyboard
import time
'''
Navigate to page with download links of target and move mouse pointer above title and run the program.
Pass number of links as command line argument.
'''
# If time: Add automation, add robustness
iterations = int(sys.argv[1])
mouse.click()
time.sleep(1)
keyboard.send('ctrl+f')
time.sleep(1)
keyboard.send('2')
time.sleep(1)
keyboard.send('0')
time.sleep(1)
keyboard.send('2')
time.sleep(1)
keyboard.send('enter')
time.sleep(1)

for _ in range(iterations-1):
    keyboard.send('ctrl+enter')
    time.sleep(0.1)
    keyboard.send('ctrl+g')
    time.sleep(0.3)

