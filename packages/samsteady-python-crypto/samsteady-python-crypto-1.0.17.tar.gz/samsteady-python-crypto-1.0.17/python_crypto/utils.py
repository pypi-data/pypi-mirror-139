import base64


def convert_kms_blob_to_string(blob):
    return base64.b64encode(blob).decode('utf-8')

def convert_kms_blob_from_string(blog_string):
    return base64.b64decode(blog_string.encode('utf-8'))