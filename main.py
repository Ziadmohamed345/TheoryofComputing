def infix_2_postfix(infix_expr):
    """
    Shunting Yard Algorithm to convert infix regular expressions to postfix
    """
    # Dictionary for special characters gives them an order of precedence
    special_chars = {'*': 50, '+': 40, '?': 30, '.': 20, '|': 10}

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


# Thompsons construction Algorithm

class State:
    def __init__(self):
        self.label, self.edge1, self.edge2 = None, None, None


class NFA:
    def __init__(self, initial, accept):
        self.initial, self.accept = initial, accept


def postfix_2_nfa(pofix: str):
    nfa_stack = []

    for c in pofix:
        if c == '*':
            nfa1 = nfa_stack.pop()
            initial, accept = State(), State()
            initial.edge1, initial.edge2 = nfa1.initial, accept
            nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept
            nfa_stack.append(NFA(initial, accept))
        elif c == '.':
            nfa2, nfa1 = nfa_stack.pop(), nfa_stack.pop()
            nfa1.accept.edge1 = nfa2.initial
            nfa_stack.append(NFA(nfa1.initial, nfa2.accept))
        elif c == '|':
            nfa2, nfa1 = nfa_stack.pop(), nfa_stack.pop()
            initial = State()
            initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial
            accept = State()
            nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept
            nfa_stack.append(NFA(initial, accept))
        elif c == '+':
            nfa1 = nfa_stack.pop()
            accept, initial = State(), State()
            initial.edge1 = nfa1.initial
            nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept
            nfa_stack.append(NFA(initial, accept))
        elif c == '?':
            nfa1 = nfa_stack.pop()
            accept, initial = State(), State()
            initial.edge1, initial.edge2 = nfa1.initial, accept
            nfa1.accept.edge1 = accept
            nfa_stack.append(NFA(initial, accept))
        else:
            accept, initial = State(), State()
            initial.label, initial.edge1 = c, accept
            nfa_stack.append(NFA(initial, accept))

    return nfa_stack.pop()


def regex_2_infix(regex: str) -> str:
    """
    Convert a regular expression to infix
    """
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

def check_string(regex, string):
  '''
  Matches a string to an infix regular expression
  '''
  # Shunt and compile the regular expression
  infix = regex_2_infix(regex)
  postfix = infix_2_postfix(infix)
  nfa = postfix_2_nfa(postfix)

  # The current set of states and the next set of states
  current = set()
  nexts = set()

  # Add the initial state to the current set
  current |= reachable(nfa.initial)

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

  # Checks if the accept state is in the set for current state  
  return (nfa.accept in current)
        
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

# User input
# while True:
#     infix = input("Enter infix regular expression: ")
#     if infix == "q":
#         break
#     string = input("Enter string: ")
#     if check_string(infix, string):
#         print("String is accepted")
#     else:
#         print("String is rejected")