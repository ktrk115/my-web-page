import bibtexparser
from pathlib import Path
from bisect import insort_right

journals = []
conferences = []
others = []

bib_path = Path(__file__).parents[1] / "static/publication.bib"
library = bibtexparser.parse_file(str(bib_path))
for entry in library.entries:
    if entry.entry_type == "article":
        journals.append(entry.fields_dict)
    elif entry.entry_type == "inproceedings":
        entry.fields_dict['booktitle'].value = "In " + entry.fields_dict['booktitle'].value
        conferences.append(entry.fields_dict)
    else:
        others.append(entry.fields_dict)

bib_path = Path(__file__).parents[1] / "static/ja/publication.bib"
library = bibtexparser.parse_file(str(bib_path))
for entry in library.entries:
    entry.fields_dict['title'].value = "ja:" + entry.fields_dict['title'].value
    if entry.entry_type == "article":
        insort_right(journals, entry.fields_dict, key=lambda x: -int(x['year'].value))
    elif entry.entry_type == "inproceedings":
        insort_right(conferences, entry.fields_dict, key=lambda x: -int(x['year'].value))
    else:
        # insort_right(others, entry.fields_dict, key=lambda x: x['year'].value)
        continue

def acm_format(fields_dict):
    title = fields_dict["title"].value
    if title.startswith("ja:"):
        fields_dict["title"].value = title[3:]
        return ja_format(fields_dict)
    title = title.replace("{","").replace("}", "")
    year = fields_dict["year"].value
    authors = fields_dict["author"].value.split(" and ")
    authors = [f'{author.split()[0][0]}.{author.split()[1]}' for author in authors]
    authors[-1] = f'and {authors[-1]}'
    authors = ", ".join(authors)
    if 'journal' in fields_dict:
        info = fields_dict["journal"].value
        info += f' {fields_dict["volume"].value},'
        info += f' {fields_dict["number"].value}'
    else:
        info = fields_dict["booktitle"].value
        if 'series' in fields_dict:
            info += f' ({fields_dict["series"].value})'
    if 'pages' in fields_dict:
        info += f', {fields_dict["pages"].value.replace("--", "-")}'
    return f"{authors}. {year}. {title}. {info}."


def ja_format(fields_dict):
    title = fields_dict["title"].value
    title = title.replace("{","").replace("}", "")
    year = fields_dict["year"].value
    authors = fields_dict["author"].value.split(" and ")
    if "Kotaro Kikuchi" not in authors:
        authors = [author.replace(" ", "") for author in authors]
    else:
        authors = [f'{author.split()[0][0]}.{author.split()[1]}' for author in authors]
        authors[-1] = f'and {authors[-1]}'
    authors = ", ".join(authors)
    if 'journal' in fields_dict:
        info = fields_dict["journal"].value
        info += f' {fields_dict["volume"].value},'
        info += f' {fields_dict["number"].value}'
    else:
        info = fields_dict["booktitle"].value
        if 'series' in fields_dict:
            info += f' ({fields_dict["series"].value})'
    if 'pages' in fields_dict:
        info += f', {fields_dict["pages"].value.replace("--", "-")}'
    return f"{authors}. {year}. {title}. {info}."



count = 0
count_reviewed = 0

def print_records(records, reviewed=True):
    global count, count_reviewed
    for fields_dict in records:
        count += 1
        is_ja = fields_dict["title"].value.startswith("ja:")
        if reviewed and not is_ja:
            count_reviewed += 1

        author = fields_dict["author"].value
        is_first_author = author.startswith("Kotaro Kikuchi") or author.startswith("菊池 康太郎")
        prefix = f'({count})(筆頭)' if is_first_author else f'({count})(共著)'
        prefix = prefix + '(査読付)' if (reviewed and not is_ja) else prefix
        print(f"{prefix} {acm_format(fields_dict)}")

# Journal
# print("（１）査読付学術誌・ジャーナル掲載・原著論文")
# print_records(journals)

# Conference
# print("（２）査読付国際学会論文")
# print_records(conferences)

# Others
# print("（３）その他（解説記事・論説等）")
# print_records(others, reviewed=False)

# print(f"合計: {count}, 査読付: {count_reviewed}, SCOPUS掲載論文数: 16")
# SCOPUS掲載論文数
# https://www.scopus.com/authid/detail.uri?authorId=57192384491


def presentation_format(fields_dict):
    title = fields_dict["title"].value
    if title.startswith("ja:"):
        title = title[3:]
    title = title.replace("{","").replace("}", "")
    year = fields_dict["year"].value
    if 'journal' in fields_dict:
        info = fields_dict["journal"].value
    else:
        info = fields_dict["booktitle"].value
        if 'series' in fields_dict:
            info += f' ({fields_dict["series"].value})'
    return f"{title}. {year}. {info}."

count = 0
count_reviewed = 0
def print_presentation(records):
    global count, count_reviewed
    for fields_dict in records:
        count += 1
        is_ja = fields_dict["title"].value.startswith("ja:")
        prefix = f'({count})'
        prefix = prefix + '(国際学会)' if not is_ja else prefix
        prefix = prefix + '(査読付)' if not is_ja else prefix
        print(f"{prefix} {presentation_format(fields_dict)}")


# 学会発表
all_records = sorted(journals + conferences + others, key=lambda x: -int(x['year'].value))
print_presentation(all_records)