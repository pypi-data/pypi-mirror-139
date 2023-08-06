# add parent path to python path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

from wsln.settings import version, pattern_handler
from wsln.lexer import Sentence

PROMPT = ">>> "

def main():
    print(f"W-SLN {version}")
    print('Type "help" for more information.\n')

    while (line := input(PROMPT)):
        sentence = Sentence(line.strip())
        print(sentence.tokens)

        w_sln = pattern_handler.match_sentence(sentence)
        for link in w_sln.links:
            print(link)

if __name__ == "__main__":
    main()