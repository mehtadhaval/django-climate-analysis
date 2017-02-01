import contextlib
import logging
import os
import tempfile

import requests

from climate_analysis.celery import app
from climate_data import reader
from climate_data.models import Request
from climate_data.processors import ClimateDataHandler

logger = logging.getLogger(__name__)


@app.task(bind=True)
def process_request(self, request_id):
    request = Request.objects.filter(status=Request.STATUS_SUBMITTED, id=request_id).first()
    if not request:
        return

    request.status = Request.STATUS_PROCESSING
    request.save()
    file_name = None
    try:
        # download file in a temporary location
        response = requests.get(request.url, stream=True)
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file_name = file.name
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        handler = ClimateDataHandler()
        with reader.ClimateDataFileReader(file_name) as file:
            for record in file:
                handler.process(record, request.type, request.region)

    except Exception as e:
        logger.exception("Error occurred while processing request")
        request.status = Request.STATUS_FAILED
        request.save()
    else:
        request.status = Request.STATUS_COMPLETED
        request.save()
    finally:
        if file_name:
            with contextlib.suppress(OSError):
                os.remove(file_name)
