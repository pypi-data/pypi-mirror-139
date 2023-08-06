from wsln.apps.word_scoring import smi

def test_smi():
    informative_tokens = [
        "georgia", "mayor", "assails", "governor's", "move", "to", "reopen", "beaches"
    ]
    detailed_tokens = "the tybee island city council voted to close the beaches on march 20 but georgia gov brian kemp issued a statewide shelter-in-place executive order which supersedes all local orders relating to coronavirus and also opened up the state's beaches".split(" ")
    returned = smi(informative_tokens, detailed_tokens, normalize=True)
    print(returned)
