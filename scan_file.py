from docx import Document
import Entity
import pymorphy2
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


def parseparagraphs(paragraphs) -> [Paragraph]:
    parsed_paragraphs = []
    current_par_level = 0
    enum_started_lst = [False] * len(paragraphs)
    case_lst = ["N"] * len(paragraphs)

    for par in paragraphs:
        for i in range(len(enum_started_lst) - 1, -1, -1):
            if enum_started_lst[i]:
                break
            current_par_level = i

        type_of_paragraph = ""
        last_ch = get_last_char(par)

        if current_par_level > 0 and enum_started_lst[current_par_level - 1]:

            if case_lst[current_par_level] == "N":
                if par[0] in consts.lower_alphabet:
                    case_lst[current_par_level] = "L"
                else:
                    case_lst[current_par_level] = "U"
            elif last_ch != ";" and ((case_lst[current_par_level] == "L" and par[0] not in consts.lower_alphabet) or
                  (case_lst[current_par_level] == "U" and par[0] not in consts.upper_alphabet)):
                current_par_level -= 1

            if last_ch == ".":
                type_of_paragraph += "enum_last_"
                enum_started_lst[current_par_level - 1] = False
                case_lst[current_par_level] = "N"
            else:
                type_of_paragraph += "enum_part_"

        if last_ch == ":":
            type_of_paragraph += "enum_head_"
            enum_started_lst[current_par_level] = True

        if type_of_paragraph == "" and last_ch == ".":
            type_of_paragraph += "plain"

        if type_of_paragraph == "":
            type_of_paragraph += "title"

        curr_par = Paragraph(par, current_par_level, type_of_paragraph)
        parsed_paragraphs.append(curr_par)

    return parsed_paragraphs


def unite_paragraphs(paragraphs):
    united_paragraphs = []
    i = 0
    while i < len(data):
        new_content = ""
        new_par = None
        if data[i].type == "title":
            while i < len(data) and data[i].type == "title":
                new_content += data[i].content
                i += 1
            new_par = Paragraph(new_content, "title")

        elif data[i].type == "enum start":
            new_content += data[i].content
            i += 1
            while i < len(data) and data[i].type != "enum end":
                new_content += data[i].content
                i += 1
            new_par = Paragraph(new_content, "enum")

        elif data[i].type == "plain":
            while i < len(data) and data[i].type == "plain":
                new_content += data[i].content
                i += 1
            new_par = Paragraph(new_content)
        united_paragraphs.append(new_par)
    return united_paragraphs


lines = docx2text('2.docx')
data = parseparagraphs(lines)
for d in data:
    print(d)
# united_data = unite_paragraphs(data)
