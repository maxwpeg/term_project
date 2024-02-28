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


def parseparagraphs(paragraphs) -> [Paragraph]:
    par_level = 0
    parsed_paragraphs = []
    end_enum = True
    prev_type = ""
    _tab = False
    tab = False

    for par in paragraphs:
        i = len(par) - 1
        last_ch = par[i]

        while i > 0 and last_ch not in consts.end_punstuation_marks and last_ch not in consts.russian_alphabet:
            i -= 1
            last_ch = par[i]

        type_of_paragraph = "title"

        if last_ch == ";":
            type_of_paragraph = "enum part"
            end_enum = False
        else:
            if "enum start" in prev_type:
                type_of_paragraph = "enum part"
            if not end_enum:
                type_of_paragraph = "enum end"
                _tab = True
            elif last_ch == ".":
                type_of_paragraph = " plain"
            if last_ch == ":":
                if type_of_paragraph == "title":
                    type_of_paragraph = ""
                else:
                    type_of_paragraph += " "
                type_of_paragraph += "enum start"
                tab = True
            end_enum = True


        curr_par = Paragraph(par, par_level, type_of_paragraph)
        parsed_paragraphs.append(curr_par)

        if tab:
            tab = False
            par_level += 1
        elif _tab:
            _tab = False
            par_level -= 1

        prev_type = curr_par.type
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


lines = docx2text('1.docx')
data = parseparagraphs(lines)
for d in data:
    print(d)
# united_data = unite_paragraphs(data)
