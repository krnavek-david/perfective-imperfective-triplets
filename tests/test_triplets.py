import triplets

# configure tests, create separate tests for suffixes
lemmas = triplets.load_file("triplets/all_lemmas")
prefix_pairs = triplets.strip_prefixes(lemmas)
suffix_pairs = triplets.find_suffixal_alternations(lemmas)
verb_triplets = triplets.create_triplets(suffix_pairs, prefix_pairs)

def test_prefix_negative():
    assert ("vařit", "ařit") not in prefix_pairs, "('vařit', 'ařit') found"
    assert ("zvát", "vát") not in prefix_pairs, "('zvát', 'vát') found"

def test_prefix_positive():
    assert ("přijet", "jet") in prefix_pairs, "('přijet', 'jet') not found"
    assert ("napsat", "psát") in prefix_pairs, "('napsat', 'psát') not found"
    assert ("přinášet", "nosit") in prefix_pairs, "('přinášet', 'nosit') not found"

def test_suffix_negative():
    assert ("pustit", "pustívat") not in suffix_pairs, "('pustit', 'pustívat') found" 
    assert ("zpít", "zpívat") not in suffix_pairs, "('zpít', 'zpívat') found"
    assert ("napouštět", "napouštívat") not in suffix_pairs, "('napouštět', 'napouštívat') found"

def test_suffix_positive():
    assert ("napustit", "napouštět") in suffix_pairs, "('napustit', 'napouštět') not found"
    assert ("pustit", "pouštět") in suffix_pairs, "('pustit', 'pouštět') not found"
    assert ("prodat", "prodávat") in suffix_pairs, "('prodat', 'prodávat') not found"
    assert ("uklidnit", "uklidňovat") in suffix_pairs, "('uklidnit', 'uklidňovat') not found"
    assert ("zpít", "zpíjet") in suffix_pairs, "('zpít', 'zpíjet') not found"

def test_triplets_positive():
    assert ("pustit", "napustit", "napouštět") in verb_triplets, "('pustit', 'napustit','napouštět') not found"
    assert ("pustit", "pouštět", "napouštět") in verb_triplets, "('pustit', 'napustit','napouštět') not found"