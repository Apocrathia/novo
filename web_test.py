import time
import urllib2
import socket

count = 120
host = "8.8.8.8"
port = 53
timeout = 2
while count > 1:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
      #  urllib2.urlopen('http://8.8.8.8', timeout=1)
        count = 0
    except urllib2.URLError as err:
        pass

    time.sleep(1)
    count -= 1.5

