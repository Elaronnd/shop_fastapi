import uvicorn
from app import app
import ngrok

if __name__ == "__main__":
    listener = ngrok.forward(8000, authtoken='2tlc6JUrKUfvbHo3joXGJewqZzQ_7MqWFcG4KipaftHdqzJuA')
    print(listener.url())
    uvicorn.run(app=app, host="0.0.0.0")