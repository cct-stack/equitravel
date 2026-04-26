"""Entry point — `uvicorn api.main:app`."""

from api.app import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    from api.config import HOST, PORT
    uvicorn.run("api.main:app", host=HOST, port=PORT, reload=True)
