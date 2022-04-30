from http.server import BaseHTTPRequestHandler
import requests, json, base64, sys
import pickle

class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    print(self.headers)
    print(self.command)
    data = self.rfile.read(int(self.headers['content-length']))
    kwargs = json.loads(data)
    kwargs['data'] = base64.b64decode(kwargs['data'])

    try:
        req = requests.request(**kwargs, verify=False, allow_redirects=False)
        serializedReq = pickle.dumps(req)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(base64.b64encode(serializedReq).decode("utf-8"))
        
    except Exception as e:#可以以集群方式返回结果抛出异常
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str(exc_value).encode().decode("utf-8"))
        
    return