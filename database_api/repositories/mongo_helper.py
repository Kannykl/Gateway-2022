import json
from bson import json_util


def parse_objects(data) -> list:
    """Transforms bson mongo format to json.

    Args:
        data: documents from mongodb

    Returns:
        documents in json format
    """
    return json.loads(json_util.dumps(data))
