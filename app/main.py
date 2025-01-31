from fastapi import FastAPI, Response
from app.delivery.seashells import seashell_router

app = FastAPI()
app.include_router(seashell_router)


@app.get("/")
def status():
    # data = "Hello world!"
    # return Response(content=data, media_type="text/plain")

    return "Program is running"
