import requests
import json
from socketIO_client import SocketIO, LoggingNamespace
import urllib3
urllib3.disable_warnings()

class WO:
    def __init__(self, base, client_id, client_secret, username, password):
    
        self.base = base ## base is in the format of http://webobservatory.soton.ac.uk
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.accessToken=''
        
        
    def login(self):
        tokenurl = self.base+'/oauth/token'
        parameters = {'grant_type':'password','client_id':self.client_id, 'client_secret':self.client_secret, 'username':self.username, 'password':self.password}
        
        r = requests.post(tokenurl, data=parameters)
        print r.status_code
        print r.url
        print r.headers
        print r.content
        
        if (r.status_code == 200):
            data = json.loads(r.content)
            self.accessToken = data['access_token']
        


    #query a dataset identified by dataset id
    #options can be a string representing the query : options = 'SELECT * WHERE {  ?subject rdf:type ?class} LIMIT 10'
    ## or a dictionary: options = {'collection':"abuse_entries_2014_12", 'query':'{}', 'limit':10,'skip':0}
    def query(self, id, options):
        try:
            if options['query']:
                d = options
        except:
            ##options is an string
            d = {'query':options}
        #print d
        if (self.accessToken):
            url= self.base +'/api/wo/'+ id + '/endpoint'
            headers={ 'Authorization': 'Bearer ' + self.accessToken}
            r= requests.get(url,params=d, headers=headers)
            print r.status_code
            print r.url
            print r.headers
            print r.content
            
        
        
    #id: dataset id;
    #options: AMQP exchange name
    #callback(err,data,stream)
    def openStream(self, id, options, callback):
        try:
            if options['query']:
                d = options
        except:
            ##options is an string
            d = {'query':options}


        if (self.accessToken):
            url= self.base +'/api/wo/'+ id + '/endpoint'
            headers={ 'Authorization': 'Bearer ' + self.accessToken}
            r= requests.get(url,params=d, headers=headers)
            
            if (r.status_code == 200):
                sid = r.content
                print sid
                def process(data):
                    print 'here'
                    print data
                    #callback(data)
                with SocketIO('https://webobservatory.soton.ac.uk/', 443, LoggingNamespace) as socketIO:
                    socketIO.on('chunk',process)
                #socketIO.wait(seconds=1)


'''
		if (token)
		{
			$.ajax(
			{
				type: 'get',
				url: woHost +'/api/wo/'+ id + '/endpoint',
				data: opts,
				headers:
				{
					Authorization: 'Bearer ' + token
				}
			}).done(function(sid)
				{
					//console.log(callback);
					if (sid){
						//try to get the stream data use socket.io
						var socket = io.connect('https://webobservatory.soton.ac.uk/' + sid);
						//console.log(socket);
						
						socket.on('chunk', function (data) {
						//console.log(data);
						
						//return the data and the stream object
						callback(null,data,socket);
						
						});
						
						//add this stream to datastreams variable
						
						if (typeof datastreams[id] == "undefined")
						{
							
							datastreams[id] = [socket];
							
						}
						else
						{
							
							datastreams[id].push(socket);
						}
						
						
						
					}
				}
				);

			
			//console.log(id);
			//console.log(options);
			//console.log(woHost +'/api/wo/'+ id + '/endpoint');
			
		}
		else
		{
			//TODO return an error code via callback
			//console.log("need to login before making query");
			callback("Not logged in");
			location.href=authURL;
		} 
'''
        
        
        
        
        
        
        
