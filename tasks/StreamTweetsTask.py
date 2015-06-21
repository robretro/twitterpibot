from Authenticator import Authenticator
from twython.api import Twython
from MyStreamer import MyStreamer
from Task import Task

class StreamTweetsTask(Task):

    def onInit(args):
        authenticator = Authenticator()
        tokens = authenticator.Authenticate()
        args.Context.twitter = Twython(tokens[0],tokens[1],tokens[2],tokens[3])
        args.streamer = MyStreamer(tokens[0],tokens[1],tokens[2],tokens[3])
        args.streamer.inbox = args.Context.inbox
 
    def onRun(args):
        print("starting stream")
        args.streamer.user()

    def onStop(args):
        args.streamer.disconnect()




