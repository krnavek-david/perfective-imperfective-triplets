# before starting programming, find two or three pairs (with prefixes, then with suffixes) manually
# WITH PREFIXES: spát - vyspat; jet - odjet; zpívat - zazpívat
# WITH SUFFIXES: spát - spávat; jezdit - jezdívat; naprogramovat - naprogramovávat
# (IRREGULAR: najít - nacházet; odjet - odjíždět)
# rethink: are there suffixes regular enough to be programmed easily?
# are there pairs where both are prefixed and it's regular enough?
# github; gitignore the verb file

import re
from data import prefix_pairs_false_friends, prefixes, suffix_pairs_false_friends, suffix_pairs_exceptions

# open file + read line by line and put it in the list/dictionary
def load_file(filepath):
    lemmas = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            lemmas.append(line.strip())
    return lemmas


# strip suffixes or prefixes (in separate functions)
def strip_prefixes(lemmas):
    # task: put triplets together (pustit - napustit - napouštět; problem: dát - dávat - prodat - prodávat)
    # think about how to solve napsat - psát × vyhrát - hrát
    # think about how to pair verbs where both the suffix and the prefix changes (přinášet - nosit)
    # optional: learn to find what slows down the code, try to make it faster
    # compile a list of errors for the thousand verbs
    # solve the false va problem
    # ('dopustit', 'dopouštět') - didn't find pustit
    # look for false friends (dojit, dojet)
    # ('doplouvat', 'doplout') - wrong order
    # manually write triplets/dublets for first 50 verbs

    
    # look if I could create a suffix dictionary from the start, so that I don't have to convert
    # va problem (start with double va)


    stripped = []
    sorted_prefixes = sorted(prefixes, key=len, reverse=True)
    for lemma in lemmas:
        for prefix in sorted_prefixes:
            if lemma not in prefix_pairs_false_friends and lemma.startswith(prefix) and (no_prefix := lemma[len(prefix):]) in lemmas:
                stripped.append((lemma, no_prefix))
                # print(stripped[-1])
                break
    return stripped

def find_suffixal_alternations(lemmas):
    sorted_lemmas = sorted(lemmas, key = lambda x : x[-1])

    pairs = []
    unpaired = [] # verbs for which we didn't find a pair; find a way to check both members of a pair and don't put "zkusit" in the list

    # suffixes = ["at", "át", "ct", "et", "ět", "it", "ít", "st", "ut", "t"]
    # suffixes = sorted(suffixes, key=len, reverse=True)
    for lemma in sorted_lemmas:
        if pair := find_ou_u_alternations(lemma, sorted_lemmas):
            if lemma not in (p[1] for p in pairs):
                pairs.append(pair)
            # if pair[0] is in unpaired, remove it
            if pair[0] in unpaired:
                unpaired.remove(pair[0])
        elif pair := find_va_alternations(lemma, sorted_lemmas):
            if lemma not in (p[1] for p in pairs):
                pairs.append(pair)
            # explain in the comment (if "pustit - pouštět" exists, don't append "pouštět - pouštívat")
            if pair[0] in unpaired:
                unpaired.remove(pair[0])
        else:
            # if lemma is not in first members of pairs, append it
            if lemma not in (p[0] for p in pairs):
                unpaired.append(lemma)
    return pairs

def find_ou_u_alternations(lemma, sorted_lemmas):

    if lemma.endswith("soušet"):
        return (lemma.replace("soušet", "sušit"), lemma)

    alternation_dict = {
        "ouštět$": "ustit",
        "oušet$": "usit",
        "oučet$": "učit",
    }

    # think about putting it in a single regular expression
    
    replaced = lemma
    
    for k, v in alternation_dict.items():
        replaced = re.sub(k, v, replaced)
    
    if replaced != lemma:
        if replaced in sorted_lemmas:
            return (replaced, lemma)
        
    return None

def find_va_alternations(lemma, sorted_lemmas):

    alternation_dict = {
        "ánit$": ["aňovat"],
        "ínit$": ["iňovat"],
        "átit$": ["acovat"],
        "ítit$": ["iťovat", "icovat"],
        "zářit$": ["zařovat"],
        "dit$": ["dívat", "ďovat", "zovat"],
        "nit$": ["nívat", "ňovat"],
        "tit$": ["tívat", "ťovat", "covat"],
        "oupit$": ["upovat"],
        "at$": ["ávat"],
        "át$": ["ávat"],
        "et$": ["ívat"],
        "ět$": ["ívat"],
        "ejt$": ["ejvat"],
        "it$": ["ívat", "ovat"],
        "ít$": ["ívat", "évat"],
        "ýt$": ["ývat"],
        "out$": ["ouvat"]
    }

    # dosvítit - dosvěcovat isn't a pair, but an unwanted triplet (dosvítit - dosvěcet - dosvěcovat)

    replaced = lemma

    for k, v in alternation_dict.items():
        for suffix in v:
            replaced = re.sub(k, suffix, replaced)
            if replaced != lemma:
                if replaced in sorted_lemmas and (not replaced.endswith("vávat") or replaced in suffix_pairs_exceptions) and replaced not in suffix_pairs_false_friends:
                    return (lemma, replaced)
            replaced = lemma

        
    return None

    # problem: uklidnit - uklidňovat × špinit - špinívat

def create_triplets(p_pairs, s_pairs):
    # for pair in suffix_pairs if pair[0] in first members of prefix_pairs create triplet (prefix_pair[1], pair[0], pair[1])
    # for pair in prefix_pairs if pair[0] in first members of suffix_pairs create triplet (pair[1], pair[0], suffix_pair[1])
    prefix_dict = {}
    suffix_dict = {}
    prefix_suffix_triplets = []

    for (k, v) in p_pairs:
        # k can be napouštět
        # v can be pouštět
        prefix_dict[k] = v

    for (k, v) in s_pairs:
        # k can be pouštět
        # v can be pustit
        suffix_dict[k] = v


    

    # example: v = "pustit", k = "napustit", suffix_dict[k] = "napouštět"
    for k, v in prefix_dict.items():
        if k in suffix_dict:
            triplet = (k, suffix_dict[k], v)
            prefix_suffix_triplets.append(triplet)
    
    # example: v = "pustit", k = "pouštět"
    for k, v in suffix_dict.items():
        triplet = (k, v)
        prefix_suffix_triplets.append(triplet)
                
    return prefix_suffix_triplets
    
# in the calling part, ask how many lemmas the file contains and how long the list of dublets is (x dublets out of y lemmas; percentage)
if __name__ == '__main__':
    loaded_lemmas = load_file("triplets/all_lemmas")
    prefix_pairs = strip_prefixes(loaded_lemmas)
    suffix_pairs = find_suffixal_alternations(loaded_lemmas)
    verb_triplets = create_triplets(prefix_pairs, suffix_pairs)
    for t in verb_triplets:
        print(t)
    #suffix_dublets = find_suffixal_alternations(lemmas)
    #print(f"Number of lemmas: {len(lemmas)}")
    #print(f"Number of prefix dublets: {len(prefix_dublets)} ({round((len(prefix_dublets) / len(lemmas) * 100), 2)} %)")
    #print(f"Number of suffix dublets: {len(suffix_dublets)} ({round((len(suffix_dublets) / len(lemmas) * 100), 2)} %)")