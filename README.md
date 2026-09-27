# program-enumerator

Program Enumerator

An enumerative program synthesizer. Given input-output examples, it finds the smallest arithmetic program that produces the right output on every example.

DSL

Programs are written in Polish (prefix) notation:

E ::= x | y | 0 | 1 | 2 | + E E | - E E | * E E

x is the first input and y is the second. For example, - * x x y means x*x - y.

Usage

Write one example per line as i_1, i_2, o_1:

1, 2, 3
4, 5, 9
0, 7, 7

Then run:

bash
python3 synth.py add.txt
# + x y

If no program of 15 tokens or fewer fits the examples, it prints NO SOLUTION.

How it works
Enumerate by size. Size 1 is the leaves x y 0 1 2. A program of size n is op left right, where the left and right parts add up to n − 1 tokens, so each size is built from smaller sizes that already exist. Only odd sizes are possible (1, 3, 5, …).
Store outputs. Each program is saved with its values on every example, so a new program's values come from combining its two parts' values without re-evaluating anything.
Prune duplicates. If two programs give the same outputs on every example (like + x y and + y x), only the first one is kept. This shrinks the search a lot without changing the answer.
Return the first match. Sizes are tried from smallest to largest, so the first program that matches every example is a smallest one.

See task progress for longer tasks.

README.md
synth.py
enum-synth.zip
synth.py

Track tools and referenced files used in this task.
