from Paragraph import Paragraph
from ParagraphType import ParagraphType


class TitleParagraph(Paragraph):
    def __str__(self):
        res = ParagraphType.TITLE.value + ": "
        for c in self.content:
            res += c.content
        return res
