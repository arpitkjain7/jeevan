import uvicorn
from core.apis.api import app
from mangum import Mangum

handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
