from os.path import exists
from os import remove
import logging
import json
# from datetime import datetime
from relionai.aws_logging_handlers.S3 import S3Handler


class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
    def format(self, record):
        record.msg = json.dumps(record.msg)
        return super().format(record)


class MonitoringSession:
    def __init__(self, account_name, model_owner, model_name, time_rotation=43200):
        clean_account_name = account_name.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
        clean_model_owner = model_owner.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
        clean_model_name = model_name.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
        self.account_name = clean_account_name
        self.model_owner= clean_model_owner
        self.model_name= clean_model_name
        self.time_rotation = time_rotation
        self.wizard_logger = None

    def __enter__(self):
        bucket="wizard-config" # The bucket should already exist
        # The log will be rotated to a new object either when an object reaches 100 MB or when 12h pass from the last rotation/initial logging
        s3_handler = S3Handler(key=f"{self.account_name}/{self.model_owner}/{self.model_name}", chunk_size=2*1024**2, bucket=bucket, time_rotation=self.time_rotation, max_file_size_bytes=104857600, encoder='utf-8')
        s3_handler.setFormatter(JSONFormatter())
        wizard_logger = logging.getLogger(f"wizard_{__name__}")
        # logger.setFormatter(JSONFormatter())
        wizard_logger.setLevel(logging.INFO)
        wizard_logger.addHandler(s3_handler)
        self.wizard_logger = wizard_logger
        return self

    def logging(self, pdf):
        result = pdf.to_dict(orient="records")
        self.wizard_logger.info(result)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass