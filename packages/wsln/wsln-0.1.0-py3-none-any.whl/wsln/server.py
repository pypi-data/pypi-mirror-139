import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

from wsln.lexer import new_sentence
from wsln.settings import template_handler

import bottle
from bottle import request, response, static_file
from bottle import get, post, route

@get("/index")
def index_page():
    return static_file("main_page.html", root="./static")

@get('/static/<path>')
def js(path):
    return static_file(path, root='./static')

@get("/links")
def extract_links():

    sentence = new_sentence(request.query["sentence"])

    print(sentence)

    links = template_handler.extract_links_from_sentence(sentence)

    node_set = set()
    for link in links:
        node_set.update({link.from_node.literal, link.to_node.literal})

    return {
        "nodes": list(node_set),
        "links": [{
                "from_node": link.from_node.literal,
                "to_node": link.to_node.literal,
                "link_word": link.indicator_token.literal,
                "link_type": str(link.link_type)[9:],
            } for link in links
        ]
    }

if __name__ == "__main__":
    bottle.run(server="gunicorn", host="0.0.0.0", port=8883)