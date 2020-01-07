from psutil import cpu_percent
import pystray
from PIL import Image, ImageDraw, ImageFont
from threading import Thread
import os

icon = None

font = ImageFont.truetype('arial.ttf', 75)


def exit_action(icon):
    icon.visible = False
    icon.stop()
    os._exit(1)


def refresh_images():
    global blue_img
    blue_img = Image.new('RGB', (100, 100), color=(61, 75, 129))
    global red_img
    red_img = Image.new('RGB', (100, 100), color=(255, 0, 0))


def decide_bg(usage):
    if usage > 70:
        return red_img
    else:
        return blue_img


def decide_coords(usage):
    if usage < 10:
        return (32, 5)
    elif usage == 100:
        return (0, 5)
    else:
        return (5, 5)


def start_icon():
    usage = int(cpu_percent(interval=1))
    refresh_images()
    image = decide_bg(usage)
    coords = decide_coords(usage)

    d = ImageDraw.Draw(image)
    d.text(coords, str(usage), font=font, fill=(255, 255, 255))

    global icon
    icon = pystray.Icon("usage", icon=image, title="CPU Usage")
    icon.menu = pystray.Menu(pystray.MenuItem('Exit', lambda: exit_action(icon)))

    icon.run()


def refresh_icon():
    while True:
        usage = int(cpu_percent(interval=1))
        refresh_images()
        image = decide_bg(usage)
        coords = decide_coords(usage)

        d = ImageDraw.Draw(image)
        d.text(coords, str(usage), font=font, fill=(255, 255, 255))

        try:
            icon.icon = image
        except:
            pass


thread1 = Thread(daemon=True, target=start_icon)
thread2 = Thread(daemon=True, target=refresh_icon)

thread1.start()
thread2.start()

thread2.join()
thread1.join()

exit()
