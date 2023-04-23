def printTransitionTable(transition_table):
    print('Transition Table:')

    # Print Header
    print('S', end='\t')
    for i in transition_table[0]:
        print(f'{i}', end='\t')

    # Print Rows
    for i in transition_table:
        # Print Key
        print(f'\n{i}', end='\t')

        # Print Values
        for j in transition_table[i]:
            print(f'{transition_table[i][j]}', end='\t')


def RE2NFA(regex):

    # States
    Q = [0, 'F']
    # Transitions
    T = [regex]

    # transition_table = {
    #     Q[0]: {T[0]: Q[-1]},
    #     Q[-1]: {T[0]: Q[-1]},
    # }

    # Keys: are states
    # Values: are transitions
    transition_table = {
        Q[0]: {},
        Q[-1]: {},
    }

    # First Step: Removing brackets
    # TODO: Fix bug when there are more than one bracket
    # TODO: Fix bug when there is asterisk after brackets
    startIndex = [] # List of indices for opening brackets
    endIndex = [] # List of indices for closing brackets

    for i, char in enumerate(regex):
        if char == '(':
            startIndex.append(i)
        elif char == ')':
            endIndex.append(i)
    for i in range(len(startIndex)):
        insideBrackets = regex[startIndex[i]+1:endIndex[i]].split('|') # Split content inside current set of brackets
        rightSide = regex[endIndex[i]+1:] # Get right side of regex after current set of brackets

        # Get left side of regex before current set of brackets
        if i == 0: # First set of brackets
            leftSide = regex[:startIndex[i]]
        else: # Subsequent sets of brackets
            leftSide = regex[endIndex[i-1]+1:startIndex[i]]

        # Concatenate right side of regex to each element inside current set of brackets
        for j in insideBrackets:
            leftSide += j + rightSide + '|'

        # Remove last '|' from current set of brackets
        leftSide = leftSide[:-1]

        # Reassemble the regex with the modifications
        regex = regex[:startIndex[i]] + leftSide + regex[endIndex[i]+1:]

    # Find all brackets and append their indices to the respective lists
    # for i, char in enumerate(regex):
    #     if char == '(':
    #         startIndex.append(i)
    #     elif char == ')':
    #         endIndex.append(i)
            
    # for i in regex:
    #     if i == '(': # Find first bracket
    #         startIndex = regex.index(i)
    #         regex = regex.replace(i, '')
    #     elif i == ')': # Find last bracket
    #         endIndex = regex.index(i)
    #         regex = regex.replace(i, '')

    #         insideBrackets = regex[startIndex:endIndex].split('|') # Split content inside brackets
    #         rightSide = regex[endIndex:] # Get right side of regex after last bracket

    #         regex = regex[:startIndex] # Get left side of regex before first bracket

    #         # Concatenate right side of regex to each element inside brackets
    #         for j in insideBrackets:
    #             regex += j + rightSide + '|'

    #         # Remove last '|' from regex
    #         regex = regex[:-1]
    
    # Second Step: Splitting regex OR operator
    T = regex.split('|')
    for k, v in transition_table.items():
        for i in T:
            transition_table[k].update({i: Q[-1]})

    # TODO: Thrid Step: Splitting regex AND operator


    # Fourth Step: Removing asterisks
    for K, V in transition_table.items():
        newDict={} # Temp Dict to update transition_table after end of iteration
        for k, v in V.items():
            if '*' in k: # If asterik found...
                without_asterisk = k.replace('*', '')
                newDict[without_asterisk] = K
            else:
                newDict[k] = v
        transition_table[K] = newDict

        # Remove keys with asterisks
        # for key_to_remove in keys_to_remove:
        #     V.pop(key_to_remove)


    # TODO: Fifth Step: Removing plus signs

    # Printing Results
    print(regex)
    print(transition_table)
    printTransitionTable(transition_table)


input_regex_1 = '((a|b))*'
RE2NFA(input_regex_1)
print('\n')
input_regex_2 = '10|(0|11)0*1'
RE2NFA(input_regex_2)