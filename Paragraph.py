class Paragraph:
    def __init__(self, tp, content):
        self._type = tp
        self._content = content

    @property
    def type(self):
        return self._type

    @property
    def content(self):
        return self._content
