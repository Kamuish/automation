import pyautogui
import time
from PIL import ImageGrab
# SITE: http://tanksw.com/piano-tiles/



def main():
    bbox = (697, 590, 1200, 591)

    size = (bbox[2] - bbox[0])

    pos_to_click = [[bbox[0] + 50 + j*size/4,bbox[1] + 60] for j in range(4)]

    max_iters = 2300
    cont = 0
    pyautogui.PAUSE = 0 # remove autoclick speed limitations.

    t0 = time.time()
    while cont < max_iters:
        im = ImageGrab.grab(bbox)

        color = [im.getpixel((50 + j*size/4,0))[0] for j in range(4)]

        pyautogui.click(pos_to_click[color.index(min(color))])

        # During runtime lower the point of the click to account the increasing speed of the tiles
        if cont == 360:
            for j in pos_to_click:
                j[-1] += 15
        elif cont == 430:
            for j in pos_to_click:
                j[-1] += 15
        elif cont == 600:
            for j in pos_to_click:
                j[-1] += 15
        cont += 1
        del im

if __name__ == '__main__':
    # save image file
    main()
  