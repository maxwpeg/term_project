import LineType


class Line:
    def __init__(self, content, case, level, types):
        self._content = content
        self._types = types
        self._level = level
        self._start_case = case

    @property
    def content(self):
        return self._content

    @property
    def types(self):
        return self._types

    @property
    def case(self):
        return self._start_case

    @property
    def level(self):
        return self._level

    def __str__(self):
        res = self.level * "\t"
        for tp in self._types:
            res += tp.value
        res += f": {self._content}"
        return res
