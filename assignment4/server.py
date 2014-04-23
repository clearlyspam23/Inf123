from network import Listener, Handler, poll

 
handlers = {} # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        users = ''
        for handler in handlers:
            if users == '':
                users += handlers[handler]
            else:
                users += ', ' + handlers[handler]
        for handler in handlers:
            handler.do_send({'leave':name, 'users':users})
     
    def on_msg(self, msg):
        if 'join' in  msg:
            handlers[self] = msg['join']
            users = ''
            for handler in handlers:
                if users == '':
                    users += handlers[handler]
                else:
                    users += ', ' + handlers[handler]
            for handler in handlers:
                handler.do_send({'join':msg['join'], 'users':users})
        elif 'speak' in msg and msg['txt'] != '':
            for handler in handlers:
                if handlers[handler] != msg['speak']:
                    handler.do_send({'name':msg['speak'], 'txt':msg['txt']})
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds

