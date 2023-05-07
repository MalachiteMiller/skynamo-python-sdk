from .WriteOperationCls import WriteOperation
from ..shared.api import makeRequest, SkynamoApiException
from typing import List, Union
from time import sleep


def executeWrites(write_operations: List[WriteOperation], verbose, key: str = None):
    for write in write_operations:
        __make_write_request(write, verbose, key)


def __make_write_request(write_operation: Union[WriteOperation, List[WriteOperation]], verbose, key: str = None):
    body = []
    if isinstance(write_operation, list):
        http_method = write_operation[0].httpMethod
        data_type = write_operation[0].dataType
        for write in write_operation:
            body.append(write.itemOrId)
    else:
        body = write_operation.itemOrId
        http_method = write_operation.httpMethod
        data_type = write_operation.dataType

    retries = [.5, 1, 2, 4, 8, 16, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 64, 128, 128]
    for sleep_time in retries:
        try:
            makeRequest(http_method, data_type, data=str(body), verbose=verbose, key=key)
            break
        except SkynamoApiException as e:
            if e.status_code >= 500 or e.status_code == 429:
                print(f"Retrying {http_method} {data_type} {body} due to {e.status_code} error")
                sleep(sleep_time)
                continue
    else:
        raise SkynamoApiException('Too many retries on a write')
