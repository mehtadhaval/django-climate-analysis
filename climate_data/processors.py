import logging
from datetime import date

from django.conf import settings
from elasticsearch.client import Elasticsearch

from climate_data.models import ClimateData, ClimateTimeSeriesData

logger = logging.getLogger(__name__)


class ClimateDataProcessor(object):
    """
    Base class that defines the processor interface
    """

    def process(self, record, type, region):
        """
        process a single record
        """
        pass

    def process_normalized_data(self, record, type, region, month):
        """
        process normalized month-wise data
        """
        pass


class DataStoreProcessor(ClimateDataProcessor):
    """
    Store in ClimateData model
    """

    def process(self, record, type, region):
        ClimateData.objects.update_or_create(
            region_id=region.id, type=type, year=record.get('year'),
            defaults=record
        )


class TimeSeriesDataStoreProcessor(ClimateDataProcessor):
    """
    Store in ClimateData model
    """

    def process_normalized_data(self, record, type, region, month):
        record_date = date(int(record.get("year")), month, 1)
        month_name = record_date.strftime("%b").lower()
        ClimateTimeSeriesData.objects.update_or_create(
            region_id=region.id, type=type, record_date=record_date,
            defaults={
                'measurement': record.get(month_name)
            }
        )


class ESInitializerMixin(object):
    """
    Initializes and assigns an ES connection instance
    """

    def __init__(self):
        self._es = Elasticsearch(hosts=[settings.ES_URL], verify_certs=False)


class ESTimeSeriesDataStoreProcessor(ESInitializerMixin, ClimateDataProcessor):
    def process_normalized_data(self, record, type, region, month):
        record_date = date(int(record.get("year")), month, 1)
        month_name = record_date.strftime("%b").lower()
        obj_id = "{type}.{month}{year}.{region}".format(
            type=type, month=month, region=region.name, year=record_date.year
        )
        try:
            self._es.index(index="climate_data", doc_type=type, id=obj_id, body={
                "measurement": float(record.get(month_name)),
                "region": region.name,
                "record_date": record_date
            })
        except Exception:
            logger.exception("Error while indexing Timeseries data to ES. ID %s", obj_id)


class ESNormalizedDataStoreProcessor(ESInitializerMixin, ClimateDataProcessor):
    """
    Stores data in normalized format, i.e. single record for a month with other data stored as a column
    """

    def process_normalized_data(self, record, type, region, month):
        record_date = date(int(record.get("year")), month, 1)
        month_name = record_date.strftime("%b").lower()
        obj_id = "{region}.{month}{year}".format(
            month=month, year=record_date.year, region=region.name
        )
        try:
            self._es.update(index="climate_data", doc_type="normalized_data", id=obj_id, body={
                "doc": {
                    type.lower(): float(record.get(month_name)),
                    "region": region.name,
                    "record_date": record_date
                },
                "doc_as_upsert": True  # index a new doc if doesn't exist
            })
        except Exception:
            logger.exception("Error while indexing Normalized climate data to ES. ID %s", obj_id)


class ClimateDataHandler(object):
    # define pipeline here
    _processors = (
        DataStoreProcessor,
        TimeSeriesDataStoreProcessor,
        ESTimeSeriesDataStoreProcessor,
        ESNormalizedDataStoreProcessor
    )

    def __init__(self):

        # initialize process pipeline
        self._pipeline = [
            cls() for cls in self._processors
            ]

    def process(self, record, type, region):

        for processor in self._pipeline:
            processor.process(record, type, region)
            for month in range(1, 13):
                processor.process_normalized_data(record, type, region, month)
