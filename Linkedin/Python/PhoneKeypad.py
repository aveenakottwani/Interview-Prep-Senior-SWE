
"""

Phone Keypad Word Match
 Description: Given a standard telephone keypad mapping and a list of KNOWN_WORDS, write a program to output all words that can be formed by a given $n$-digit phone number.
 Example:
 phoneNumber: 2273377 $\rightarrow$ Output: ['careers']
 phoneNumber: 54653346 $\rightarrow$ Output: ['linkedin', 'linkedgo']

 Follow-up: Discussed concurrency and how to make the lookup/solution thread-safe (e.g., utilizing a ConcurrentHashMap for caching or shared dictionaries).

 Problem
Given a digit string phoneNumber and a dictionary knownWords, return all dictionary words that fully match the number. Each letter maps to one digit, and the word must have the same length as the number.

Use the standard telephone keypad:

2: abc
3: def
4: ghi
5: jkl
6: mno
7: pqrs
8: tuv
9: wxyz
Input and output
Standard input contains a JSON object with:

phoneNumber: a digit string.
knownWords: an array of lowercase English words.
Print a JSON array of matching words.

Added conventions and constraints
The original post does not specify all boundaries. Use these additional conventions for implementation and testing:

Preserve first-occurrence order and output each distinct word once.
Digits 0 and 1 have no corresponding letters, so a number containing either has no matches.
1 <= len(phoneNumber) <= 100000.
0 <= len(knownWords) <= 100000.
Words are nonempty, and their total length does not exceed 1000000.
Example 1
Input:

{"phoneNumber":"2273377","knownWords":["careers","career","car"]}
Output:

["careers"]
Example 2
Input:

{"phoneNumber":"54653346","knownWords":["linkedin","linkedgo","careers"]}
Output:

["linkedin","linkedgo"]
Follow-up
How would you make lookups, caching, and dictionary updates thread-safe when multiple threads share the dictionary?

The phone number question was: given a set of words and the letters associated with phone keypad inputs, determine which known words correspond to a new phone number input.

"""
def match_words(phone: str, known_words: list) -> list:
    if "0" in phone or "1" in phone:
        return []

    key = {}
    for digit, letters in {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
                           "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}.items():
        for ch in letters:
            key[ch] = digit

    n = len(phone)
    seen, out = set(), []
    for w in known_words:
        if len(w) != n or w in seen:
            continue
        for i, ch in enumerate(w):
            if key.get(ch) != phone[i]:   # non-letters return None, so they never match
                break
        else:                              # loop finished with no mismatch
            seen.add(w)
            out.append(w)
    return out

assert match_words("2273377", ["careers", "career", "car"]) == ["careers"]
assert match_words("54653346", ["linkedin", "linkedgo", "careers"]) == ["linkedin", "linkedgo"]
assert match_words("227", ["car", "bar", "car"]) == ["car", "bar"]   # dedupe, first-occurrence order
assert match_words("207", ["car"]) == []                              # contains 0
assert match_words("2", []) == []                                     # no words
assert match_words("2", ["a", "b", "d"]) == ["a", "b"]
assert match_words("22", ["a"]) == []                                 # length mismatch


"""
OPTIMIZATION


"""
def optimized():
    index = {}                      # digit string -> words, in order
    for w in known_words:
        d = "".join(key[c] for c in w)
        bucket = index.setdefault(d, [])
        if w not in bucket:         # use a set per bucket if buckets are large
            bucket.append(w)

    index.get(phone, [])            # each query is now O(N)