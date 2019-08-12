import numpy as np

def update_values(script_id):

    

    script = Script.objects.get(id = script_id)
    score = script.score
    value = script.value
    other_scripts = Script.objects.filter(exclude = script_id)
    expected_score = 0

    #Summing the probabilities of the current script beating all the other scripts, which produces the expected score.
    for s in other_scripts:
        expected_score += calc_propability(value - s.value)
        information +=  ((calc_probability(value - s.value)) * (1 - (calc_probability(value - s.value))

    
    script.value = value + (score - expected_score) / information




#Function that calculates the probability that a script beats another script, based on the value difference between them.
def calc_probability(value_diff):
    
    return (np.exp(value_diff)) / (1 + np.exp(value_diff))


update_values()
        




