from time import sleep


################### MODEL #############################

from common import Model
            

################### CONTROLLER #############################

class Controller():
    def __init__(self, m):
        self.m = m
        self.current_pellet = None
    
    def poll(self):
        cmd = None
        if self.current_pellet is None or self.current_pellet not in self.m.pellets:
            running_total = 999999
            for pellet in self.m.pellets:
                if pellet[0] + pellet[1] < running_total:
                    self.current_pellet = pellet
                    running_total = pellet[0] + pellet[1]
        if self.m.mybox[0] < self.current_pellet[0]:
            cmd = 'right'
        elif self.m.mybox[0] > self.current_pellet[0]:
            cmd = 'left'
        elif self.m.mybox[1] < self.current_pellet[1]:
            cmd = 'down'
        elif self.m.mybox[1] > self.current_pellet[1]:
            cmd = 'up'
            
        if cmd:
            self.m.do_cmd(cmd)
        
################### VIEW #############################

class View():
    def __init__(self, m, max_timer = 50):
        self.m = m
        self.max_timer = max_timer
        self.timer = max_timer
        
    def display(self):
        self.timer-=1
        if self.timer <= 0:
            print 'location: ' + str(self.m.mybox[0]) + ', ' + str(self.m.mybox[1])
            self.timer = self.max_timer
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()