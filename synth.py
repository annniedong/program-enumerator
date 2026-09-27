"""
Enumerative program synthesizer.

DSL (Polish notation):  E ::= x | y | 0 | 1 | 2 | + E E | - E E | * E E

Usage:  python3 synth.py problem.txt
"""

import sys

LEAVES = ["x", "y", "0", "1", "2"]
OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}


def parse_examples(text):
    """'1, 2, 3' lines  ->  [(1, 2, 3), ...]"""
    examples = []
    for line in text.splitlines():
        if line.strip():
            x, y, out = (int(n) for n in line.split(","))
            examples.append((x, y, out))
    return examples


def evaluate(program, x, y):
    """Evaluate a Polish-notation program string on inputs x, y."""
    tokens = program.split()

    def go(i):
        # returns (value, index of the next unread token)
        tok = tokens[i]
        if tok in OPS:
            left, i = go(i + 1)
            right, i = go(i)
            return OPS[tok](left, right), i
        if tok == "x":
            return x, i + 1
        if tok == "y":
            return y, i + 1
        return int(tok), i + 1

    return go(0)[0]


def synthesize(examples, max_size=15, prune=True):
    """Return the smallest program that matches every example, or None."""
    xs = tuple(x for x, _, _ in examples)
    ys = tuple(y for _, y, _ in examples)
    target = tuple(out for _, _, out in examples)

    # bank[size] = list of (program, outputs on every example)
    bank = {}
    seen = set()  # outputs we've already produced (for pruning)

    def add(program, outputs, size):
        if prune:
            if outputs in seen:
                return False          # an earlier program already does this
            seen.add(outputs)
        bank.setdefault(size, []).append((program, outputs))
        return outputs == target

    # Size 1: the leaves
    for leaf in LEAVES:
        if leaf == "x":
            outputs = xs
        elif leaf == "y":
            outputs = ys
        else:
            outputs = tuple(int(leaf) for _ in examples)
        if add(leaf, outputs, 1):
            return leaf

    # Size 3, 5, 7, ...: "op left right", where left + right = size - 1 tokens
    for size in range(3, max_size + 1, 2):
        for op, fn in OPS.items():
            for left_size in range(1, size - 1, 2):
                right_size = size - 1 - left_size
                for left, left_out in bank.get(left_size, []):
                    for right, right_out in bank.get(right_size, []):
                        program = f"{op} {left} {right}"
                        outputs = tuple(fn(a, b) for a, b in zip(left_out, right_out))
                        if add(program, outputs, size):
                            return program
    return None


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        result = synthesize(parse_examples(f.read()))
    print(result if result else "NO SOLUTION")
