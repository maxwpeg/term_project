class TextEnum:

    def __init__(self, head, parts):
        self._head = head
        self._parts = parts

    @property
    def head(self):
        return self._head

    @property
    def parts(self):
        return self._parts

    def __str__(self):
        res = str(self._head) + "\n"
        for p in self._parts:
            res += "\t" + str(p) + "\n"
        return res
