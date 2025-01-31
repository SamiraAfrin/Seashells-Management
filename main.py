import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=7777, reload=True)
