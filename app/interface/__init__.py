from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title='API',
              description='',
              version='0.1')

# from .controllers import controller

# api.include_router(controller.router,
                   # prefix='/api/v1/controller',
                   # tags=['controller'])

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
