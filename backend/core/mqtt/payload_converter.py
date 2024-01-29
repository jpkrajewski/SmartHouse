def convert(payload: str):
    """Simple payload converter for MQTT message, <[ID]#[TYPE_OF_VALUE]#[VALUE]>"""
    _id, _type, value = payload.split("#")
    return {"device_id": _id, "type": _type, "value": value}
