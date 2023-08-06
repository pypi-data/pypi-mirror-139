# pylint: skip-file
import os

import uvicorn

from unimatrix.ext import webapi

os.environ.setdefault('APP_ROLE', 'listener')
os.environ.setdefault('UNIMATRIX_SETTINGS_MODULE', __name__)

app = webapi.application_factory(allowed_hosts="*")

if __name__ == '__main__':
    uvicorn.run(app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
