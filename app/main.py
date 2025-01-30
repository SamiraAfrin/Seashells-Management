from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/")
def hello():
    data = "Hello world!"
    return Response(content=data, media_type="text/plain")