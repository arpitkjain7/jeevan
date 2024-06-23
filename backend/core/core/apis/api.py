from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from core.apis.routes.users_router import user_router
from core.apis.routes.pmr_router import pmr_router
from core.apis.routes.patient_router import patient_router
from core.apis.routes.hip_router import hip_router
from core.apis.routes.gatewayInteraction_router import gateway_router
from core.apis.routes.callback_router import callback_router
from core.apis.routes.common_router import common_router
from core.apis.routes.hid_router import hid_router
from core.apis.routes.dataTransfer_router import dataTransfer_router
from core.apis.routes.appointment_router import appointment_router
from core.apis.routes.hiu_router import hiu_router
from core.apis.routes.abdm_wrapper import abdm_router
from core.apis.routes.ai_router import ai_router

"""
from core.apis.routes.listOfComplaints_router import listOfComplaint_router
from core.apis.routes.listOfDiagnosis_router import listOfDiagnosis_router
from core.apis.routes.listOfMedicalTests_router import listOfMedicalTests_router
from core.apis.routes.listOfMedicines_router import listOfMedicines_router
"""

# from core.apis.routes.event_router import event_router
# from core.apis.routes.annotation_router import annotation_router


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


app.include_router(user_router, tags=["Authentication"])
app.include_router(hid_router, tags=["ABHA Registration"])
app.include_router(appointment_router, tags=["Appointments"])
app.include_router(pmr_router, tags=["Patient Medical Record"])
app.include_router(patient_router, tags=["Patient Details"])
app.include_router(hip_router, tags=["HIP Records"])
app.include_router(gateway_router, tags=["Gateway Interactions"])
app.include_router(callback_router, tags=["Callback"])
app.include_router(dataTransfer_router, tags=["Data Transfer"])
app.include_router(hiu_router, tags=["HIU Routers"])
app.include_router(common_router, tags=["Common"])
app.include_router(ai_router, tags=["AI Engine"])
app.include_router(abdm_router, tags=["ABDM Wrapper"])

"""
app.include_router(listOfComplaint_router, tags=["Common"])
app.include_router(listOfDiagnosis_router, tags=["Common"])
app.include_router(listOfMedicalTests_router, tags=["Common"])
app.include_router(listOfMedicines_router, tags=["Common"])
"""


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
        title="CliniQ360 - Lobster",
        version="0.1 - Beta",
        description="ABDM complaint HIMS System for hospitals",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
