##############################################################
# Regular Expression To Infix
##############################################################

def regex_2_infix(regex: str) -> str:
    '''
    Convert a regular expression to infix
    '''
    operators = {')', '*', '+', '?', '|', '.'}
    infix = ''
    last_char = None

    for char in regex:
        # If character is not an operator, we need to check the last_char for concatenation.
        if char not in operators:
            if last_char == '*':
                infix += '.' + char
            elif last_char not in operators and last_char is not None and last_char != '(':
                infix += '.' + char
            else:
                infix += char
    
        else: 
            # If character is an operator, simply append it to the infix string.
            infix += char

        # Remember the last character for the next iteration.
        last_char = char

    return infix

##############################################################
# Infix To Postfix
##############################################################

def infix_2_postfix(infix_expr):
    '''
    Shunting Yard Algorithm to convert infix regular expressions to postfix
    '''
    # Dictionary for special characters gives them an order of precedence
    special_chars = {'*': 3, '.': 2, '|': 1}

    # Initializing empty postfix list and stack list
    # Here we push operators in or out
    postfix_expr = []
    operator_stack = []

    # This loop reads the infix regular expression one character at a time
    for char in infix_expr:
        # If the character is an opening bracket, append it to the stack
        if char == '(':
            operator_stack.append(char)
        # If the character is a closing bracket, pop elements from the stack
        # until an opening bracket is found, and append them to postfix
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                postfix_expr.append(operator_stack.pop())
            operator_stack.pop()     # Remove the opening bracket from the stack
        # If the character is in the 'special_chars' dictionary,
        # handle its precedence and pop elements from the stack accordingly
        elif char in special_chars:
            while operator_stack and special_chars.get(char, 0) <= special_chars.get(operator_stack[-1], 0):
                postfix_expr.append(operator_stack.pop())
            operator_stack.append(char) # Append the current special character to the stack
        else:
            # If the character is not a special character or a bracket,
            # append it directly to postfix
            postfix_expr.append(char)

    # Pop and append any remaining elements from the operator stack to postfix
    while operator_stack:
        postfix_expr.append(operator_stack.pop())

    # Return postfix as a string
    return ''.join(postfix_expr)

##############################################################
# Thompsons construction Algorithm
##############################################################

class State:
    '''
    State class contains a label and two edges, labelled by arrows
    '''
    def __init__(self):
        self.label = None
        self.edge1 = None
        self.edge2 = None


class NFA:
    '''
    NFA class contains start and final states only of the NFA
    '''
    def __init__(self, start, final):
        self.start = start
        self.final = final


def postfix_2_nfa(pofix: str):
    '''
    Converts postfix regular expressions to NFA
    '''
    nfa_stack = []

    for c in pofix:
        if c == '*':
            nfa1 = nfa_stack.pop()

            start = State()
            final = State()

            start.edge1 = nfa1.start
            start.edge2 = final

            nfa1.final.edge1 = nfa1.start
            nfa1.final.edge2 = final

            nfa_stack.append(NFA(start, final))

        elif c == '.':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            nfa1.final.edge1 = nfa2.start

            nfa_stack.append(NFA(nfa1.start, nfa2.final))

        elif c == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            start = State()

            start.edge1 = nfa1.start
            start.edge2 = nfa2.start

            final = State()

            nfa1.final.edge1 = final
            nfa2.final.edge1 = final

            nfa_stack.append(NFA(start, final))

        else:
            final = State()
            start = State()

            start.label = c
            start.edge1 = final

            nfa_stack.append(NFA(start, final))

    return nfa_stack.pop()

##############################################################
# Regex String Matching
##############################################################

def check_string(regex, string):
  '''
  Test if regular expression matches string
  '''
  # Shunt and compile the regular expression
  infix = regex_2_infix(regex)
  postfix = infix_2_postfix(infix)
  nfa = postfix_2_nfa(postfix)

  # The current set of states and the next set of states
  current = set()
  nexts = set()

  # Add the start state to the current set
  current |= reachable(nfa.start)

  # loop through each character in the string
  for s in string:
    # loop through the current set of states
    for c in current:
      # Check to see if state is labelled 's'
      if c.label == s:
        nexts |= reachable(c.edge1)
    # set current to next and clears out next
    current = nexts
    # next is back to an empty set
    nexts = set()

  # Checks if the final state is in the set for current state  
  return (nfa.final in current)

def reachable(state):
  '''
  Returns set of states that can be reached from state following e arrows
  '''
  # Create a new set, with state as its only member
  states = set()
  states.add(state)

  # Check if state has arrows labelled e from it
  if state.label is None:
    # If there's an 'edge1', follow it
    if state.edge1 is not None:
      states |= reachable(state.edge1)
    # If there's an 'edge2', follow it
    if state.edge2 is not None:
      states |= reachable(state.edge2)

  # Returns the set of states
  return states

##############################################################
# Old code for converting regex to FA
##############################################################

# def printTransitionTable(transition_table):
#     '''
#     Helper function to print the transition table
#     '''
#     print('Transition Table:')

#     # Print Header
#     print('S', end='\t')
#     for i in transition_table[0]:
#         print(f'{i}', end='\t')

#     # Print Rows
#     for i in transition_table:
#         # Print Key
#         print(f'\n{i}', end='\t')

#         # Print Values
#         for j in transition_table[i]:
#             print(f'{transition_table[i][j]}', end='\t')


# def regex_2_fa(regex):
#     '''
#     Converts a regular expression to a finite automata
#     '''
#     # States
#     Q = [0, 'F']
#     # Transitions
#     T = [regex]

#     # transition_table = {
#     #     Q[0]: {T[0]: Q[-1]},
#     #     Q[-1]: {T[0]: Q[-1]},
#     # }

#     # Keys: are states
#     # Values: are transitions
#     transition_table = {
#         Q[0]: {},
#         Q[-1]: {},
#     }

#     # First Step: Removing brackets
#     # TODO: Fix bug when there are more than one brackets
#     # TODO: Fix bug when there is asterisk after brackets
#     startIndex = 0 # Index of first bracket
#     endIndex = 0 # Index of last bracket
#     for i in regex:
#         if i == '(': # Find first bracket
#             startIndex = regex.index(i)
#             regex = regex.replace(i, '')
#         elif i == ')': # Find last bracket
#             endIndex = regex.index(i)
#             regex = regex.replace(i, '')

#             insideBrackets = regex[startIndex:endIndex].split('|') # Split content inside brackets
#             rightSide = regex[endIndex:] # Get right side of regex after last bracket

#             regex = regex[:startIndex] # Get left side of regex before first bracket

#             # Concatenate right side of regex to each element inside brackets
#             for j in insideBrackets:
#                 regex += j + rightSide + '|'

#             # Remove last '|' from regex
#             regex = regex[:-1]
    
#     # Second Step: Splitting regex OR operator
#     T = regex.split('|')
#     for k, v in transition_table.items():
#         for i in T:
#             transition_table[k].update({i: Q[-1]})

#     # TODO: Thrid Step: Splitting regex AND operator


#     # Fourth Step: Removing asterisks
#     for K, V in transition_table.items():
#         newDict={} # Temp Dict to update transition_table after end of iteration
#         for k, v in V.items():
#             if '*' in k: # If asterik found...
#                 without_asterisk = k.replace('*', '')
#                 newDict[without_asterisk] = K
#             else:
#                 newDict[k] = v
#         transition_table[K] = newDict

#         # Remove keys with asterisks
#         # for key_to_remove in keys_to_remove:
#         #     V.pop(key_to_remove)


#     # TODO: Fifth Step: Removing plus signs

#     # Printing Results
#     printTransitionTable(transition_table)

##############################################################
# Testcases
##############################################################

# Testcases 1
infix = "(aa|ba)*"
strings = ["aabaaa", "abaa"]

print("Infix: ", infix)
for s in strings:
    print("String: ", s)
    if check_string(infix, s):
        print("String is accepted")
    else:
        print("String is rejected")
print("\n")

# Testcase 2
infix = "(a(ba|bb))*"
strings = ["aba", "aabb"]

print("Infix: ", infix)
for s in strings:
    print("String: ", s)
    if check_string(infix, s):
        print("String is accepted")
    else:
        print("String is rejected")
print("\n")

##############################################################
# User Input
##############################################################

while True:
    re = input("Enter regular expression: ")
    while True:
        string = input("Enter string: ")

        if string == 'q':
            break

        if check_string(re, string):
            print("String is accepted")
        else:
            print("String is rejected")