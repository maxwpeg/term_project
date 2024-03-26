from docx import Document
import Entity
import pymorphy2
from ParagraphType import ParagraphType
from EndMarks import EndMarks
import consts
from Paragraph import Paragraph
from CaseType import CaseType
from TextEnum import TextEnum


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
    case_lst = [CaseType.NOT_INITIALISED] * len(paragraphs)

    for par in paragraphs:

        curr_par_lvl = get_last_true_index(enum_started_lst)
        par_types = []
        last_ch = get_last_char(par)
        curr_case = CaseType.LOWER if par[0] in consts.lower_alphabet else CaseType.UPPER

        if curr_par_lvl > 0 and enum_started_lst[curr_par_lvl - 1]:
            if case_lst[curr_par_lvl] == CaseType.NOT_INITIALISED:
                case_lst[curr_par_lvl] = curr_case
            elif last_ch != EndMarks.SEMICOLON.value and case_lst[curr_par_lvl] != curr_case:
                curr_par_lvl -= 1

            if last_ch == EndMarks.POINT.value:
                par_types.append(ParagraphType.ENUM_LAST)
                enum_started_lst[curr_par_lvl - 1] = False
                case_lst[curr_par_lvl] = CaseType.NOT_INITIALISED
            else:
                par_types.append(ParagraphType.ENUM_PART)

        if last_ch == EndMarks.COLON.value:
            par_types.append(ParagraphType.ENUM_HEAD)
            enum_started_lst[curr_par_lvl] = True

        if len(par_types) == 0 and last_ch == EndMarks.POINT.value:
            par_types.append(ParagraphType.PLAIN)
        elif len(par_types) == 0:
            par_types.append(ParagraphType.TITLE)

        curr_par = Paragraph(par, curr_case, curr_par_lvl, par_types)
        parsed_paragraphs.append(curr_par)

    return parsed_paragraphs


def get_enum(pars, start_level, start_index):
    parts = []
    i = start_index + 1
    par = pars[i]
    while ParagraphType.ENUM_LAST not in par.types:
        if ParagraphType.ENUM_HEAD in par.types:
            new_enum, i = get_enum(pars, par.level, i)
            parts.append(new_enum)
        else:
            parts.append(par)
        i += 1
        par = pars[i]
    parts.append(par)
    return TextEnum(pars[start_index], parts), i


def get_plain_or_title(pars, start_level, start_index, tp):
    i = start_index + 1
    content = pars[start_index].content
    case = pars[start_index].case
    par = pars[i]
    while tp in par.types:
        par = pars[i]
        content += par.content
        i += 1
    return Paragraph(content, case, start_level, [tp]), i - 1


def unite_paragraphs(pars):
    united_paragraphs = []
    i = 0
    while i < len(pars):
        par_lvl = pars[i].level
        par_types = pars[i].types
        if ParagraphType.ENUM_HEAD in par_types:
            curr_enum, i = get_enum(pars, par_lvl, i)
            united_paragraphs.append(curr_enum)
        else:
            curr_type = ParagraphType.TITLE if ParagraphType.TITLE in par_types else ParagraphType.PLAIN
            if i < len(pars) - 1:
                curr_plain, i = get_plain_or_title(pars, par_lvl, i, curr_type)
            else:
                curr_plain = pars[i]
            united_paragraphs.append(curr_plain)
        i += 1

    return united_paragraphs


lines = docx2text('2.docx')
data = parse_paragraphs(lines)
# for d in data:
#     print(d)
united_data = unite_paragraphs(data)
for u in united_data:
    print(u)
    print()