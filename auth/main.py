from fastapi import FastAPI
from routes.userRoutes import userRouter
app = FastAPI()
app.include_router(userRouter)



