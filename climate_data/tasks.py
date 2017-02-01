import contextlib
import logging
import os
import tempfile
from datetime import date

import requests
from django.conf import settings
from elasticsearch import Elasticsearch

from climate_analysis.celery import app
from climate_data import reader
from climate_data.models import Request, ClimateData, ClimateTimeSeriesData

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

        with reader.ClimateDataFileReader(file_name) as file:
            es = Elasticsearch(hosts=[settings.ES_URL], verify_certs=False)
            for record in file:
                ClimateData.objects.update_or_create(
                    region_id=request.region_id, type=request.type, year=record.get('year'),
                    defaults=record
                )
                # store data in timeseries table
                for month in range(1, 13):
                    record_date = date(int(record.get("year")), month, 1)
                    month_name = record_date.strftime("%b").lower()
                    obj, created = ClimateTimeSeriesData.objects.update_or_create(
                        region_id=request.region_id, type=request.type, record_date=record_date,
                        defaults={
                            'measurement': record.get(month_name)
                        }
                    )
                    es.index(index="climate_data", doc_type=request.type, id=obj.id, body={
                        "measurement": float(obj.measurement),
                        "region": obj.region.name,
                        "record_date": obj.record_date
                    })
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
