from http.server import BaseHTTPRequestHandler
import requests, json, base64, sys
import pickle

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
   
        data = self.rfile.read(int(self.headers['content-length']))
        kwargs = json.loads(data)
        kwargs['data'] = base64.b64decode(kwargs['data'])
        for i,v in kwargs.items():
         print(" ",i,": ",v)

        try:
            req = requests.request(**kwargs, verify=False, allow_redirects=False)
            serializedReq = pickle.dumps(req)

            self.send_response(200)
            self.end_headers()
         #  self.wfile.write(base64.b64encode(serializedReq).decode("utf-8"))
            self.wfile.write(base64.b64encode(serializedReq))
        
        except Exception as e:#可以以集群方式返回结果抛出异常
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(exc_value).encode().decode("utf-8"))
        
        return

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())
        return