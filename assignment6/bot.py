"""
The Client is slave: 
- it sends only the player inputs to the server.
- every frame, it displays the server's last received data
Pros: the server is the only component with game logic, 
so all clients see the same game at the same time (consistency, no rollbacks).
Cons: lag between player input and screen display (one round-trip).
But the client can smooth the lag by interpolating the position of the boxes. 
"""
from network import Handler, poll

from pygame import Rect, init as init_pygame
from pygame.event import get as get_pygame_events
from pygame.locals import QUIT
from pygame.time import Clock


borders = []
pellets = []
players = {}  # map player name to rectangle
myname = None
     
init_pygame()
clock = Clock()

def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return Rect(x, y, w, h)

keep_going = True
    
class Client(Handler):
    
    def on_close(self):
        global keep_going
        print "Server Closed"
        keep_going = False
        
    def on_open(self):
        print "Connected to server"
            
    def on_msg(self, data):
        global borders, pellets, players, myname
        borders = [make_rect(b) for b in data['borders']]
        pellets = [make_rect(p) for p in data['pellets']]
        players = {name: make_rect(p) for name, p in data['players'].items()}
        myname = data['myname']
        
client = Client('localhost', 8888)  # connect asynchronously

class NetworkController():
    def __init__(self):
        self.current_pellet = None
        self.last_size = None
    
    def poll(self):
        cmd = None
        if self.current_pellet is None or self.current_pellet not in pellets:
            running_total = 999999
            for pellet in pellets:
                if pellet[0] + pellet[1] < running_total:
                    self.current_pellet = pellet
                    running_total = pellet[0] + pellet[1]
        if myname is not None:
            me = players[myname]
            if self.last_size is None:
                self.last_size = me
            else:
                if me.w > self.last_size.w or me.h > self.last_size.h:
                    print 'ate a pellet'
                self.last_size = me
            if me.x <= self.current_pellet.left:
                cmd = 'right'
            elif me.x >= self.current_pellet.right:
                cmd = 'left'
            elif me.y <= self.current_pellet.top:
                cmd = 'down'
            elif me.y >= self.current_pellet.bottom:
                cmd = 'up'
            
        if cmd:
            client.do_send({'input' : cmd })
            
controller = NetworkController()

while keep_going:
    
    poll()  # push and pull network messages

    # send valid inputs to the server
    for event in get_pygame_events():  
        if event.type == QUIT:
            exit()
            
    controller.poll()
    
    # draw everything
#     screen.fill((0, 0, 64))  # dark blue
#     [draw_rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
#     [draw_rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
#     for name, p in players.items():
#         if name != myname:
#             draw_rect(screen, (255, 0, 0), p)  # red
#     if myname:
#         draw_rect(screen, (0, 191, 255), players[myname])  # deep sky blue
#     
#     update_pygame_display()
    
    clock.tick(50)  # frames per second, independent of server frame rate