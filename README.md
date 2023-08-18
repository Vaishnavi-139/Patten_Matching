# Patten_Matching

1 Background
Consider the basic pattern matching problem discussed in class: given a string p of length m (a.k.a. the
pattern) and a string x of length n (a.k.a the document), the task is to find all occurrences of p in x.
Assume m ≤ n. We saw in class that a na¨ıve algorithm for this takes O(mn) time, whereas the smarter
Knuth-Morris-Pratt algorithm does the job in O(m + n) time. Throughout this document, if y is a string,
then we denote by y[i..j] the substring of y starting at index i and ending at index j. Recall that the
Knuth-Morris-Pratt algorithm computes the failure function h : {1, . . . , m} −→ {1, . . . , m} associated with
the pattern p, where h(i) is the length of the longest proper prefix of p[1..i] that is also a suffix of p[1..i].
This function is then used to process the document. Thus, the function h remains in the working memory,
occupying Θ(m log m) bits of space. Another Θ(log n) bits of space is needed to store the current index
while scanning the document, bringing the overall space complexity to Θ(m log m + log n). The log n term
is unavoidable because we have to store at least a constant number of indices, but can we cut down the
m log m term?
Our task for this assignment is to design and implement an algorithm that has about the same time
complexity as Knuth-Morris-Pratt, but uses only O(log m + log n) working memory. Of course, this comes
at a cost: the algorithm does report false positives with a tiny probability ε.
2 The Basic Idea
For the purpose of this assignment, assume that the document x is a string over the uppercase Latin alphabet:
{A, B, . . . , Z}. Identify these characters with numbers as follows: A with 0, B with 1, . . ., Z with 25. A
string y = y[0]y[1] · · · y[n−1] over the set {A, B, . . . , Z} of length n is the 26-ary representation of the number
f(y) = Pn−1
i=0 26n−i−1 × y[i] (i.e. y[0] is the most significant and y[n − 1] is the least significant), and the
function f is a bijection between strings and non-negative integers. The task of finding occurrences of p in a
document x is the same as finding all indices i such that f(x[i..(i + m − 1)]) = f(p). This observation does
give a correct algorithm, but how better is it than the na¨ıve and the Knuth-Morris-Pratt algorithms? Apart
from the current index, we need to store the number f(p) in our working memory, and this takes about
log n + log2 26m space, which is Θ(m + log n) – not significantly better than Knuth-Morris-Pratt. For each
i, computing f(x[i..(i + m − 1)]) takes time Ω(m). Thus, the running time is Ω(mn) – no better than the
na¨ıve algorithm. We definitely need more ideas!
To get around the problem of Ω(m + log n) space, we choose an appropriate prime number q, and store
f(p) mod q in our working memory instead of f(p). Only O(log q) bits of working memory are sufficient
for this. Then for each i, we compute f(x[i..(i + m − 1)]) mod q, and report a match if and only if it
equals f(p) mod q. This does introduce false positives, and we will see how to control the error probability
by choosing q carefully. Let us worry about the computation first. Note that computing f(x[i..(i + m −
1)]) mod q still takes Ω(m) time, resulting in an overall Ω(mn) running time. How do you get around
this? Your first challenge is to design an algorithm whose output is the same as the algorithm mentioned
above, but which runs in time O(n log2
q), assuming that basic arithmetic operations on b-bit numbers take
Θ(b) time. Your algorithm may only use O(log n + log q) bits of working memory. Call this algorithm
modPatternMatch(q,p,x).
3 Controlling Error
How should we choose the prime number q for modPatternMatch(q,p,x) so that we don’t report too
many false-positives (i.e. indices i such that f(x[i..(i + m − 1)]) ̸= f(p) but (f(x[i..(i + m − 1)]) mod q) =
(f(p) mod q))? Clearly, choosing q deterministically is not a good idea. A worst-case instance could have
lots of occurrences of a pattern p
′ ̸= p such that (f(p
′
) mod q) = (f(p) mod q). To get around this, we
choose q to be a uniformly random prime which is at most an appropriately chosen number N. The number
N will depend on m, the length of the pattern, and ε, the upper bound on the error probability. Thus, we
get the following algorithm.
randPatternMatch(ε,p,x):
1. Compute N appropriately. (Your job is to figure out the details.)
2. q ← randPrime(N). (You are given an implementation of the function randPrime(N) which returns a
uniformly random prime less than or equal to N. For analysis, we will ignore the running time of this
function.)
3. Return modPatternMatch(q,p,x).
As stated in the algorithm, your job is to figure out what N you should use. You will find the following
facts useful.
Claim 1. The number of prime factors of a positive integer d is at most log2 d.
Claim 2. Let π(N) denote the number of primes that are less than or equal to N. Then for all N > 1,
π(N) ≥
N
2 log2 N
.
As an exercise, you may try proving the first claim. (Don’t submit the proof.) The proof of the second
claim is outside the scope of the course.
For full credit, randPatternMatch(ε,p,x) must run in time O
