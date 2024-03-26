from Paragraph import Paragraph
from ParagraphType import ParagraphType


class PlainParagraph(Paragraph):
    def __str__(self):
        res = ParagraphType.PLAIN.value + ": "
        for c in self.content:
            res += c.content + "\n"
        return res[:-1]
