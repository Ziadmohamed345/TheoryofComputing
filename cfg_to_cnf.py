##############################################################
# Theory of Computing
##############################################################
# Anas Ahmed Hassan Sayed - 202000005
# Mennatallah Mohamed Naguib - 202001758
# Ziad Mohamed – 202000055
# Seif Khattab – 202000478

##############################################################
# CFG to CNF
##############################################################


def cfg_2_cnf(cfg):
    cnf = cfg

    # 1st Create New Start State   
    print("---------------------------------------")
    print("1st Create New Start State")
    print("---------------------------------------")
    cnf = new_start_state(cnf)
    print_cfg(cnf)

    # 2nd Eliminate nullable productions
    print("---------------------------------------")
    print("2nd Eliminate e productions")
    print("---------------------------------------")
    cnf = eliminate_nullable_productions(cnf)
    print_cfg(cnf)

    # 3rd Eliminate unit productions
    print("---------------------------------------")
    print("3rd Eliminate unit productions")
    print("---------------------------------------")
    cnf = eliminate_unit_productions(cnf)
    print_cfg(cnf)

    # 4th Eliminate useless productions
    print("---------------------------------------")
    print("4th Eliminate useless productions")
    print("---------------------------------------")
    cnf = eliminate_useless_productions(cnf)
    print_cfg(cnf)

    # 5th Convert to Chomsky Normal Form
    print("---------------------------------------")
    print("5th Convert to Chomsky Normal Form")
    print("---------------------------------------")
    cnf = convert_to_cnf(cnf)
    print_cfg(cnf)

    return cnf

##############################################################
# Helper Functions
##############################################################

def new_start_state(cfg):
    s0 = {'S0': ['S', 'e']}
    s0.update(cfg)
    return s0

def eliminate_nullable_productions(cfg):
    cnf = cfg.copy()

    # Get epsilon (nullable) productions
    epsilon_productions = set()
    variables = set()
    for symbol, productions in cnf.items():
        variables.add(symbol)
        if 'e' in productions:
            epsilon_productions.add(symbol)

    # Remove epsilon (nullable) productions from the grammar
    for e in epsilon_productions:
        new_productions = []
        for production in cnf[e]:
            if production != 'e':
                new_productions.append(production)
        cnf[e].extend(new_productions)
        cnf[e] = list(set(cnf[e]))
        cnf[e].remove('e')

    # Update other rules
    updated_grammar = {}
    
    for key, value in cnf.items():
        updated_productions = []

        for production in value:
            new_productions = {production}
            for nullable_symbol in epsilon_productions:
                temp_productions = set()

                for p in new_productions:
                    positions = [
                        pos for pos, symbol in enumerate(p) if symbol == nullable_symbol
                    ]

                    for pos in positions:
                        temp_productions.add(
                            p[:pos] + p[pos + 1:]
                        )

                new_productions.update(temp_productions)

            new_productions.discard('')
            updated_productions.extend(new_productions)
                    
        updated_grammar[key] = list(set(updated_productions))

    return updated_grammar



def eliminate_unit_productions(cfg):
    cnf = cfg.copy()
    has_unit_production = True

    while has_unit_production:
        has_unit_production = False

        for key, value in cnf.items():
            new_values = []

            for prod_value in value:
                if len(prod_value) == 1 and prod_value.isupper() and prod_value != key:
                    has_unit_production = True
                    new_values.extend(cnf[prod_value])
                else:
                    new_values.append(prod_value)

            cnf[key] = new_values
    
    # Remove repeated productions
    for key, value in cnf.items():
        cnf[key] = list(set(value))

    return cnf


def eliminate_useless_productions(cfg):
    cnf = cfg.copy()
    
    list_of_non_terminals = []

    for key, list in cnf.items():
        for prod in list:
            for char in prod:
                if char.isupper() and char not in list_of_non_terminals and char != key:
                    list_of_non_terminals.append(char)
    #print(list_of_non_terminals)
    for key, list in cfg.items():
        if key not in list_of_non_terminals and 'S' not in key:
            del cnf[key]

    return cnf


def convert_to_cnf(cfg):
    cnf = cfg.copy()

    unused_uppercase_letters = [chr(i) for i in range(65, 91)]  # A to Z

    for key, list in cnf.items():
        for prod in list:
            for char in prod:
                if char.isupper() and char in unused_uppercase_letters:
                    unused_uppercase_letters.remove(char)

    # 1st Convert terminals to productions
    for non_terminal, productions in cfg.items():
        new_productions = []
        for production in productions:
            modified_production = ""
            for char in production:
                if len(production)==1 and production.islower():
                    modified_production += char
                    continue
                if char.islower() and char != 'e':
                    temp_non_terminal = None
                    # Check if the lowercase character is already in the values of cnf
                    for k, v in cnf.items():
                        if [char] == v:
                            temp_non_terminal = k
                            break
                    # If not found, use an unused uppercase letter and add it to cnf
                    if temp_non_terminal is None:
                        temp_non_terminal = unused_uppercase_letters.pop()
                        cnf[temp_non_terminal] = [char]
                    modified_production += temp_non_terminal
                else:
                    modified_production += char
            new_productions.append(modified_production)
        cnf[non_terminal] = new_productions

    new_cfg = cnf.copy()

    # 2nd Convert productions to CNF
    list_of_long_productions = []
    for non_terminal, productions in new_cfg.items(): # Check for productions with more than 2 symbols
        for production in productions:
            if len(production) > 2 and production not in list_of_long_productions:
                list_of_long_productions.append(production)

    dict_of_new_productions = {}
    for long_production in list_of_long_productions: # Create a dict of new productions
        for i in range(0, len(long_production), 2):
            if i == len(long_production)-1:
                break
            new_non_terminal = unused_uppercase_letters.pop()
            dict_of_new_productions[new_non_terminal] = [long_production[i] + long_production[i+1]]

    for non_terminal, productions in new_cfg.items(): # Replace long productions with new non-terminals
        for production in productions:
            for key, list in dict_of_new_productions.items():
                for s in list:
                    if s in production:
                        new_production = production.replace(s, key)
                        new_productions = productions
                        for p in productions:
                            if p == production:
                                new_productions[new_productions.index(production)] = new_production
    
    cnf.update(dict_of_new_productions)

    return cnf



def print_cfg(cfg):
    for key, value in cfg.items():
        print(key, "->", " | ".join(value))
    print('')


CFG_test = {'S': ['ASB', 'a'],
       'A': ['aAS', 'a', 'e'],
       'B': ['SbS', 'A', 'bb']}

#CFG_test = {'S': ['ABA'], 'A': ['aA', 'e'], 'B': ['bBc', 'e']}

#CFG_test = {'S': ['a', 'aA', 'B'], 'A': ['aBB', 'e'], 'B': ['Aa', 'b']}

CFG_test = {'S': ['a','aA','B'],
            'A': ['aBB','e'],
            'B': ['Aa','b'],
            'C': ['ba','bC']}

print("---------------------------------------")
print("Starting CFG:")
print("---------------------------------------")
print_cfg(CFG_test)

cfg_2_cnf(CFG_test)

##############################################################
# User Input
##############################################################


print("---------------------------------------")
print("Enter the CFG in the following format:")
print("---------------------------------------")
print("S->ASB|a")
print("A->aAS|a|e")
print("B->SbS|A|bb")
print("---------------------------------------")
print("Enter 'q' to stop entering the CFG")
print("---------------------------------------")
print("Enter the CFG: ")

CFG_input = {}
user_input = ""

while True:
    user_input = input()
    if user_input != 'q':
        user_input = user_input.split('->')
        CFG_input[user_input[0]] = user_input[1].split('|')
    else:
        break

print("The CFG you entered is:")
print_cfg(CFG_input)

cnf_input = cfg_2_cnf(CFG_input)

print("The CNF of the CFG you entered is:")
print_cfg(cnf_input)