"""
Rippling: AI-assisted coding round. Logger with handlers.

Build a logger that passes every logged message to a set of handlers. Four handler types:
  Remove:    removes every occurrence of a configured string, then prints the result.
  Truncate:  keeps only the first N characters, then prints the result.
  Uppercase: converts the whole message to uppercase, then prints the result.
  Store:     keeps the message in an internal array without printing anything.
Follow-up: search the stored messages.

Conventions
- Every handler independently receives the original message (no pipeline).
- Remove target is nonempty; literal, left-to-right, non-overlapping replacement, no
  repeated removal of newly formed matches ("ababa" minus "aba" -> "ba").
- N >= 0; if N exceeds the length, keep the whole message (Unicode code points).
- Uppercase follows Python str.upper().
- Store preserves original content, duplicates, and insertion order.
- Search: case-sensitive literal substring match, results in insertion order; an empty
  query matches every message. Punctuation is ordinary text (no tokenizing, no regex).
- Handlers send printed output to an injected output function, collected into "printed".

Input (stdin JSON):
  {"handlers":[{"type":"filter","remove":"l"},{"type":"truncation","length":5},
               {"type":"uppercase"},{"type":"array"}],
   "messages":["hello world"]}
Output (stdout JSON):
  {"printed":["heo word","hello","HELLO WORLD"],"arrays":[["hello world"]]}
If "queries" is given, "search_results" holds one list of matches per query.

Note: an earlier version of the spec used types remove/truncate/store with keys text/n and
output keys printed/stored/search_results. This file follows the example format above.
"""
import json
import sys


class Handler:
    def __init__(self, out=print):
        self.out = out

    def handle(self, message):
        raise NotImplementedError


class RemoveHandler(Handler):
    def __init__(self, text, out=print):
        super().__init__(out)
        self.text = text

    def handle(self, message):
        self.out(message.replace(self.text, ""))  # single non-overlapping pass


class TruncateHandler(Handler):
    def __init__(self, n, out=print):
        super().__init__(out)
        self.n = n

    def handle(self, message):
        self.out(message[:self.n])


class UppercaseHandler(Handler):
    def handle(self, message):
        self.out(message.upper())


class StoreHandler(Handler):
    def __init__(self, out=print):
        super().__init__(out)
        self.messages = []

    def handle(self, message):
        self.messages.append(message)

    def search(self, query):
        return [m for m in self.messages if query in m]


class Logger:
    def __init__(self, handlers):
        self.handlers = handlers

    def log(self, message):
        for h in self.handlers:
            h.handle(message)


def build_handler(cfg, out):
    t = cfg["type"]
    if t == "filter":
        return RemoveHandler(cfg["remove"], out)
    if t == "truncation":
        return TruncateHandler(cfg["length"], out)
    if t == "uppercase":
        return UppercaseHandler(out)
    if t == "array":
        return StoreHandler(out)
    raise ValueError(f"unknown handler type: {t}")


def run(data):
    printed = []
    handlers = [build_handler(c, printed.append) for c in data["handlers"]]
    logger = Logger(handlers)
    for m in data["messages"]:
        logger.log(m)
    stores = [h for h in handlers if isinstance(h, StoreHandler)]
    result = {"printed": printed, "arrays": [s.messages for s in stores]}
    if "queries" in data:
        result["search_results"] = [[m for s in stores for m in s.search(q)] for q in data["queries"]]
    return result


def main():
    print(json.dumps(run(json.load(sys.stdin)), separators=(",", ":")))


if __name__ == "__main__":
    main()
