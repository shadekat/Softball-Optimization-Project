import random
from itertools import permutations
from operator import itemgetter
# # # state defined as (on 1st, on 2nd, on 3rd, inning, outs, score, batter index, batting_order)

def gameContinue(state):

    #game not over
    if state[3] < 8:
        return (next_at_bat(state))

    #game over, return score
    else:
        return state[5]

def walk(state):
    # no one on first
    if not state[0]:
        return (True, state[1], state[2], state[3], state[4], state[5], (state[6]+1)%9, state[7])
    # no one on second
    elif not state[1]:
        return (True, True, state[2], state[3], state[4], state[5], (state[6]+1)%9, state[7])
    # no one on third
    elif not state[2]:
        return (True, True, True, state[3], state[4], state[5], (state[6]+1)%9, state[7])
    # someone on every base
    else:
        return (True, True, True, state[3], state[4], state[5]+1, (state[6]+1)%9, state[7])


def strikeout(state):
    # 2 outs
    if state[4] == 2:
        return (False, False, False, state[3]+1, 0, state[5], (state[6]+1)%9, state[7])
    else:
        return (state[0], state[1], state[2], state[3], state[4]+1, state[5], (state[6]+1)%9, state[7])


def single(state):
    score = state[5]
    # People on 2nd and 3rd score
    if state[1]:
        score += 1
    if state[2]:
        score += 1
    # if someone on 1st --> 3rd
    if state[0]:
        return (True, False, True, state[3], state[4], score, (state[6]+1)%9, state[7])
    else:
        return (True, False, False, state[3], state[4], score, (state[6]+1)%9, state[7])


def double(state):
    score = state[5]
    # People on 1st, 2nd, and 3rd score
    if state[0]:
        score += 1
    if state[1]:
        score += 1
    if state[2]:
        score += 1
    return (False, True, False, state[3], state[4], score, (state[6]+1)%9, state[7])


def triple(state):
    score = state[5]
    # People on 1st, 2nd, and 3rd score
    if state[0]:
        score += 1
    if state[1]:
        score += 1
    if state[2]:
        score += 1
    return (False, False, True, state[3], state[4], score, (state[6]+1)%9, state[7])


def homerun(state):
    # batter scores
    score = state[5] + 1
    # People on 1st, 2nd, and 3rd score
    if state[0]:
        score += 1
    if state[1]:
        score += 1
    if state[2]:
        score += 1
    return (False, False, False, state[3], state[4], score, (state[6]+1)%9, state[7])


def out_advance_runners(state):
    if state[4] == 2:
        return (False, False, False, state[3]+1, 0, state[5], (state[6]+1)%9, state[7])
    else:
        score = state[5]
        # person on 3rd scores
        if state[2]:
            score += 1
        # everyone goes forward one
        return (False, state[0], state[1], state[3], state[4]+1, state[5], (state[6]+1)%9, state[7])


def out_no_advance(state):
    # if already 2 outs
    if state[4] == 2:
        #print "inning"
        # not last inning
        #if state[3] < 7:
        return (False, False, False, state[3]+1, 0, state[5], (state[6]+1)%9, state[7])
    else:
        return (state[0], state[1], state[2], state[3], state[4]+1, state[5], (state[6]+1)%9, state[7])

def next_at_bat(state):
    rand = random.random()

    #walk
    if rand < state[7][state[6]].pWalk:
        return gameContinue(walk (state))
    #strikeout
    elif rand < state[7][state[6]].pWalk + state[7][state[6]].pStrikeout:
        return gameContinue(strikeout(state))
    #single
    elif rand < state[7][state[6]].pWalk + state[7][state[6]].pStrikeout + state[7][state[6]].pSingle:
        return gameContinue(single(state))
    #double
    elif rand < state[7][state[6]].pWalk + state[7][state[6]].pStrikeout + state[7][state[6]].pSingle + state[7][state[6]].pDouble:
        return gameContinue(double(state))
    #triple
    elif rand < state[7][state[6]].pWalk + state[7][state[6]].pStrikeout + state[7][state[6]].pSingle + state[7][state[6]].pDouble + state[7][state[6]].pTriple:
        return gameContinue(triple(state))
    #homerun
    elif rand < state[7][state[6]].pWalk + state[7][state[6]].pStrikeout + state[7][state[6]].pSingle + state[7][state[6]].pDouble + state[7][state[6]].pTriple + state[7][state[6]].pHomerun:
        return gameContinue(homerun(state))
    #out_advance_runners
    elif rand < state[7][state[6]].pWalk + state[7][state[6]].pStrikeout + state[7][state[6]].pSingle + state[7][state[6]].pDouble + state[7][state[6]].pTriple + state[7][state[6]].pHomerun + state[7][state[6]].pOutAdvance:
        return gameContinue(out_advance_runners(state))
    #out_no_advance
    else:
        return gameContinue(out_no_advance(state))
def play_game(batting_order):

    initial_state = [False, False, False, 1, 0, 0, 0, batting_order]

    return gameContinue(initial_state)
def avg_games(tries, batting_order):
    cur_sum = 0.0
    for i in range(tries):
        cur_sum = cur_sum + play_game(batting_order)
    return cur_sum / tries

class Batter:
    def __init__(self, name, number, pWalk, pStrikeout, pSingle, pDouble, pTriple, pHomerun, pOutAdvance, pOutNoAdvance):
        self.name = name
        self.number = number
        self.pWalk = pWalk
        self.pStrikeout = pStrikeout
        self.pSingle = pSingle
        self.pDouble = pDouble
        self.pTriple = pTriple
        self.pHomerun = pHomerun
        self.pOutAdvance = pOutAdvance
        self.pOutNoAdvance = pOutNoAdvance

#print play_game([dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy])

jasmin = Batter("Jasmin", 1, 0.07692307692, 0.08791208791, 0.2967032967, 0.06043956044, 0.02197802198, 0.005494505495, 0.0989010989, 0.3516483516)

#print "Jasmin " + str(avg_games(10000, [jasmin, jasmin, jasmin, jasmin, jasmin, jasmin, jasmin, jasmin, jasmin]))

monica = Batter("Monica", 2, 0.07878787879, 0.1272727273, 0.1515151515, 0.03636363636, 0.0, 0.006060606061, 0.2363636364, 0.3636363636)

#print "Monica " + str(avg_games(10000, [monica, monica, monica, monica, monica, monica, monica, monica, monica]))

ali = Batter("Ali", 3, 0.04861111111, 0.09027777778, 0.1875, 0.027777777786, 0.0, 0.01388888889, 0.1736111111, 0.4583333333)

#print "Ali " + str(avg_games(10000, [ali, ali, ali, ali, ali, ali, ali, ali, ali]))

natalie = Batter("Natalie", 5, 0.1298701299, 0.07792207792, 0.1818181818, 0.01298701299, 0.0, 0.0, 0.1818181818, 0.4155844156)

#print "Natalie " + str(avg_games(10000, [natalie, natalie, natalie, natalie, natalie, natalie, natalie, natalie, natalie]))

amanda = Batter("Amanda", 6, 0.1091954023, 0.05747126437, 0.2356321839, 0.05172413793, 0.005747126437, 0.01724137931, 0.224137931, 0.2988505747)

#print "Amanda " + str(avg_games(10000, [amanda, amanda, amanda, amanda, amanda, amanda, amanda, amanda, amanda]))

zoe = Batter("Zoe", 10, 0.05755395683, 0.1294964029, 0.2158273381, 0.04316546763, 0.005747126437, 0.01438848921, 0.2374100719, 0.2949640288)

#print "Zoe " + str(avg_games(10000, [zoe, zoe, zoe, zoe, zoe, zoe, zoe, zoe, zoe]))

erika = Batter("Erika", 11, 0.02666666667, 0.09333333333, 0.1733333333, 0.01333333333, 0.0, 0.0, 0.1066666667, 0.5866666667)

#print "Erika " + str(avg_games(10000, [erika, erika, erika, erika, erika, erika, erika, erika, erika]))

kim = Batter("Kim", 12, 0.08849557522, 0.1238938053, 0.1769911504, 0.01769911504, 0.008849557522, 0.008849557522, 0.2300884956, 0.3451327434)

#print "Kim " + str(avg_games(10000, [kim, kim, kim, kim, kim, kim, kim, kim, kim]))

katie = Batter("Katie", 16, 0.1048951049, 0.06293706294, 0.2307692308, 0.03496503497, 0.006993006993, 0.0, 0.1118881119, 0.4475524476)

#print "Katie " + str(avg_games(100000, [katie, katie, katie, katie, katie, katie, katie, katie, katie]))
    #3628800 tries = 5:25
tori = Batter("Tori", 23, 0.06962025316, 0.1139240506, 0.2341772152, 0.04430379747, 0.0, 0.01898734177, 0.1962025316, 0.3227848101)

#print "Tori " + str(avg_games(10000, [tori, tori, tori, tori, tori, tori, tori, tori, tori]))


#####ALL
print "starting ALL"
scores_dict = {}
for p in permutations([jasmin, monica, ali, natalie, amanda, zoe, erika, kim, katie, tori]):
    scores_dict[p[:9]] = avg_games(20, p[:9])
print len(scores_dict)

sorted_scores = sorted(scores_dict.items(), key=itemgetter(1), reverse=True)
print len(sorted_scores)

top_scores = sorted_scores[:500000]
print len(top_scores)


#####500,000
print "starting 500,000"
scores_dict_500000 = {}
for t in top_scores:
    scores_dict_500000[t[0]] = avg_games(30, t[0])
print len(scores_dict_500000)

sorted_scores_500000 = sorted(scores_dict_500000.items(), key=itemgetter(1), reverse=True)
print len(sorted_scores_500000)

top_scores_500000 = sorted_scores_500000[:60000]
print len(top_scores_500000)


######60,000
print "starting 60,000"
scores_dict_60000 = {}
for t6 in top_scores_500000:
    scores_dict_60000[t6[0]] = avg_games(200, t6[0])
print len(scores_dict_60000)

sorted_scores_60000 = sorted(scores_dict_60000.items(), key=itemgetter(1), reverse=True)
print len(sorted_scores_60000)

top_scores_60000 = sorted_scores_60000[:7000]
print len(top_scores_60000)


######7000
print "starting 7,000"
scores_dict_7000 = {}
for t7 in top_scores_60000:
    scores_dict_7000[t7[0]] = avg_games(1000, t7[0])
print len(scores_dict_7000)

sorted_scores_7000 = sorted(scores_dict_7000.items(), key=itemgetter(1), reverse=True)
print len(sorted_scores_7000)

top_scores_7000 = sorted_scores_7000[:1000]
print len(top_scores_7000)

orders = []
for elt in top_scores_7000:
    order = []
    for bat in elt[0]:
        order.append(bat.number)
    orders.append((elt[1], order))
print len(orders)
print orders


