#!/usr/bin/python
import random

BETRAY = True
SILENT = False

class Alg:
    def play(self, my_history, their_history):
        """ @param my_history List of own last choices
            @param their_history List of last choices of the other
            @return decision {BETRAY, SILENT}
        """
        raise NotImplementedError
    def __repr__(self):
        return "{}()".format(type(self).__name__)

def score(A_choice, B_choice):
    if A_choice == B_choice:
        if A_choice == BETRAY:
            return (1, 1)
        return (3, 3)
    if A_choice == BETRAY:
        return (5, 0)
    return (0, 5)

def play(A, B, *, rounds=200):
    A_choices = []
    A_score = 0
    B_choices = []
    B_score = 0
    for i in range(rounds):
        A_choice = A.play(A_choices, B_choices)
        B_choice = B.play(B_choices, A_choices)
        A_score_, B_score_ = score(A_choice, B_choice)
        A_score += A_score_
        B_score += B_score_
        A_choices.append(A_choice)
        B_choices.append(B_choice)
    #print("A={!r}\nB={!r}".format(A_choices, B_choices))
    return (A_score, B_score)

def simulate(algs, *, seed=42, rounds=200):
    random.seed(seed)
    score = [[0] * len(algs) for i in range(len(algs))]

    for idx_A, A in enumerate(algs):
        for idx_B, B in enumerate(algs):
            if idx_B > idx_A:
                break
            A_score, B_score = play(A, B, rounds=rounds)
            score[idx_A][idx_B] = A_score
            score[idx_B][idx_A] = B_score

    for line in range(len(algs)):
        s = sum(score[line])
        score[line].insert(0, s)
        score[line].insert(0, "{!r}".format(algs[line]))
    score.sort(key=lambda l: l[1], reverse=True)
    score.insert(0, ["{!r}".format(a) for a in ["A↓ B→", "total"] + algs])
    print_mat(score)

def print_mat(matrix):
    # https://stackoverflow.com/a/13214945
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


################################################################################
class Random(Alg):
    def __init__(self, p_silent=0.5):
        self.p_silent = p_silent
    def play(self, my_history, their_history):
        if random.random() < self.p_silent:
            return SILENT
        return BETRAY
    def __repr__(self):
        return "{}(p_silent={!r})".format(type(self).__name__, self.p_silent)
class Tit4Tat(Alg):
    def play(self, my_history, their_history):
        if len(their_history) == 0:
            return SILENT
        return their_history[-1]
