# -*- coding: utf-8 -*-
import argparse
import uvicorn
from fastapi import FastAPI

from ai_route import ai_router


def create_app(run_mode: str = None):
    app = FastAPI(debug=True)

    app.include_router(ai_router)

    return app


def run_api(host, port, **kwargs):
    uvicorn.run(app, host=host, port=port)


app = create_app()


if __name__ == "__main__":    
    parser = argparse.ArgumentParser(
        prog="azim-ai",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9988)
    args = parser.parse_args()

    run_api(host=args.host, port=args.port,)
