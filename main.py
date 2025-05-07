import uvicorn
from app import app
import ngrok
from app.config.config import AUTH_NGROK

if __name__ == "__main__":
    listener = ngrok.forward(8000, authtoken=AUTH_NGROK)
    print(listener.url())
    uvicorn.run(app=app, host="0.0.0.0")