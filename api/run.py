import uvicorn

from src.config import load_configuration
from src.create_app import create_app


config = load_configuration()
app = create_app(config)


if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host=config.server.host,
        port=config.server.port,
        reload=config.debug,
    )
