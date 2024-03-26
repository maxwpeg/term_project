from docx import Document
# import Entity
from LineType import LineType
from EndMarks import EndMarks
import consts
from Line import Line
from CaseType import CaseType
from EnumParagraph import EnumParagraph
from ParagraphType import ParagraphType
from PlainParagraph import PlainParagraph
from TextBlock import TextBlock
from TitleParagraph import TitleParagraph


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


def parse_lines(lines):
    parsed_lines = []
    enum_started_lst = [False] * len(lines)
    case_lst = [CaseType.NOT_INITIALISED] * len(lines)

    for line in lines:

        curr_par_lvl = get_last_true_index(enum_started_lst)
        par_types = []
        last_ch = get_last_char(line)
        curr_case = CaseType.LOWER if line[0] in consts.lower_alphabet else CaseType.UPPER

        if curr_par_lvl > 0 and enum_started_lst[curr_par_lvl - 1]:
            if case_lst[curr_par_lvl] == CaseType.NOT_INITIALISED:
                case_lst[curr_par_lvl] = curr_case
            elif last_ch != EndMarks.SEMICOLON.value and case_lst[curr_par_lvl] != curr_case:
                curr_par_lvl -= 1

            if last_ch == EndMarks.POINT.value:
                par_types.append(LineType.ENUM_LAST)
                enum_started_lst[curr_par_lvl - 1] = False
                case_lst[curr_par_lvl] = CaseType.NOT_INITIALISED
            else:
                par_types.append(LineType.ENUM_PART)

        if last_ch == EndMarks.COLON.value:
            par_types.append(LineType.ENUM_HEAD)
            enum_started_lst[curr_par_lvl] = True

        if len(par_types) == 0 and last_ch == EndMarks.POINT.value:
            par_types.append(LineType.PLAIN)
        elif len(par_types) == 0:
            par_types.append(LineType.TITLE)

        curr_par = Line(line, curr_case, curr_par_lvl, par_types)
        parsed_lines.append(curr_par)

    return parsed_lines


def collect_enum(lines, start_index):
    start_level = lines[start_index].level
    parts = []
    i = start_index + 1
    while i < len(lines) and LineType.ENUM_LAST not in lines[i].types and lines[i].level >= start_level + 1:
        if LineType.ENUM_HEAD in lines[i].types:
            new_enum, i = collect_enum(lines, i)
            parts.append(new_enum)
        else:
            parts.append(lines[i])
        i += 1
    if i < len(lines) and lines[i].level == start_level + 1:
        parts.append(lines[i])
        i += 1
    return EnumParagraph(ParagraphType.ENUM, lines[start_index], parts), i - 1


def collect_plain(lines, start_index):
    content = [lines[start_index]]
    i = start_index + 1
    if i > len(lines) - 1:
        return PlainParagraph(ParagraphType.PLAIN, content), i - 1
    while i < len(lines) and LineType.PLAIN in lines[i].types:
        content.append(lines[i])
        i += 1
    return PlainParagraph(ParagraphType.PLAIN, content), i - 1


def collect_title(lines, start_index):
    content = [lines[start_index]]
    i = start_index + 1
    if i > len(lines) - 1:
        return TitleParagraph(ParagraphType.TITLE, content), i - 1
    while i < len(lines) and LineType.TITLE in lines[i].types:
        content.append(lines[i])
        i += 1
    return TitleParagraph(ParagraphType.TITLE, content), i - 1


def collect_pars(lines):
    pars = []
    i = 0
    while i < len(lines):
        if LineType.PLAIN in lines[i].types:
            par, i = collect_plain(lines, i)
        elif LineType.TITLE in lines[i].types:
            par, i = collect_title(lines, i)
        else:
            par, i = collect_enum(lines, i)
        pars.append(par)
        i += 1
    return pars


def collect_blocks(pars):
    i = 0
    blocks = []
    while i < len(pars):
        title = pars[i]
        if i == len(pars) - 1:
            blocks.append(TextBlock(title, []))
            break
        curr_pars = []
        i += 1
        while i < len(pars) and pars[i].type != ParagraphType.TITLE:
            curr_pars.append(pars[i])
            i += 1
        blocks.append(TextBlock(title, curr_pars))
    return blocks


lines2 = docx2text('2.docx')
data = parse_lines(lines2)
# for d in data:
#     print(d)
paragraphs = collect_pars(data)
# for p in paragraphs:
#     print(p)
#     print()
text_blocks = collect_blocks(paragraphs)
for block in text_blocks:
    print(block)
    print("---")
