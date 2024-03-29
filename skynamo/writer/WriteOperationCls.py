from typing import Literal, Union


class WriteOperation:
    def __init__(self, dataType: str, httpMethod: Literal['post', 'patch', 'put', 'delete'], itemOrId: Union[dict, str],
                 can_be_combined=True):
        self.dataType = dataType
        self.httpMethod = httpMethod
        self.itemOrId = itemOrId
        self.can_be_combined = can_be_combined
