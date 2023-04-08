from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from core.apis.routes.user_router import user_router
from core.apis.routes.event_router import event_router
from core.apis.routes.annotation_router import annotation_router


app = FastAPI(
    title="albumDekho",
    version="0.1 - Beta",
    description="An Image sorting and sharing engine",
    redoc_url="/documentation",
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, tags=["authentication"])
app.include_router(event_router, tags=["event_management"])
app.include_router(annotation_router, tags=["annotation_management"])


@app.get("/")
def ping():
    """[ping func provides a health check]

    Returns:
        [dict]: [success response for health check]
    """
    return {"response": "ping to find my photos backend server successful"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="albumDekho",
        version="0.1 - Beta",
        description="An Image sorting and sharing engine",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
