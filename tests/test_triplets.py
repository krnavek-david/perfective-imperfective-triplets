import triplets

# configure tests, create separate tests for suffixes
lemmas = triplets.load_file("triplets/all_lemmas")
prefix_pairs = triplets.strip_prefixes(lemmas)
suffix_pairs = triplets.find_suffixal_alternations(lemmas)

def test_prefix_negative():
    assert ("vařit", "ařit") not in prefix_pairs, "('vařit', 'ařit') found"
    assert ("zvát", "vát") not in prefix_pairs, "('zvát', 'vát') found"

def prefix_test_positive():
    assert ("přijet", "jet") in prefix_pairs, "('přijet', 'jet') not found"
    assert ("napsat", "psát") in prefix_pairs, "('napsat', 'psát') not found"
    assert ("přinášet", "nosit") in prefix_pairs, "('přinášet', 'nosit') not found"

def suffix_test_negative():
    assert ("pustit", "pustívat") not in suffix_pairs, "('pustit', 'pustívat') found" 
    assert ("zpít", "zpívat") not in suffix_pairs, "('zpít', 'zpívat') found"

def suffix_test_positive():
    assert ("napustit", "napouštět") in suffix_pairs, "('napustit', 'napouštět') not found"
    assert ("prodat", "prodávat") in suffix_pairs, "('prodat', 'prodávat') not found"
    assert ("uklidnit", "uklidňovat") in suffix_pairs, "('uklidnit', 'uklidňovat') not found"
    assert ("zpít", "zpíjet") in suffix_pairs, "('zpít', 'zpíjet') not found"


