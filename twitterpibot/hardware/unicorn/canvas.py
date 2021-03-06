import datetime
import logging

import pytz

from twitterpibot.hardware.myhardware import is_linux
from twitterpibot.hardware.unicorn.directions import Down

if is_linux:
    import unicornhat
else:
    import twitterpibot.hardware.unicorn.unicornhat_viz as unicornhat

from twitterpibot.hardware.unicorn.sprites import Raindrop, Firework, Square, BouncingBall
from twitterpibot.hardware.unicorn.games import SnakeGame
from twitterpibot.logic import astronomy, image_helper


day_bright = 196
night_bright = 64


def _calc_max_brightness(now=None):
    return night_bright + int((day_bright - night_bright) * astronomy.get_daytimeness_factor(now))


class CanvasMode(object):
    def __init__(self, buffer):
        self._buffer = buffer


class ParticleMode(CanvasMode):
    def __init__(self, buffer):
        super(ParticleMode, self).__init__(buffer)
        self._particles = []

    def get_particle(self, rgb):
        return Firework(self._buffer, rgb)

    def add_particle(self, rgb):
        particle = self.get_particle(rgb)
        self._particles.append(particle)
        particle.draw()
        self._buffer.update_all()

    def iterate(self):

        for particle in self._particles:
            particle.clear()
        for particle in self._particles:
            particle.iterate()
            if particle.complete:
                self._particles.remove(particle)
        for particle in self._particles:
            particle.draw()
        self._buffer.update_all()


class Rain(ParticleMode):
    def __init__(self, buffer, direction=Down(), trails=False):
        super(Rain, self).__init__(buffer)
        self._direction = direction
        self._trails = trails

    def get_particle(self, rgb):
        return Raindrop(self._buffer, rgb, self._direction, self._trails)


class Fireworks(ParticleMode):
    def get_particle(self, rgb):
        return Firework(self._buffer, rgb)


class Squares(ParticleMode):
    def get_particle(self, rgb):
        return Square(self._buffer, rgb)


class BouncingBalls(ParticleMode):
    def get_particle(self, rgb):
        return BouncingBall(self._buffer, rgb)




class Buffer(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._buffer = [[(0, 0, 0) for _ in range(self._x)] for _ in range(self._y)]

        self.max_bright = _calc_max_brightness()

    def set_max_brightness(self):
        self.max_bright = _calc_max_brightness()

    def _write_pixel(self, x, y):
        pixel = self._buffer[x][y]
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        unicornhat.set_pixel(x, y, r, g, b)

    def update_all(self):
        for y in range(8):
            for x in range(8):
                self._write_pixel(x, y)
        unicornhat.show()

    def fade(self):
        for y in range(8):
            for x in range(8):
                r, g, b = self._buffer[x][y]
                r, g, b = image_helper.fade_rgb(r, g, b)
                self._buffer[x][y] = (r, g, b)
                unicornhat.set_pixel(x, y, r, g, b)
        unicornhat.show()

    def clear(self):
        r = 0
        g = 0
        b = 0
        for y in range(8):
            for x in range(8):
                unicornhat.set_pixel(x, y, r, g, b)
        unicornhat.show()

    def camera_flash(self, on):
        for y in range(8):
            for x in range(8):
                if on:
                    r = 255
                    g = 255
                    b = 255
                else:
                    pixel = self._buffer[x][y]
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                unicornhat.set_pixel(x, y, r, g, b)
        unicornhat.show()

    def pixel_delta(self, clear, position, rgb_delta):
        x = position.x
        y = position.y
        if 0 <= x < 8 and 0 <= y < 8:
            if clear:
                self._buffer[x][y] = tuple(self._limit(z[0] - z[1]) for z in zip(self._buffer[x][y], rgb_delta))
            else:
                self._buffer[x][y] = tuple(self._limit(sum(z)) for z in zip(self._buffer[x][y], rgb_delta))

    def _limit(self, param):
        return max(0, min(param, self.max_bright))

    def set_pixel(self, position, rgb):
        x = position.x
        y = position.y
        if 0 <= x < 8 and 0 <= y < 8:
            self._buffer[x][y] = rgb


if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    now = datetime.datetime.now(pytz.UTC)

    for hour in range(24):
        for min in range(0, 59, 5):
            time = now + datetime.timedelta(hours=hour, minutes=min)

            print("{} {} {}".format(hour, time, _calc_max_brightness(time)))
