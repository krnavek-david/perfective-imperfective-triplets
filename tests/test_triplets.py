import triplets

# configure tests, create separate tests for suffixes
lemmas = triplets.load_file("triplets/all_lemmas")
prefix_dublets = triplets.strip_prefixes(lemmas)

def test_prefix_negative():
    assert ("vařit", "ařit") not in prefix_dublets, "('vařit', 'ařit') found"
    assert ("zvát", "vát") not in prefix_dublets, "('zvát', 'vát') found"

def prefix_test_positive():
    assert ("přijet", "jet") in prefix_dublets, "('přijet', 'jet') not found"
    assert ("napsat", "psát") in prefix_dublets, "('napsat', 'psát') not found"
    assert ("přinášet", "nosit") in prefix_dublets, "('přinášet', 'nosit') not found"

def suffix_test_positive():
    assert ("přijet", "jet") in prefix_dublets, "('napustit', 'napouštět') not found"