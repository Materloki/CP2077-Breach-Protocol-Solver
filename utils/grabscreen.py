# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = 'D:\Program Files/tesseract/tesseract.exe'


def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

def get_sections(region=None, image=None):
    '''
    Get the text sections that we need to solve
    the puzzle
    '''
    if image == None:
        screen = grab_screen(region)
    else:
        screen = cv2.imread(image)
    
    matrix = screen[350:750, 250:700] #Depends on the resolution, mine is standard FHD
    sequences = screen[340:470, 820:1100]

    sections = [matrix, sequences]
    for i in range(len(sections)):
        # Pre process the image to better performance at OCR
        sections[i] = cv2.cvtColor(sections[i], cv2.COLOR_BGR2GRAY)
        kernel = np.ones((2,2), np.uint8)
        sections[i] = cv2.dilate(sections[i], kernel, iterations=1)
        kernel_e = np.ones((2,2), np.uint8)
        sections[i]= cv2.erode(sections[i], kernel_e, iterations=1)
        sections[i] = cv2.medianBlur(sections[i],3)
        # Tesseract handles better black text on white background
        sections[i] = cv2.threshold(sections[i], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    custom_config = r'--oem 3 --psm 6'
    text_matrix = pytesseract.image_to_string(sections[0], config=custom_config)
    text_sequences = pytesseract.image_to_string(sections[1], config=custom_config)
    return text_matrix, text_sequences

def breach_panel(region=None):
    ''''
    Checks if the game is on the breach protocol screen,
    then we can proceed to solve the puzzle
    
    '''
    screen = grab_screen()
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen_logo = screen[0:100, 0:300]
    template = cv2.imread("utils/template.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    res = cv2.matchTemplate(screen_logo, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res>=0.9) #0.9 is the threshold
    if len(loc[0]) != 0:
        return True
    else:
        return False

if __name__ == "__main__":
    text_matrix, text_sequences = get_sections(image="mine2.png")
    print(text_matrix)
    print(text_sequences)
