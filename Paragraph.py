class Paragraph:
    def __init__(self, content, level=1, type="plain"):
        self._content = content
        self._type = type
        self._level = level

    @property
    def content(self):
        return self._content

    @property
    def type(self):
        return self._type

    @property
    def level(self):
        return self._level

    def __str__(self):
        return self.level * "\t" + f"{self._type}: {self._content}"
