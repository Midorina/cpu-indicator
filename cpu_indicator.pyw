import time
from threading import Thread

import pystray
from PIL import Image, ImageDraw, ImageFont
from psutil import cpu_percent


class Indicator:
    # changeable variables
    REFRESH_INTERVAL = 0.5
    FONT_SIZE = 200
    ICON_RES = 250, 250

    FONT = ImageFont.truetype('arial.ttf', FONT_SIZE)
    BLUE_BG = Image.new('RGB', ICON_RES, color=(61, 75, 129))
    RED_BG = Image.new('RGB', ICON_RES, color=(255, 0, 0))

    def __init__(self):
        self.icon = pystray.Icon("usage", title="CPU Usage")
        self.icon.menu = pystray.Menu(pystray.MenuItem('Exit', lambda: self.exit_action()))

        self.refresh_icon_thread = None

        # this is so that our icon refresher thread knows when to stop
        self.stopped = False

    def exit_action(self):
        self.icon.stop()
        self.stopped = True

    def refresh_icon(self):
        while True:
            if self.stopped is True:
                return

            # ceil the usage without the math lib
            # to decrease the size of the .exe file
            # (this most likely didnt help at all)
            usage = cpu_percent(interval=0)
            usage = int(- (-usage // 1))

            # decide bg depending on usage
            image = self.RED_BG.copy() if usage > 70 else self.BLUE_BG.copy()

            # draw the usage text over bg
            draw = ImageDraw.Draw(image)
            draw.text(
                # center the usage text
                xy=(
                    self.ICON_RES[0] / 2,
                    self.ICON_RES[1] / 2
                ),
                anchor="mm",  # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#text-anchors

                text=str(usage),
                font=self.FONT,
                fill=(255, 255, 255),
            )

            self.icon.icon = image

            time.sleep(self.REFRESH_INTERVAL)

    def start(self):
        self.refresh_icon_thread = Thread(daemon=True, target=self.refresh_icon)
        self.refresh_icon_thread.start()

        # wait a bit so that an icon is set
        time.sleep(0.5)

        self.icon.run()

        self.refresh_icon_thread.join()


Indicator().start()
