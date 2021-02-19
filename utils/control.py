import utils.keys as k
import time

keys = k.Keys()

def horizontal(d):
    if d > 0:
        for i in range(d):
            keys.directMouse(63, 0)
            time.sleep(0.1)
    else:
        d = - d 
        for i in range(d):
            keys.directMouse(-63, 0)
            time.sleep(0.1)

def vertical(d):
    if d > 0:
        for i in range(d):
            keys.directMouse(0, 63)
            time.sleep(0.1)
    else:
        d = - d 
        for i in range(d):
            keys.directMouse(0, -63)
            time.sleep(0.1)

def pathing(path):
    # Get the cursor in to the matrix
    keys.directKey("LEFT")
    time.sleep(0.4)
    keys.directKey("LEFT", keys.key_release)
    time.sleep(0.4)

    # Follow the path that the solver found
    x, y = 0, 5
    for i in range(len(path)):
        x_ = path[i][0]
        y_ = path[i][1]
        dx = x_ - x
        dy = y_ - y
        if dx != 0:
            vertical(dx)
        if dy != 0:
            horizontal(dy)
        keys.directKey("F")
        time.sleep(0.01)
        keys.directKey("F", keys.key_release)
        x = x_
        y = y_
    time.sleep(1)

    #Get out of that screen
    keys.directKey("ESC", type=keys.virtual_keys)
    time.sleep(0.04)
    keys.directKey("ESC", keys.key_release, keys.virtual_keys)
    time.sleep(1)
