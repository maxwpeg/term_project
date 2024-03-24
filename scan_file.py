from docx import Document
import Entity
import pymorphy2
from ParagraphType import ParagraphType
from EndMarks import EndMarks
import consts
from Paragraph import Paragraph


def docx2text(filename):
    doc = Document(filename)
    result = []
    for param in doc.paragraphs:
        if len(param.text) != 0:
            result.append(param.text)
    return result


def get_last_char(line):
    i = len(line) - 1
    last_ch = line[i]
    while i > 0 and last_ch not in consts.end_punctuation_marks and last_ch not in consts.russian_alphabet:
        i -= 1
        last_ch = line[i]
    return last_ch


def get_last_true_index(lst):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i]:
            return i + 1
    return 0


def parse_paragraphs(paragraphs):
    parsed_paragraphs = []
    enum_started_lst = [False] * len(paragraphs)
    case_lst = ["N"] * len(paragraphs)

    for par in paragraphs:

        curr_par_lvl = get_last_true_index(enum_started_lst)
        type_of_par = EndMarks.EMPTY.value
        last_ch = get_last_char(par)
        curr_case = "L" if par[0] in consts.lower_alphabet else "U"

        if curr_par_lvl > 0 and enum_started_lst[curr_par_lvl - 1]:
            if case_lst[curr_par_lvl] == "N":
                case_lst[curr_par_lvl] = curr_case
            elif last_ch != EndMarks.SEMICOLON.value and case_lst[curr_par_lvl] != curr_case:
                curr_par_lvl -= 1

            if last_ch == EndMarks.POINT.value:
                type_of_par += ParagraphType.ENUM_LAST.value
                enum_started_lst[curr_par_lvl - 1] = False
                case_lst[curr_par_lvl] = "N"
            else:
                type_of_par += ParagraphType.ENUM_PART.value

        if last_ch == EndMarks.COLON.value:
            type_of_par += ParagraphType.ENUM_HEAD.value
            enum_started_lst[curr_par_lvl] = True

        if type_of_par == EndMarks.EMPTY.value and last_ch == EndMarks.POINT.value:
            type_of_par += ParagraphType.PLAIN.value

        if type_of_par == EndMarks.EMPTY.value:
            type_of_par += ParagraphType.TITLE.value

        curr_par = Paragraph(par, curr_par_lvl, type_of_par)
        parsed_paragraphs.append(curr_par)

    return parsed_paragraphs


def unite_paragraphs(paragraphs):
    united_paragraphs = []
    i = 0
    while i < len(data):
        new_content = EndMarks.EMPTY.value
        new_par = None
        if data[i].type == ParagraphType.TITLE.value:
            while i < len(data) and data[i].type == ParagraphType.TITLE.value:
                new_content += data[i].content
                i += 1
            new_par = Paragraph(new_content, ParagraphType.TITLE.value)

        elif data[i].type == ParagraphType.ENUM_HEAD.value:
            new_content += data[i].content
            i += 1
            while i < len(data) and data[i].type != ParagraphType.ENUM_LAST.value:
                new_content += data[i].content
                i += 1
            new_par = Paragraph(new_content, ParagraphType.ENUM_LAST.value)

        elif data[i].type == ParagraphType.PLAIN.value:
            while i < len(data) and data[i].type == ParagraphType.PLAIN.value:
                new_content += data[i].content
                i += 1
            new_par = Paragraph(new_content)
        united_paragraphs.append(new_par)
    return united_paragraphs


lines = docx2text('1.docx')
data = parse_paragraphs(lines)
for d in data:
    print(d)
united_data = unite_paragraphs(data)
