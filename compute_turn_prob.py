import random
from bisect import bisect
import math
import copy
import numpy
from pylab import plot, legend, show, xlabel, ylabel, title, ylim, savefig

#parameters
num_participants = 6
num_to_eliminate = 3
num_cakes = 30
#each number in cake_knowledge_list denotes the amount of cakes known/recognised by a participant
#participants are assumed to have equal cake knowledge
cake_knowledge_list = xrange(5,11)
num_trials = 100000
zip_pow = 0.5
debug = False

#generate zipfian distribution for cake probability
cake_prob = {}
for i in xrange(num_cakes):
    cake_prob[i] = float(1.0)/math.pow(i+1,zip_pow)

#functions
#weighted sampling
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

#generate a person's cake knowledge
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
results = []
for cake_knowledge in cake_knowledge_list:
    print "cake_knowledge =", cake_knowledge
    fail = [0]*num_participants
    for nt in xrange(num_trials):
        #if nt % 1000  == 0:
            #print "trial", nt, "\r"
        person_cake = []
        #give everyone knowledge of random selection of cakes
        #popular cakes are known by more people
        #probability of a cake known by a participant follows a zipfian distribution
        person_cake = gen_person_cake(cake_knowledge)
        if debug:
            print person_cake

        cake_remaining = set(xrange(30))
        participant_id = 0
        participant_remaining = set(xrange(num_participants))
        while True:
            #terminate game when no cake left
            #(in this case the number of failed participants could be less than 3)
            if len(cake_remaining) == 0:
                break

            participant_id = participant_id % num_participants
            if participant_id in participant_remaining:
                overlap = person_cake[participant_id] & cake_remaining
                if debug:
                    print "\nparticipant =", participant_id
                    print "\tremainining cake =", cake_remaining
                    print "\tcake overlap =", overlap
                #participant knows no more cake, select a random cake and fail
                if len(overlap) == 0:
                    cake_remaining.remove(random.choice(list(cake_remaining)))
                    fail[participant_id] += 1
                    if debug:
                        print "\t****FAILED****", fail
                    participant_remaining.remove(participant_id)
                    if (num_participants - len(participant_remaining)) == num_to_eliminate:
                        break
                #participant selects randomly a remaining cake that he/she knows
                else:
                    cake_remaining.remove(random.choice(list(overlap)))
                
            participant_id += 1

    fail = [ float(item)/(num_trials) for item in fail]
    print fail
    results.append(fail)

#plot the results (participants' fail chance vs # cake knowledge)
xs = range(1, num_participants+1)
for ys in results:
    plot(xs, ys)
lg = [ "# cakes known = " + str(item) for item in cake_knowledge_list ] 
legend(lg)
xlabel("participant's turn number")
ylabel("fail probability")
ylim(0.3, 0.7)
title("fail probability vs. participant's turn number")
#show()
savefig("fail_prob_vs_turn_number.pdf")
savefig("fail_prob_vs_turn_number.png")

#calculate mean fail probability over cake knowledge
results = numpy.array(results)
print
for i in xrange(results.shape[1]):
    print "Average probability for turn number", i+1, "=", ("%.3f" % numpy.mean(results[:,i])), "(", ("%.3f" % numpy.std(results[:,i])), ")"
