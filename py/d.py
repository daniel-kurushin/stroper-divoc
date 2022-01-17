from rutermextract import TermExtractor

def _filter_term(term):
    wrong_grammemes = {'ADJF', 'LATN', 'UNKN', 'NUMB', 'NUMR' }
    
    word = term.words[0].parsed
    
    return len(term.words) > 1 and \
           len(word.tag.grammemes & wrong_grammemes) == 0 

def _normalize_terms_weights(kw):
    import numpy as np
    res = []

    max_weight, min_weight = kw[0][1], kw[-1][1]
    a, b = np.polyfit([max_weight, min_weight], [1, 0.1], 1)
    for term, weight in kw:
        normalized_weight = max(0, a * weight + b)
        res += [[str(term), normalized_weight]]
        
    return res
    
def get_text_keywords(a_text):
    from rutermextract import TermExtractor
    te = TermExtractor()
    kw = [ (term, term.count) for term in te(a_text) if _filter_term(term) ]
    
    return _normalize_terms_weights(kw)

_in = open('../report 2021.md').read()
kw = get_text_keywords(_in)
print("\n".join(sorted([ x[0] for x in kw])))