from fastapi import FastAPI
import uvicorn

from domain.picture import picture_router
from domain.member import member_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(member_router.router)
app.include_router(picture_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)