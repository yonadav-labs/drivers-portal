import os
import tempfile

try:
    ## TODO replace for orjson
    # https://pypi.org/project/orjson/
    import rapidjson as json
except ImportError:
    import json


from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from sodapy import Socrata

import requests
import xlrd

try:
    NYC_OPEN_DATA_API_TOKEN = getattr(settings, "NYC_OPEN_DATA_API_TOKEN")
    NYC_OPEN_DATA_API_USER = getattr(settings, "NYC_OPEN_DATA_API_USER")
    NYC_OPEN_DATA_API_PASSWORD = getattr(settings, "NYC_OPEN_DATA_API_PASSWORD")
except AttributeError:
    raise ImproperlyConfigured("Some NYC Open data api credentials not configured.")

from importer.constants import (
    NYC_API_MEDALLION_DRIVERS_DATASET_ID,
    NYC_API_FOR_HIRE_VEHICLES_DATASET_ID,
)


class BaseImporterClient:
    limit = 0

    def get_count(self):
        raise NotImplementedError

    def get(self, offset):
        raise NotImplementedError


def nyc_data_api_client_factory(dataset_id):
    return SocrataClient(dataset_id)


class SocrataClient(BaseImporterClient):
    NYC_OPEN_DATA_API_TOKEN = NYC_OPEN_DATA_API_TOKEN
    NYC_OPEN_DATA_API_USER = NYC_OPEN_DATA_API_USER
    NYC_OPEN_DATA_API_PASSWORD = NYC_OPEN_DATA_API_PASSWORD
    NYC_DATASET_SOURCE = "data.cityofnewyork.us"
    NYC_API_MEDALLION_DRIVERS_DATASET_ID
    NYC_API_FOR_HIRE_VEHICLES_DATASET_ID

    limit = 1000

    def __init__(self, dataset_id):
        self._dataset_id = dataset_id
        self._client = Socrata(
            self.NYC_DATASET_SOURCE,
            NYC_OPEN_DATA_API_TOKEN,
            username=self.NYC_OPEN_DATA_API_USER,
            password=self.NYC_OPEN_DATA_API_PASSWORD,
        )

    def _get(self, dataset_id, **kwargs):
        return self._client.get(dataset_id, **kwargs)

    def _get_paginated(self, dataset_id, offset, limit=None):
        _pagination = self._pagination_q(offset, limit)
        return self._get(dataset_id, **_pagination)

    def _pagination_q(self, offset, limit=None):
        return {"limit": limit or self.limit, "offset": offset, "order": ":id"}

    def _count_q(self):
        return {"select": "count(*) as amount"}

    @property
    def get_dataset_id(self):
        return self._dataset_id

    def get_count(self):
        result = self._get(self.get_dataset_id, **self._count_q())[0]
        return int(result["amount"])

    def get(self, offset, limit=None):
        return self._get_paginated(self.get_dataset_id, offset, limit)


def download_xls_client_factory(source_url, header):
    return XlsxImporterClient(source_url=source_url, header=header)


def download_fast_xls_client_factory(source_url, header):
    return FastXlsxImporterClient(source_url=source_url, header=header)


class XlsxRowItem:
    __slots__ = [
        "tlc_license_type",
        "tlc_license_number",
        "dmv_plate",
        "vin",
        "automobile_insurance_code",
        "automobile_insurance_name",
        "automobile_insurance_policy_number",
        "vehicle_owner_name",
        "affiliated_base_or_taxi_agent_or_fleet_license_number",
    ]

    def __init__(
        self,
        *,
        tlc_license_type,
        tlc_license_number,
        dmv_plate,
        vin,
        automobile_insurance_code,
        automobile_insurance_name,
        automobile_insurance_policy_number,
        vehicle_owner_name,
        affiliated_base_or_taxi_agent_or_fleet_license_number
    ):
        self.tlc_license_type = tlc_license_type
        self.tlc_license_number = tlc_license_number
        self.dmv_plate = dmv_plate
        self.vin = vin
        self.automobile_insurance_code = automobile_insurance_code
        self.automobile_insurance_name = automobile_insurance_name
        self.automobile_insurance_policy_number = automobile_insurance_policy_number
        self.vehicle_owner_name = vehicle_owner_name
        self.affiliated_base_or_taxi_agent_or_fleet_license_number = (
            affiliated_base_or_taxi_agent_or_fleet_license_number
        )

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
        data = dict()
        for var in self.__slots__:
            data[var] = getattr(self, var)
        return data


class FastXlsxImporterClient(BaseImporterClient):
    limit = 5000

    def __init__(self, *, source_url, header, ignore_header_lines=1):
        self._header = header
        self._source = source_url
        self._filepath = None
        self._ignore_lines = ignore_header_lines
        self._data = None
        # This will download the file
        self._get_file(self._source)

    @property
    def data(self):
        if not self._data:
            _book = xlrd.open_workbook(self._filepath)
            sheet = _book.sheet_by_index(0)
            self._data = self._get_data(sheet)
            del sheet
            del _book
        return self._data

    def _get_data(self, sheet):
        _max_row = sheet.nrows

        def _create_row_item(idx):
            row_values = sheet.row_values(idx, start_colx=0)
            return XlsxRowItem(
                tlc_license_type=row_values[0],
                tlc_license_number=row_values[1],
                dmv_plate=row_values[2],
                vin=row_values[3],
                automobile_insurance_code=row_values[4],
                automobile_insurance_name=row_values[5],
                automobile_insurance_policy_number=row_values[6],
                vehicle_owner_name=row_values[7],
                affiliated_base_or_taxi_agent_or_fleet_license_number=row_values[8],
            )

        return [
            _create_row_item(row_idx) for row_idx in range(self._ignore_lines, _max_row)
        ]

    def _get_file(self, source):
        response = requests.get(source, stream=True)
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, buffering=0) as fd:
            for chunk in response.iter_content(chunk_size=512):
                fd.write(chunk)
            self._filepath = fd.name

    def _get_paginated(self, offset, limit=None):
        _limit = limit or self.limit
        _offset = offset
        _end_row = _offset + _limit

        return (xlsx_row for xlsx_row in self.data[_offset:_end_row])

    def get_count(self):
        _data_length = len(self.data)
        return _data_length

    def get(self, offset, limit=None):
        return self._get_paginated(offset, limit)


class XlsxImporterClient(BaseImporterClient):
    limit = 5000

    def __init__(self, *, source_url, header, ignore_header_lines=1):
        self._header = header
        self._source = source_url
        self._filepath = None
        self._ignore_lines = ignore_header_lines
        self._max_row = None
        self._book = None
        # This will download the file
        self._get(self._source)

    @property
    def book(self):
        if not self._book:
            self._book = xlrd.open_workbook(self._filepath)
        return self._book

    @property
    def sheet(self, *, sheet_index=0):
        return self.book.sheet_by_index(sheet_index)

    def _get(self, source):
        response = requests.get(source, stream=True)
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, buffering=0) as fd:
            for chunk in response.iter_content(chunk_size=512):
                fd.write(chunk)
            self._filepath = fd.name

    def _get_paginated(self, offset, limit=None):
        _limit = limit or self.limit
        _offset = offset
        _end_row = _offset + _limit

        # Avoid retrieving headers
        if _offset == 0 and self._ignore_lines > 0:
            _offset = self._ignore_lines

        # get_count recalculates _max_row
        if self._max_row is None:
            self.get_count()

        # Avoid out of range
        if _end_row > self._max_row:
            _end_row = self._max_row

        def _merge_headers(items):
            return dict(zip(self._header, items))

        return (
            _merge_headers(row)
            for row in RowRange(sheet=self.sheet, start_row=_offset, end_row=_end_row)
        )

    def get_count(self):
        if not self.sheet:
            self._max_row = 0
            return self._max_row
        self._max_row = self.sheet.nrows - 1
        return self._max_row

    def get(self, offset, limit=None):
        return self._get_paginated(offset, limit)


class RowRange:
    """
    for row in RowRange(sheet=sheet, start_row=2, end_row=5):
        ...row...
    """

    def __init__(self, *, sheet, start_row, end_row):
        self.sheet = sheet
        self.start_row = start_row
        self.end_row = end_row
        self.row_count = self.start_row - 1  # First iteration

    def __iter__(self):
        return self

    def __next__(self):
        self.row_count += 1
        if self.row_count > self.end_row:
            raise StopIteration()
        # return self.sheet.row_slice(self.row_count, start_colx=0)
        return self.sheet.row_values(self.row_count, start_colx=0)
