from network import Listener, Handler, poll


handlers = {} # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        global handlers, names, subs
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name] = self
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            send_list = {}
            send_everyone = True
            name, txt = msg['speak'], msg['txt']
            #broadcast({'speak': name, 'txt': txt})
            tokens = txt.split()
            for token in tokens:
                if token.startswith('+'):
                    if token[1:] not in subs:
                        subs[token[1:]] = []
                    subs[token[1:]].append(name)
                elif token.startswith('#'):
                    send_everyone = False
                    if token[1:] in subs:
                        for user in subs[token[1:]]:
                            send_list[user] = names[user]
                elif token.startswith('-'):
                    if token[1:] in subs:
                        if name in subs[token[1:]]:
                            subs[token[1:]].remove(name)
                elif token.startswith('@'):
                    send_everyone = False
                    if token[1:] in names:
                        send_list[token[1:]] = names[token[1:]]
            if send_everyone:
                broadcast({'speak':name, 'txt':txt})
            else:
                for h in send_list.values():
                    h.do_send({'speak':name, 'txt':txt})
            
                    
                    
                    


Listener(8888, MyHandler)
while 1:
    poll(0.05)