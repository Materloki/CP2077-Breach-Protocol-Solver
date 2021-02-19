from utils.grabscreen import grab_screen, get_sections, breach_panel
from utils.solver import text_correction, solver
from utils.control import pathing

import pytesseract
import cv2
import numpy as np
import time

def main():
    print("Running")
    bp = breach_panel()

    #Runs until find the breach screen
    while bp == False:
        time.sleep(1)
        bp = breach_panel()


    #Geting the text sections
    m, sequences = get_sections()
    m = np.array(text_correction(m))
    sequences = text_correction(sequences)
    print(f'Sequences: {sequences}')
    print(f'matrix \n {m}')

    # Breach solver
    path = solver(m, sequences[0])

    #Control the keyboard and mouse to solve the puzzle
    pathing(path)
    return 0

if __name__ == "__main__":
    main()
