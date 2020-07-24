import os

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.crm.asgi:app",
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "8000")),
    )
