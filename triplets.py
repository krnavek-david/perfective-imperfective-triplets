# before starting programming, find two or three pairs (with prefixes, then with suffixes) manually
# WITH PREFIXES: spát - vyspat; jet - odjet; zpívat - zazpívat
# WITH SUFFIXES: spát - spávat; jezdit - jezdívat; naprogramovat - naprogramovávat
# (IRREGULAR: najít - nacházet; odjet - odjíždět)
# rethink: are there suffixes regular enough to be programmed easily?
# are there pairs where both are prefixed and it's regular enough?
# github; gitignore the verb file

import re
from data import prefix_pairs_false_friends, prefixes

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

    stripped = []
    sorted_prefixes = sorted(prefixes, key=len, reverse=True)
    for lemma in lemmas:
        for prefix in sorted_prefixes:
            if lemma not in prefix_pairs_false_friends and lemma.startswith(prefix) and (no_prefix := lemma[len(prefix):]) in lemmas:
                stripped.append((lemma, no_prefix))
                print(stripped[-1])
                break
    return stripped

def find_suffixal_alternations(lemmas):
    sorted_lemmas = sorted(lemmas, key = lambda x : x[-1])
    # example of suffix pair: napustit - napouštět
    # u -> ou, s -> š

    # a -> á, i -> ě, é -> o, u -> ou
    # c -> k, č -> k, s -> š, z -> ž

    # two subfunctions: u -> ou (s -> š, etc.), at -> ávat
    # find more verbs with u -> ou, at -> ávat, ...
    # pustit -> pouštět, poručit -> poroučet, zkusit -> zkoušet
    # prodat -> prodávat, vyplout -> vyplouvat, přespat -> přespávat, přestat -> přestávat, vyhrát -> vyhrávat
    # začít -> začínat, vyjet -> vyjíždět, promluvit -> promlouvat
    # prodloužit -> prodlužovat
    # I can't figure out to implement the subfunctions

    # difficult to solve: dát (perfective) × spát (imperfective)
    # -> dát (P) - dávat (I) × spát (I) - spávat (I)
    # creating pairs/triplets = primary goal
    # perfective and imperfective = secondary goal

    pairs = []
    unpaired = [] # verbs for which we didn't find a pair; find a way to check both members of a pair and don't put "zkusit" in the list

    # suffixes = ["at", "át", "ct", "et", "ět", "it", "ít", "st", "ut", "t"]
    # suffixes = sorted(suffixes, key=len, reverse=True)
    for lemma in sorted_lemmas:
        if pair := find_ou_u_alternations(lemma, sorted_lemmas):
            pairs.append(pair)
            # if pair[0] is in unpaired, remove it
            if pair[0] in unpaired:
                unpaired.remove(pair[0])
            break
        elif pair := find_va_alternations(lemma, sorted_lemmas):
            pairs.append(pair)
            if pair[0] in unpaired:
                unpaired.remove(pair[0])
            break
        else:
            # if lemma is not in first members of pairs, append it
            if lemma not in (p[0] for p in pairs):
                unpaired.append(lemma)
    return pairs

def find_ou_u_alternations(lemma, sorted_lemmas):

    if lemma in ["dosoušet", "vysoušet", "osoušet", "předsoušet"]:
        return (lemma.replace("soušet", "sušit"), lemma)

    alternation_dict = {
        "ouš": "us",
        "ouč": "uč",
        "[eě]t$": "it"
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
        "at$": "ávat",
        "et$": "ívat",
        "ět$": "ívat",
        "ejt$": "ejvat",
        "it$": "ívat",
        "ít$": "ívat",
        "out$": "ouvat"
    }

    for k, v in alternation_dict.items():
        replaced = re.sub(k, v, lemma)

    if replaced != lemma:
        if replaced in sorted_lemmas:
            return (replaced, lemma)
        
    return None

    

    # problem: uklidnit - uklidňovat × špinit - špinívat
                
# in the calling part, ask how many lemmas the file contains and how long the list of dublets is (x dublets out of y lemmas; percentage)
if __name__ == '__main__':
    loaded_lemmas = load_file("triplets/all_lemmas")
    prefix_dublets = strip_prefixes(loaded_lemmas)
    #suffix_dublets = find_suffixal_alternations(lemmas)
    #print(f"Number of lemmas: {len(lemmas)}")
    #print(f"Number of prefix dublets: {len(prefix_dublets)} ({round((len(prefix_dublets) / len(lemmas) * 100), 2)} %)")
    #print(f"Number of suffix dublets: {len(suffix_dublets)} ({round((len(suffix_dublets) / len(lemmas) * 100), 2)} %)")