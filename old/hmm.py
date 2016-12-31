# def print_dptable(V):
#     print "    ",
#     for i in range(len(V)): print "%7d" % i,
#     print

#     for y in V[0].keys():
#         print "%.5s: " % y,
#         for t in range(len(V)):
#             print "%.7s" % ("%f" % V[t][y]),
#         print
def viterbi(obs, states, remain_p, start_p, bi_p, tri_p, emit_p):
    prob = [[0 for r in range(len(obs))] for c in range(len(states))]
    path = {}

    # Run Viterbi for subsequent characters
    for t in range(len(obs)):
        new_path = {}

        for s in states:
            # if s in guessed and obs[t] != s:
            #     prob[index(s)][t] = 0
            #     new_path[s] = [s]

            # Use start letter freq
            if t == 0:
                prob[index(s)][t] = remain_p[index(s)][t] * start_p[index(s)] * emit_p[index(s)][index(obs[t])]
                new_path[s] = s

            # Use bigram freq
            elif t == 1:
                (probability, state) = max([(remain_p[index(s)][t] * prob[index(s0)][t-1] * bi_p[index(s0)][index(s)] * emit_p[index(s)][index(obs[t])], s0) for s0 in states])
                prob[index(s)][t] = probability
                new_path[s] = path[state] + s

            # Use trigram freq
            elif t >= 2:
                s_tri_p = tri_p[s]

                (probability, state) = max([(remain_p[index(s)][t] * prob[index(tup[0][0])][t-2] * prob[index(tup[0][1])][t-1] * tup[1] \
                    * emit_p[index(s)][index(obs[t])], tup[0][1]) for tup in s_tri_p])
                prob[index(s)][t] = probability
                new_path[s] = path[state] + s

        path = new_path

    predictions = [(prob[index(s)][len(obs) - 1], path[s]) for s in states]

    return sorted(predictions, reverse=True)

    # count = 0
    # while count < 26:
    #     print "%.20f: %s\n" % (rank_prediction[~count][0], path[rank_prediction[~count][1]])
    #     count += 1

# def viterbi(obs, states, start_p, trans_p, emit_p):
#     prob = [[0 for r in range(len(obs))] for c in range(len(states))]
#     path = {}
    
#     # Initialize first character
#     for c in states:
# 		prob[index(c)][0] = start_p[index(c)] * emit_p[index(c)][index(obs[0])]
# 		path[c] = [c]

# 	# Run Viterbi for subsequent characters
#     for t in range(1, len(obs)):
#     	new_path = {}

#     	for s in states:
#     		(probability, state) = max([(prob[index(s0)][t-1] * trans_p[index(s0)][index(s)] * emit_p[index(s)][index(obs[t])], s0) for s0 in states])
#     		prob[index(s)][t] = probability
#     		new_path[s] = path[state] + [s]

#         path = new_path

#     # (probability, state) = max([(prob[index(s)][len(obs) - 1], s) for s in states])
#     # return (probability, path[state])
#     rank = sorted([(prob[index(s)][len(obs) - 1], s) for s in states])
#     count = 0
#     while count < 26:
#     	print "%.20f: %s\n" % (rank[~count][0], "".join(path[rank[~count][1]]))
#     	count += 1
#     return ([row[~0] for row in prob], path)
    

# def getCandidates(prob, states, num):
# 	rank = sorted([(prob[index(s)][len(obs) - 1], s) for s in states])
#     count = 0
#     while count < 10:
#     	print "%.20f: %s\n" % (rank[~count][0], "".join(path[rank[~count][1]]))
#     	count += 1

def index(c):
	return 26 if c == '_' else ord(c)-ord('a')

