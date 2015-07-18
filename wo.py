import requests
import json
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
#import urllib3
#urllib3.disable_warnings()
import logging
###uncomment for printing debug info
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
logging.captureWarnings(True)


class WO:
    def __init__(self, hostname, client_id, client_secret, username, password):

        self.hostname = hostname
        self.base = "https://"+hostname ## self.base contains protocol
        self.port = 443


        h = hostname.split(':')
#        print len(h)
        if len(h)==2:
                self.hostname = h[0]
                self.port = int(h[1])
                self.base = "https://"+h[0]

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.accessToken=''


    def login(self):
        tokenurl = self.base+':'+str(self.port)+'/oauth/token'
        parameters = {'grant_type':'password','client_id':self.client_id, 'client_secret':self.client_secret, 'username':self.username, 'password':self.password}

        r = requests.post(tokenurl, data=parameters, verify=False)
#        print r.status_code
#        print r.url
#        print r.headers
#        print r.content

        if (r.status_code == 200):
            data = json.loads(r.content)
            self.accessToken = data['access_token']
            return ''
        else:
            return "[ERROR] Login Failed: Failed to obtain access token."

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
            url= self.base+':'+str(self.port) +'/api/wo/'+ id + '/endpoint'
            headers={ 'Authorization': 'Bearer ' + self.accessToken}
            r= requests.get(url,params=d, headers=headers,verify=False)
#            print r.status_code
#            print r.url
#            print r.headers
#            print r.content
            return '', r.content
        else:
            return "[ERROR] Query Failed:  No access token. Try  wo.login() first. ", None


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
            url= self.base+':'+str(self.port)+'/api/wo/'+ id + '/endpoint'
            headers={ 'Authorization': 'Bearer ' + self.accessToken}
            
            r= requests.get(url,params=d, headers=headers, verify=False)
            
        if ('r' in locals() and r.status_code == 200):
                sid = r.content
#                print "sid:---"+sid
#                sio = 'http://webobservatory.soton.ac.uk'#+sid
                #sio = 'dev-001.ecs.soton.ac.uk'
                #print sio
#                class Namespace(BaseNamespace):
#                    def on_connect(self):
#                        print '[Connected]'

                class dataNamespace(BaseNamespace):
                    #def on_aaa_response(self, *args):
                    #    print('on_aaa_response', args)
                    def on_connect(self):
                        print '[Connected]'
                        pass

                def process(data):
#                    print "process data"
#                    print data
                    callback(False, data,socketIO)


#               socketIO = SocketIO(sio,443,LoggingNamespace,verify=False)
                socketIO = SocketIO(self.base,self.port, verify=False)
#                socketIO = SocketIO(self.base, 9090)
                data_namespace = socketIO.define(dataNamespace,'/'+sid)


                #data_namespace.emit('stop')
                data_namespace.on('chunk',process)
#                data_namespace.emit('stop')
#                socketIO.emit("stop")
#                socketIO.wait(seconds=1)
#                data_namespace.wait()
                socketIO.wait()
        else:
            callback("[ERROR] Open Stream Failed: Stream opening failed for:"+id,None,None)










