import data
import outcome_functions as results
import best_thousand

# Data from the simulation program
best_orders = best_thousand.best

# Possible things that can happen at an at-bat
outcomes = [results.walk, results.strikeout, results.single, results.double, results.triple, results.homerun,
            results.out_advance_runners, results.out_no_advance]
outcome_words = ["walk", "strikeout", "single", "double", "triple", "homerun", "out_advance", "out_no_advance"]

# Mapping of number to batter data
# Used to easily translate from orders from simulation program to use in this program
batter_mapping = {
    1: data.jasmin,
    2: data.monica,
    3: data.ali,
    5: data.natalie,
    6: data.amanda,
    10: data.zoe,
    11: data.erika,
    12: data.kim,
    16: data.katie,
    23: data.tori
}

# state defined as (on 1st, on 2nd, on 3rd, inning, outs, score, batter index)

# Start with no one on base, inning 1, 0 outs and points, and at batter 0 in the order
start = (False, False, False, 1, 0, 0, 0)
scores_list = []

# loop through the orders from simulation
for attempt in best_orders:
    order = attempt[1]
    # reset the states to just include the start state to begin and 0 expected score
    states = set()
    states.add(start)
    state_prob = {start: 1}
    exp_score = 0
    # while we haven't exhausted all possibilities
    while len(states) > 0:
        state = states.pop()
        # loop through all outcomes
        for i in range(len(outcomes)):
            # find new sate after that outcome to the at-bat
            res = outcomes[i](state)
            # calculate the probability of that outcome given probability of the previous state and the batter data
            res_prob = state_prob[state]*batter_mapping[order[state[6]]][outcome_words[i]]
            # if game finished
            if res[0] == "end":
                exp_score += res[1]*res_prob
            # if game continuing
            else:
                states.add(res)
                # update the probability of result in the state probability dictionary
                if res not in state_prob:
                    state_prob[res] = 0
                state_prob[res] += res_prob
        # reset probability of beginning state to 0 so that if we come back to that state it doesn't have distorted
        # probability
        state_prob[state] = 0
    scores_list.append((exp_score, order))

# see the best orders in order
scores_list.sort(reverse=True)
# Printing the scores in the best order
print scores_list




