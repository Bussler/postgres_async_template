import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="TEMPLATE APP", lifespan=lifespan)
app.include_router(api_router, prefix="/api")

# CORS
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    uvicorn.run("app.main:app", host="localhost", port=8001, reload=True)
    
if __name__ == "__main__":
    main()