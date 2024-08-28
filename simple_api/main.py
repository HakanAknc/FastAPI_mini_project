from fastapi import FastAPI

# FastAPI uygulamasını başlat
app = FastAPI()

# Basit bir "Merhaba, Dünya!" endpointi
@app.get("/")
def read_root():
    return {"message": "Merhaba Dünya!"}