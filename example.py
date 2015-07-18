from wo import WO
import logging
###uncomment for printing debug info
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
logging.captureWarnings(True)
#import urllib3
#urllib3.disable_warnings()



appid = "55590b16a7f6527a06ebe96d"
appsec = "e4b72c8cb25d32ba" 
username = ""
password = ""



client = WO('webobservatory.soton.ac.uk', appid, appsec, username ,password )

##login after the client creation
res = client.login()
if res:
    print "Error message:"+ res


##demo of the query using a string:
err, res1 = client.query('52e19220bef627683c79c3a6','SELECT * WHERE {  ?subject rdf:type ?class} LIMIT 10')
if not err:
    print "\n\n"
    print "RESULT 1:"
    print res1
else:
    print err


##query using a dict:
opt = {'collection':"abuse_entries_2014_12", 'query':'{}', 'limit':10,'skip':0}
err, res2 = client.query('54eb0a1d590ea23530f24644', opt)
if not err:
    print "\n\n"
    print "RESULT 2:"
    print res2
else:
    print err
##


def callback(err, data,socket):
        if not err:
                print 'data:'+data
#                socket.emit("stop")
#                print "stopped"
        else:
            print err

client.openStream('54eb13d7590ea23530f24645','logs',callback)
#client.openStream('543e79000124b4b01c40612f','wikipedia_hose',callback)



