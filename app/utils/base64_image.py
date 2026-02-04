def extract_base64_image(base64_string: str) -> bytes:
    if not base64_string:
        raise ValueError("Image data is empty")

    if "," in base64_string:
        base64_string = base64_string.split(",", 1)[1]
    return base64_string
