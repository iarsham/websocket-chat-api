from logging import getLogger
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.commons.config import settings
from app.commons.db import async_session, engine, async_engine

logger = getLogger(name=__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS
)


@app.on_event(event_type="startup")
async def run_async_engine() -> None:
    async with async_session() as session:
        query = text("SELECT current_timestamp;")
        result = await session.execute(statement=query)
        result = result.scalar()
        logger.warning(f"Connected to db now! : {result.isoformat()}")


@app.on_event(event_type="shutdown")
async def close_db_engine() -> None:
    await async_engine.dispose()
    engine.dispose()
    logger.warning("Postgres connections closed.")


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url=app.docs_url)
