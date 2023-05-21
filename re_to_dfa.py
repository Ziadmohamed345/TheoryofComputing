##############################################################
# Theory of Computing
##############################################################
# Anas Ahmed Hassan Sayed - 202000005
# Mennatallah Mohamed Naguib - 202001758
# Ziad Mohamed – 202000055
# Seif Khattab – 202000478


##############################################################
# Regular Expression To Infix
##############################################################

def regex_2_infix(regex: str) -> str:
    """
    Convert a regular expression to infix
    """
    operators = {')', '*', '|', '.'}
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
    """
    Shunting Yard Algorithm
    """
    # Precedence of operators
    special_chars = {'*': 3, '.': 2, '|': 1}
    
    postfix_expr = [] # Initializing empty postfix list and stack list
    operator_stack = [] # Here we push operators in or out

    # This loop reads the infix regular expression one character at a time
    for char in infix_expr:

        # If opening bracket, push to operator stack
        if char == '(':
            operator_stack.append(char)

        elif char == ')':
            # loop through the operator stack until we find the opening bracket
            while operator_stack and operator_stack[-1] != '(':
                postfix_expr.append(operator_stack.pop())

            operator_stack.pop()

        # If operator
        elif char in special_chars:

            # loop while there are still operators in the stack
            while operator_stack and special_chars.get(char, 0) <= special_chars.get(operator_stack[-1], 0):
                postfix_expr.append(operator_stack.pop())

            operator_stack.append(char)

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
    """
    State class
    """
    def __init__(self):
        self.name = None
        self.label = None
        self.transition1 = None
        self.transition2 = None


class NFA:
    """
    NFA class contains start and final states only of the NFA
    """
    def __init__(self, start, final):
        self.start = start
        self.final = final


def postfix_2_nfa(postfix: str):
    """
    Converts postfix regular expressions to NFA
    """
    
    nfa_stack = []
    count = 0

    for c in postfix:

        # Kleene star
        if c == '*':
            # Pop the top NFA from the stack
            nfa1 = nfa_stack.pop()

            # Create new start and final states
            start = State()
            start.name = count
            count += 1

            final = State()
            final.name = count
            count += 1

            # Add the appropriate connections between states
            start.transition1 = nfa1.start
            start.transition2 = final

            nfa1.final.transition1 = nfa1.start
            nfa1.final.transition2 = final

            # Push the new NFA onto the stack
            nfa_stack.append(NFA(start, final))

        # Concatenation
        elif c == '.':
            # Pop two NFAs from the top of the stack
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            # Combine the two NFAs
            nfa1.final.transition1 = nfa2.start

            # Push the new combined NFA onto the stack
            nfa_stack.append(NFA(nfa1.start, nfa2.final))

        # Or
        elif c == '|':
            # Pop two NFAs from the top of the stack
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            # Create new start and final states
            start = State()
            start.name = count
            count += 1

            # Connect the start state to the start states of nfa1 and nfa2
            start.transition1 = nfa1.start
            start.transition2 = nfa2.start

            final = State()
            final.name = count
            count += 1

            # Connect the final states of nfa1 and nfa2 to the new final state
            nfa1.final.transition1 = final
            nfa2.final.transition1 = final

            # Push the new NFA onto the stack
            nfa_stack.append(NFA(start, final))

        # Alphabet
        else:
            # Create new start and final states
            final = State()
            final.name = count
            count += 1

            start = State()
            start.name = count
            count += 1

            # Set the label to the character and connect the start to the final state
            start.label = c
            start.transition1 = final

            # Push the new NFA onto the stack
            nfa_stack.append(NFA(start, final))

    # Return the final NFA from the stack
    return nfa_stack.pop()


def print_nfa(nfa: NFA):
    """
    Prining NFA structure for debugging
    """
    def explore_state(state, visited_states):
        if state in visited_states:
            return

        visited_states.add(state)
        print(f"State: {state.name} | Label: {state.label or 'None':<4} | transition1: {state.transition1.name if state.transition1 else 'None':^7} | transition2: {state.transition2.name if state.transition2 else 'None':^7}")

        if state.transition1:
            explore_state(state.transition1, visited_states)
        if state.transition2:
            explore_state(state.transition2, visited_states)

    print("NFA Structure:")
    visited_states = set()
    explore_state(nfa.start, visited_states)

##############################################################
# Regex String Matching
##############################################################

def check_string(regex, string):
    """
    Test if regular expression matches string
    """
    nfa = postfix_2_nfa(infix_2_postfix(regex_2_infix(regex)))

    current = reachable(nfa.start) # Return set of states that can be reached from start state

    # Loop through each character in the string
    for s in string:
        nexts = set()
        
        for c in current:
            if c.label == s:
                nexts |= reachable(c.transition1)
                
        current = nexts

    # Checks if the final state is in the set for current state  
    return nfa.final in current


def reachable(state):
  """
  Recursive function that returns set of states that can be reached from given state
  """
  # Create a new set, with state as its only member
  states = set()
  states.add(state)

  # Check if state has arrows labelled e from it
  if state.label is None:
    # If there's an 'transition1', follow it
    if state.transition1 is not None:
      states |= reachable(state.transition1)
    # If there's an 'transition2', follow it
    if state.transition2 is not None:
      states |= reachable(state.transition2)

  # Returns the set of states
  return states

##############################################################
# Old code for converting regex to FA
##############################################################

# def printTransitionTable(transition_table):
#     """
#     Helper function to print the transition table
#     """
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
#     """
#     Converts a regular expression to a finite automata
#     """
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

# # Testcases 1
# infix = "(aa|ba)*"
# strings = ["aabaaa", "abaa"]

# for s in strings:
#     print("String: ", s)
#     if check_string(infix, s):
#         print("String is accepted")
#     else:
#         print("String is rejected")
# print("\n")

# # Testcase 2
# infix = "(a(ba|bb))*"
# strings = ["aba", "aabb"]

# for s in strings:
#     print("String: ", s)
#     if check_string(infix, s):
#         print("String is accepted")
#     else:
#         print("String is rejected")
# print("\n")

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