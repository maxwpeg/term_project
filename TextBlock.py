class TextBlock:
    def __init__(self, title, content):
        self._title = title
        self._content = content

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    def __str__(self):
        res = str(self.title) + "\n"
        for par in self._content:
            res += str(par) + "\n"
        return res[:-1]
