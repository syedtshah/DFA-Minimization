import pygraphviz as pgv
import os


# INPUT

print('Enter the state values:')
states = input().split()
print('Enter the alphabets:')
alpha = input().split()
initial_state = input("\nEnter initial state: ")
final_states = input("\nEnter final state(s):  ").split()


a = {}

for ele in states:
    a[ele] = []

print("\nEnter transitions:\n")
for ele in states:
    for alp in alpha:
        print("\n{0} on {1} -> ".format(ele, alp), end='')

        flag = True
        while flag:
            b = input()
            if b in states:
                a[ele].append(b)
                flag = False
            else:
                print("Enter valid state:")

mat = []
for i in range(len(states)-1):
    mat.append([0 for i in range(i + 1)])
    [mat[i].append(-1) for j in range(i + 1, len(states)-1)]

# input for dfa graph generation

G = pgv.AGraph(directed=True, rankdir='LR')
G.add_node('qi', shape='point')
G.add_node(initial_state, color='red')
G.add_edge('qi', initial_state)
[G.add_node(fs, shape='doublecircle', color='green:green') for fs in final_states]
for tab in sorted(a):
    labels = []
    temp = tab
    for i in range(len(alpha)):
        label =  G.get_edge(tab,a[tab][i]).attr['label'] + ',' + alpha[i] if G.has_edge(tab,a[tab][i]) else alpha[i]
        G.add_edge(tab, a[tab][i], label=label)

G.write('in.dot')
G.layout()
G.draw('in.png', prog='dot')
os.system('eog in.png')

# final states position finder

index_lst = [states.index(i) for i in final_states]

for i in index_lst:
    for j in range(len(states) - 1):
        for k in range(j + 1):
            if i - 1 == j and k not in index_lst:
                mat[j][k] = 1
            elif i == k and j + 1 not in index_lst:
                mat[j][k] = 1

# recursive defn. for looping through 'mat' till no operation is done

flag = True
while flag:
    flag3 = True
    for i in range(len(states) - 1):
        for j in range(i + 1):
            if mat[i][j] == 0:
                r = states[i + 1]
                c = states[j]
                t = 0
                flag2 = True

                while t < len(alpha) and flag2:

                    if a[r][t] != a[c][t]:
                        r1 = states.index(a[r][t]) - 1
                        c1 = states.index(a[c][t])

                        if c1 == len(states) - 1 or mat[r1][c1] == -1 or r1 == -1 or c1 == -1:
                            r1, c1 = c1 - 1, r1 + 1

                        if mat[r1][c1] == 1:
                            mat[i][j] = 1
                            flag3 = False
                            flag2 = False
                    t += 1

    if flag3:
        flag = False

# equivalent pair finder

pairs = []
for i in range(len(states) - 1):
    for j in range(i + 1):
        if mat[i][j] == 0:
            pairs.append((min(states[i + 1], states[j]), max(states[i + 1], states[j])))

# transitive property applier (on pairs)

i, j = 0, 0
flag = True

while flag:
    i, j = 0, 0
    flag = False
    while i < len(pairs):
        j = 0
        while j < len(pairs):
            if i != j and len(set(pairs[i]).intersection(pairs[j])) > 0:
                temp1 = set(pairs[i]).union(pairs[j])
                pairs.pop(i)
                if i > j:
                    pairs.pop(j)
                else:
                    pairs.pop(j - 1)
                pairs.append(temp1)
                flag = True
            j += 1
        i += 1

# mapping from actual state to merged pairs

tab_dict = {}

for ele in states:
    flag = True
    for i in range(len(pairs)):
        if ele in pairs[i]:
            tab_dict[ele] = sorted(list(pairs[i]))
            flag = False
            break
    if flag:
        tab_dict[ele] = [ele]

# minimized table generation

table = {}

for ele in sorted(tab_dict):
    table[', '.join(tab_dict[ele])] = []
    for i in range(len(alpha)):
        table[', '.join(tab_dict[ele])].append(sorted(tab_dict[a[tab_dict[ele][0]][i]]))
        for j in range(1, len(tab_dict[ele])):
            table[', '.join(tab_dict[ele])][i] = sorted(
                set(table[', '.join(tab_dict[ele])][i]).union(tab_dict[a[tab_dict[ele][j]][i]]))

# initial and final state(s) finder for minimised dfa

fin_final = []
fin_init = None
for tab in table:
    if initial_state in tab:
        fin_init = tab
    [fin_final.append(tab) for fs in final_states if fs in tab]

# minimised dfa (output) graph

G = pgv.AGraph(directed=True,rankdir='LR')
G.add_node(fin_init, color='red')
G.add_node('qi', shape='point')
G.add_edge('qi',fin_init,label='start')
[G.add_node(fs, peripheries=2, color='green:green') for fs in fin_final]
for tab in sorted(table):
    for i in range(len(alpha)):
        label = G.get_edge(tab,', '.join(table[tab][i])).attr['label'] + ',' + alpha[i] if G.has_edge(tab,', '.join(table[tab][i])) else alpha[i]
        G.add_edge(tab, ', '.join(table[tab][i]), label=label)

# output minimised dfa's description

print("Iniital state of minimal dfa: " + fin_init + '\n')
print("Final state of minimal dfa: " + ', '.join(fin_final) + '\n')
print("Minimal DFA transition table:\n\n")
print("{:<20}".format('States') + ''.join("{:<20}".format(i) for _, i in enumerate(alpha)))

for tab in sorted(table):
    strs = [', '.join(i) for i in table[tab]]
    print("{:<20}".format(tab) + ''.join("{:<20}".format(i) for _, i in enumerate(strs)))

# print minimised (output) graph

G.write('out.dot')
G.layout()
G.draw('out.png', prog='dot')
os.system('eog out.png')

# FIN
