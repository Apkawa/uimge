import uimge
import threading, Queue

url = Queue.Queue()

def upl( mode ):
    _u = uimge.Uimge()
    _u.set_host(mode)
    while True:
        msg = url.get()
        if msg:
            _u.upload( msg  )
            print _u.img_url
        else:
            break
num_thread = 200
for i in xrange( num_thread):
    t1 = threading.Thread( target = upl, args=['o_opicture'] )
    t1.start()
for x in xrange(1000):
    url.put('http://i707.photobucket.com/albums/ww71/lynthai/left4dead-mar1st.jpg')
for n in xrange(num_thread):
    url.put(False)
t1.join()
exit(1)
