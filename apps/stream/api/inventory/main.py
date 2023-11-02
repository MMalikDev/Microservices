import uvicorn
from config.core import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.endpoints import products

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(products.router, tags=["products"], prefix="/products")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        use_colors=True,
    )
