import uvicorn

from app.app import app

if __name__ == "__main__":

    uvicorn.run("main:app", reload=True, use_colors=True, host="0.0.0.0", port=8000)
