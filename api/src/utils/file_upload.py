def get_image_mime_type(extension: str) -> str:
    mapping = {
        'apng': 'apng',
        'avif': 'avif',
        'gif': 'gif',
        'jpg': 'jpeg',
        'jpeg': 'jpeg',
        'jfif': 'jpeg',
        'pjpeg': 'jpeg',
        'pjp': 'jpeg',
        'png': 'png',
        'svg': 'svg+xml',
        'webp': 'webp',
    }
    mime_type = mapping.get(extension)
    if mime_type is None:
        return 'application/octet-stream'
    else:
        return f'image/{mime_type}'
