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
    list_to_remove = []
    for key, value in cnf.items():

        # Don't eliminate e productions in start state
        if 'S' in key:
            continue
        
        # Check for e
        if 'e' in value:
            value.remove('e')
            list_to_remove.append(key)

    for e_to_remove in list_to_remove:
       for key, value in cnf.items():
            for e in value:
                if e_to_remove in e and e_to_remove != e and e.replace(e_to_remove, '') not in value:
                    value.append(e.replace(e_to_remove, ''))

    # Remove productions that only contain nullable symbols
    for key, value in cnf.items():
        if not value:
            for k, v in cnf.items():
                for prod in v:
                    if key in prod:
                        cnf[k].remove(prod)
    
    return cnf


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

    return cnf


def eliminate_useless_productions(cfg):
    cnf = cfg.copy()
    
    reachable_symbols = set(['S', 'S0'])  # Assuming 'S' is the start symbol
    new_reachable_symbols = set(['S', 'S0'])

    # Iterate until no more new symbols are found
    while len(new_reachable_symbols) > 0:
        previous_length = len(reachable_symbols)
        
        for symbol in list(new_reachable_symbols):
            rules = cnf.get(symbol, [])
            
            for production in rules:
                production_symbols = [sym for sym in production if sym in cnf]
                reachable_symbols.update(production_symbols)
                new_reachable_symbols.update(production_symbols)
                
        new_reachable_symbols.difference_update(reachable_symbols)
        reachable_symbols.update(new_reachable_symbols)

    # Remove non-reachable symbols from the CNF dictionary
    non_reachable_symbols = set(cnf.keys()) - reachable_symbols
    for symbol in non_reachable_symbols:
        del cnf[symbol]

    return cnf


def convert_to_cnf(cfg):
    cnf = cfg.copy()

    unused_uppercase_letters = [chr(i) for i in range(65, 91)]  # A to Z

    # 1st Convert terminals to productions
    for non_terminal, productions in cfg.items():
        new_productions = []
        for production in productions:
            modified_production = ""
            for char in production:
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
    # for non_terminal, productions in new_cfg.items():
    #     produc_copy = productions[:]  # avoid RuntimeError due to changing list size
    #     for production in produc_copy:
    #         if len(production) > 2:
    #             productions.remove(production)
    #             extra_non_terminal = unused_uppercase_letters.pop()
    #             productions.append(extra_non_terminal + production[-1])
    #             cnf[extra_non_terminal] = [production[:-1]]

    return cnf



def print_cfg(cfg):
    for key, value in cfg.items():
        print(key, "->", " | ".join(value))
    print('')


CFG_test = {'S': ['ASB', 'a'],
       'A': ['aAS', 'a', 'e'],
       'B': ['SbS', 'A', 'bb']}

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