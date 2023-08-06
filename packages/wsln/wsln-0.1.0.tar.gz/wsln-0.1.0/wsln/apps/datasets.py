from pathlib import Path
from tqdm import tqdm
from lxml import etree


def read_paper_dataset(limit=-1):
    # base_path = Path("/media/lee/辽东铁骑/数据集/acl2014/RST_summary/data/acl2014/")
    base_path = Path("/mnt/e/数据集/acl2014/RST_summary/data/acl2014/")

    paths = list((base_path / "abstract").glob("*.txt"))

    if limit == -1:
        limit = len(paths)

    for path in tqdm(paths[:limit], desc="paper-corpus"):
        yield read_paper(base_path, path.name)

def read_paper(base_path, file_name="147.P14-1087.xhtml.txt"):
    abstract = (base_path / "abstract" / file_name).read_text()
    introduction, *sections, conclusion = (base_path / "content" / file_name).read_text().split("\n")

    return abstract, introduction + conclusion, " ".join(sections)


def split_sentences(sentences, points):
        if len(points) <= 0: return sentences
        points.extend([0, 1])

        points = sorted(set(points))

        sentence_group = []
        sentence_len = len(sentences)
        for pre_point, after_point in zip(points[:-1], points[1:]):
            pre_point, after_point = map(int, 
                [sentence_len * pre_point, sentence_len * after_point])
            sentence_group.append(sentences[pre_point:after_point])

        return map(lambda lines: "".join(lines), sentence_group)


def read_cnn_corpus(limit=500):
    base_path = Path("/mnt/e/数据集/新闻/cnn/stories")
    items = []

    for file_path in tqdm(list(base_path.glob("*.story"))[:limit], desc="cnn-corpus"):
        item = read_cnn(file_path)
        items.append(item)
    
    return items

def read_cnn(file_path):
    content = file_path.read_text(encoding="utf-8")
    highlight_index = content.find("@highlight")
    story, highlights = content[:highlight_index], content[highlight_index:].split("@highlight")

    story_lines = [line for line in story.split("\n") if line]
    highlight_lines = [line for line in highlights if line]

    story_lines = [line[9:] if line.startswith("(CNN) -- ") else line for line in story_lines]
    highlight_lines = [line[9:] if line.startswith("(CNN) -- ") else line for line in highlight_lines]

    important, unimportant, important2 = list(split_sentences(story_lines, [0.5, 0.99]))
    important = important + important2

    return ". ".join(highlight_lines), important, unimportant


def read_legal_corpus(limit=3000):
    base_path = Path("/mnt/e/数据集/legal case/corpus/corpus")
    items = []

    for file_path in tqdm(list((base_path / "citations_summ").glob("*.xml"))[:limit], desc="legal-corpus"):
        items.append(read_legal(
            base_path / "citations_summ" / file_path.name,
            base_path / "fulltext" / file_path.name,
        ))
    
    return items


def read_legal(citation_path, fulltext_path):
    summ_tree = etree.HTML(citation_path.read_text(encoding="utf-8", errors="ignore"))
    full_tree = etree.HTML(fulltext_path.read_text(encoding="utf-8", errors="ignore"))

    summ_phrases = ". ".join(summ_tree.xpath("//citphrase//text()"))
    cite_phrases = ". ".join(full_tree.xpath("//catchphrase//text()"))
    sentences = full_tree.xpath("//sentence//text()")[:-2]  # Irrelevant sentence to text

    important, unimportant, important2 = list(split_sentences(sentences, [0.5, 0.99]))
    important = important + important2

    return f"{summ_phrases} {cite_phrases}", important, unimportant