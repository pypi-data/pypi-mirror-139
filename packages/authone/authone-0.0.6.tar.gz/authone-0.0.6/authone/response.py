

class AuthOneResponse:

    def __init__(self, content, raw_data, status_code):
        self.content = content
        self.status_code = status_code
        self.data = raw_data.get('data', {})
        self.raw_data = raw_data
