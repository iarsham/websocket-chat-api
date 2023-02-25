from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url=app.docs_url)
