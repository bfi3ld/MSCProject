import numpy as np
from project.models import Script

def update_values(pk,script):

    score = script.score
    value = script.value
    other_scripts = Script.objects.filter(script__assignment__id = pk).exclude(id = script.id)
    expected_score = 0
    information = 0

    #Summing the probabilities of the current script beating all the other scripts, which produces the expected score.
    for s in other_scripts:
        
        expected_score += calc_probability(value - s.value)
        print(expected_score)
        information +=  ((calc_probability(value - s.value)) * (1 - (calc_probability(value - s.value))))
        print(information)
    
    script_value = value + ((score - expected_score) / information)
    print(script_value)

    return script_value




#Function that calculates the probability that a script beats another script, based on the value difference between them.
def calc_probability(value_diff):
    
    return (np.exp(value_diff)) / (1 + np.exp(value_diff))




    







