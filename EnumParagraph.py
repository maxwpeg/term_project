from Paragraph import Paragraph


class EnumParagraph(Paragraph):

    def __init__(self, tp, key_sentence, content):
        super().__init__(tp, content)
        self._key_sentence = key_sentence

    def key_sentence(self):
        return self._key_sentence

    def __str__(self):
        res = str(self._key_sentence) + "\n"
        for p in self.content:
            res += str(p) + "\n"
        return res[:-1]
