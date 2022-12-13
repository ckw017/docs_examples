from fastapi import FastAPI
from ray import serve
import time
import os

# Use this var to test service inplace update. When the env var is updated, users see new return value.
msg = os.getenv("SERVE_RESPONSE_MESSAGE", "Hello world!")

serve.start(detached=True)

app = FastAPI()

@serve.deployment(route_prefix="/")
@serve.ingress(app)
class HelloWorld:
    @app.get("/")
    def hello(self):
        time.sleep(90)
        return msg
    
    @app.get("/slowbro")
    def hello(self):
        time.sleep(300)
        return msg
    
    @app.get("/slowking")
    def hello(self):
        time.sleep(1800)
        return msg
    
    @app.get("/healthcheck")
    def healthcheck(self):
        return

HelloWorld.deploy()
