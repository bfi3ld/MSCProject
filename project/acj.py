import numpy as np

#Function that pass the scores of the scripts to be evaluated, and returns the calculated values based on those scores.
def estimate_values(scores, vals=None, max_iter=100, tol=0.001):
    vals = vals or [1]*len(scores)
    exp_scores = [1]*len(scores)

    i = 0
    while get_error(scores, exp_scores) > tol and i < max_iter:
        vals, exp_scores = get_iteration_values(scores, vals)
       
        i += 1
        print(exp_scores, get_error(scores, exp_scores))

    if i >= max_iter:
        print("Maximum iterations reached!")

    return vals, exp_scores

#Function that returns the biggest difference between the scores and expected scores of all the scripts. 
def get_error(scores, exp_scores):
    return max([a-b for a,b in zip(scores, exp_scores)])

#Function that returns all the new values and new scores. 
def get_iteration_values(script_scores, script_values):
    new_values = []
    new_expected_scores = []

    for i, (score, value) in enumerate(zip(script_scores, script_values)):
        other_scripts_values = [v for j, v in enumerate(script_values) if i!=j]
        new_value, new_expected_score = get_iteration_value(score, value, other_scripts_values)
        new_values.append(new_value)
        new_expected_scores.append(new_expected_score)

    return new_values, new_expected_scores

#Function that returns a new value and a new expected score on a single script.
def get_iteration_value(script_score, script_value, other_scripts_values):
    expected_score = 0
    information = 0

    # Summing the probabilities of the current script beating all the other scripts, which produces the expected score.
    for other_script_value in other_scripts_values:
        value_diff = script_value - other_script_value
        prob = calc_probability(script_value, other_script_value)
        expected_score += prob
        information +=  prob * (1 - prob)
    
    print("Script value ", script_value)
    print("Expected score ",expected_score)
    print("Information ",information)
    try:
        script_value = script_value + ((script_score - expected_score) / information)
    except ZeroDivisionError:
        print("hej")

    return script_value, expected_score

#Function that calculates the probability that a script beats another script, based on the value difference between them.
def calc_probability(val1, val2):
    
    value_diff = val1-val2

    return (np.exp(value_diff)) / (1 + np.exp(value_diff))


    





if __name__=="__main__":
    script_score, script_value, other_scripts_values = 4, 1, [1, 1, 1, 1]
    new_script_value = update_values(script_score, script_value, other_scripts_values)

