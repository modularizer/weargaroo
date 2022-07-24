import time
import terminalio
import displayio

from adafruit_display_text import label
from components.display.colors import get_color


class ColorText(displayio.Group):
    def __init__(self, text="", scale=1, x=0, y=0, line_spacing=20, font=terminalio.FONT, color=0xFFFFFF,
                 background_color=None,
                 tab_replacement=(2, " "), letter_delay=0.05, word_delay=0.3, line_delay=0.6, cursor="|",
                 pause_chars=None, **kwargs):
        super().__init__(scale=scale, x=x, y=y)
        self.color = get_color(color)
        self.background_color = get_color(background_color)
        kwargs.update({"tab_replacement": tab_replacement, "font": font})
        self.kwargs = kwargs
        self.typing_settings = {
            "letter_delay": letter_delay,
            "word_delay": word_delay,
            "line_delay": line_delay,
            "cursor": cursor,
            "pause_chars": pause_chars
        }
        self.typing = False
        self.write(text, color)

    @property
    def text(self):
        return "\n".join([line.text for line in self])

    @text.setter
    def text(self, text):
        while len(self) > 0:
            self.pop(0)
        self.write(text)

    def clear(self):
        self.text = ""

    def write(self, text, color=None, background_color="default", typing=None, letter_delay=None, word_delay=None,
              line_delay=None, cursor=None, pause_chars=None, **kwargs):
        self.kwargs.update(kwargs)

        if color is not None:
            self.color = get_color(color)
        color = self.color
        if background_color != "default":
            self.background_color = get_color(background_color)
        background_color = self.background_color

        if typing is None:
            typing = self.typing
        self.typing = typing

        if not typing:
            t = label.Label(text=text, color=color, background_color=background_color, **self.kwargs)
            self.append(t)
        else:
            if line_delay is not None:
                self.typing_settings["line_delay"] = line_delay
            if word_delay is not None:
                self.typing_settings["word_delay"] = word_delay
            if letter_delay is not None:
                self.typing_settings["letter_delay"] = letter_delay
            if cursor is not None:
                self.typing_settings["cursor"] = cursor
            if pause_chars is not None:
                self.typing_settings["pause_chars"] = pause_chars
            t = label.Label(text="", color=color, background_color=background_color, **self.kwargs)
            self.append(t)

            cur = self.typing_settings["cursor"]
            ld = self.typing_settings["letter_delay"]
            wd = self.typing_settings["word_delay"]
            lnd = self.typing_settings["line_delay"]
            pc = self.typing_settings["pause_chars"]
            n = len(cur)

            t.text = cur
            time.sleep(ld)
            for letter in text:
                if pc and letter in pc:
                    time.sleep(pc[letter])
                else:
                    s = t.text[:-n] + letter + cur
                    t.text = s
                    time.sleep(ld)
                    if letter == " ":
                        time.sleep(wd)
                    if letter == "\n":
                        time.sleep(lnd)
            t.text = t.text[:-n]

    def type(self, text, **kw):
        self.write(text, typing=True, **kw)

