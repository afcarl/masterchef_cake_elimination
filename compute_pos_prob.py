import random
from bisect import bisect
import math
import copy

num_participants = 6
num_to_eliminate = 3
num_cakes = 30
cake_knowledge_set = xrange(5,16)
num_trials = 50000
zip_pow = 0.5
debug = False

#generate zipfian distribution for cake probability
cake_prob = {}
for i in xrange(num_cakes):
    cake_prob[i] = float(1.0)/math.pow(i+1,zip_pow)

#functions
def weighted_choice(choices):
    values = choices.keys()
    weights = choices.values()
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect(cum_weights, x)
    return values[i]

def gen_person_cake(ck):
    person_cake = []
    for i in xrange(num_participants):
        participant_cake_prob = copy.copy(cake_prob)
        cake_list = set([])
        for j in xrange(ck):
            selected = weighted_choice(participant_cake_prob)
            cake_list.add(selected)
            del participant_cake_prob[selected]
        person_cake.append(cake_list)
    return person_cake

#main
for cake_knowledge in cake_knowledge_set:
    print "cake_knowledge =", cake_knowledge
    fail = [0]*num_participants
    for nt in xrange(num_trials):
        #if nt % 1000  == 0:
            #print "trial", nt, "\r"
        person_cake = []
        #give everyone knowledge of random selection of cakes
        #for np in xrange(num_participants):
        #    person_cake.append(set(random.sample(xrange(30), cake_knowledge)))
        person_cake = gen_person_cake(cake_knowledge)
        if debug:
            print person_cake

        cake_remaining = set(xrange(30))
        participant_id = 0
        participant_remaining = set(xrange(num_participants))
        while True:
            participant_id = participant_id % num_participants
            if participant_id in participant_remaining:
                overlap = person_cake[participant_id] & cake_remaining
                if debug:
                    print "\nparticipant =", participant_id
                    print "\tremainining cake =", cake_remaining
                    print "\tcake overlap =", overlap
                if len(overlap) == 0:
                    fail[participant_id] += 1
                    if debug:
                        print "\t****FAILED****", fail
                    participant_remaining.remove(participant_id)
                    if (num_participants - len(participant_remaining)) == num_to_eliminate:
                        break
                else:
                    cake_remaining.remove(random.choice(list(overlap)))
                
            participant_id += 1

    fail = [ ("{0:.3f}".format(float(item)/(num_trials))) for item in fail]
    print fail

        
        
