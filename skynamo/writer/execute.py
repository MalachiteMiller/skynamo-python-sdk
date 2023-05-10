import math

from .WriteOperationCls import WriteOperation
from ..shared.api import makeRequest, SkynamoApiException
from ..shared.helpers import setup_logger
from typing import List, Union
from time import sleep
import json


logger = setup_logger()


def executeWrites(write_operations: List[WriteOperation], verbose, key: str = None,
                  retry: bool = True, timeout: int = None):
    write_groups = []
    for write in write_operations:
        found = False
        if not write.can_be_combined:
            write_groups.append(write)
            continue
        for writeBatch in write_groups:
            if writeBatch[0].dataType == write.dataType and writeBatch[0].httpMethod == write.httpMethod:
                writeBatch.append(write)
                found = True
                break
        if not found:
            write_groups.append([write])

    errors = []
    for writes in write_groups:
        body = []
        if isinstance(writes, list):
            http_method = writes[0].httpMethod
            data_type = writes[0].dataType
            for write in writes:
                body.append(write.itemOrId)
        else:
            body.append(writes.itemOrId)
            http_method = writes.httpMethod
            data_type = writes.dataType

        retries = [.5, 1, 2, 4, 8, 16, 32, 32, 32, 32, 32, 32,
                   32, 32, 32, 32, 32, 64, 128, 128, 0]  # last one makes the loop happy, doesn't need to sleep
        if retry:
            for sleep_time in retries:
                try:
                    makeRequest(http_method, data_type, data=json.dumps(body), verbose=verbose, key=key, timeout=timeout)
                    break
                except SkynamoApiException as e:
                    if e.status_code != 429:
                        if sleep_time:
                            logger.warning(f"Retrying {http_method} {data_type} due to {e.status_code} error")
                            sleep(sleep_time)
                            continue
                        else:
                            logger.critical(f'Too many retries on a write, last error: {e.status_code}. {http_method}'
                                            f' {data_type} {body}')
                            errors.append(body)
                    else:
                        logger.critical(f'Error on write: {e.status_code}. {http_method} {data_type} {body}')
                        raise e
        else:
            makeRequest(http_method, data_type, data=json.dumps(body), verbose=verbose, key=key, timeout=timeout)
    return errors
