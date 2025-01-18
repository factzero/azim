import argparse
import uvicorn
from fastapi import FastAPI

from imgs_route import imgs_router
from db.base import create_tables


def create_app(run_mode: str = None):
    app = FastAPI(title="Test", debug=True)

    app.include_router(imgs_router)

    return app


def run_api(host, port, **kwargs):
    uvicorn.run(app, host=host, port=port)


app = create_app()


if __name__ == "__main__":    
    create_tables()
    
    parser = argparse.ArgumentParser(
        prog="Test",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7861)
    args = parser.parse_args()

    run_api(host=args.host, port=args.port,)
