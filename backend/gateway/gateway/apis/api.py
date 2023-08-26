from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi


from gateway.apis.routes.context_callback_router import patient_context_router
from gateway.apis.routes.dataTransfer_callback_router import (
    dataTransfer_callback_router,
)
from gateway.apis.routes.hiu_callback_router import hiu_callback_router
from gateway.apis.routes.patient_callback_router import patient_callback_router
from gateway.apis.routes.registration_callback_router import (
    registeration_callback_router,
    heartbeat_callback_router,
)

app = FastAPI(
    title="CliniQ360 - Lobster",
    version="0.1 - Beta",
    description="ABDM complaint HIMS System for hospitals",
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


app.include_router(patient_context_router, tags=["Patient Callback"])
app.include_router(dataTransfer_callback_router, tags=["Data Transfer Callback"])
app.include_router(hiu_callback_router, tags=["HIU Callback"])
app.include_router(patient_callback_router, tags=["Patient Callback"])
app.include_router(registeration_callback_router, tags=["Registeration Callback"])
app.include_router(heartbeat_callback_router, tags=["Heartbeat"])


@app.get("/")
def ping():
    """[ping func provides a health check]

    Returns:
        [dict]: [success response for health check]
    """
    return {"response": "ping to CliniQ360 backend server successful"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CliniQ360 - Lobster - Callback",
        version="0.1 - Beta",
        description="ABDM complaint HIMS System for hospitals",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
