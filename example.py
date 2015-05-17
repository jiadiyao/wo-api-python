from wo import WO 


client = WO('http://webobservatory.soton.ac.uk', '55590b16a7f6527a06ebe96d', 'e4b72c8cb25d32ba', 'jiadi.yao@gmail.com','qwer1234' )


client.login()
#client.query('52e19220bef627683c79c3a6','SELECT * WHERE {  ?subject rdf:type ?class} LIMIT 10')

opt = {'collection':"abuse_entries_2014_12", 'query':'{}', 'limit':10,'skip':0}
#client.query('54eb0a1d590ea23530f24644', opt)

def callback(data,socket):
        print 'data'+data
        print 'socket:'+socket
client.openStream('54eb13d7590ea23530f24645','logs',callback)



