import math
import time
import random
try:    
    from piglow import PiGlow
    enablePiglow = True
except Exception:
    enablePiglow = False


class MyPiglow(object):
    def __init__(self, *args, **kwargs):

        self.t = 0;

        self.piglow = None
        if enablePiglow:
            self.piglow = PiGlow()
            self.maxbright = 8
            self.piglow.all(0)

            self.buffer = [0 for led in range(18)]



        return super(MyPiglow, self).__init__(*args, **kwargs)

    def getLed(args, arm,colour):
        return int(6 * arm + colour)
    def getBright(args, factor):
        return max(0, min(int(-0.5 * args.maxbright + args.maxbright * factor),255))



    def InitPattern(args):
        self.pattern = [[0 for x in range(360)]for y in range(18)]
        for t in range(360):
            for colour in range(6):
                for arm in range(3):
                    b1 = math.sin(math.radians(t + arm * 15 + colour * 360 / 32))
                    led = self.getLed(arm,colour)
                    self.pattern[led][t] = self.getBright(b1)

    def DisplayPattern(args):

        if enablePiglow:
            if args.t >= 360:
                args.t = 0
            else:
                args.t += 1

            for led in range(18):
                args.piglow.led(led + 1, args.pattern[led][args.t])
             
            time.sleep(1) 


    def OnInboxItemRecieved(args, inboxItem):
        if enablePiglow:
            led = random.randint(0,17)
            args.buffer = args.maxbright
            args.WriteLed(led)


    def Fade(args):
        if enablePiglow:

            for led in range(18):
                if args.buffer[led] > 1:
                    args.buffer[led] -= 1
        
            args.WriteAll()

    def WriteAll(args):
        if enablePiglow:
            for led in range(18):
                args.WriteLed(led)
                

    def WriteLed(args, led):
        if enablePiglow:
            args.piglow.led(led + 1, args.buffer[led])