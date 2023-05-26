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
    cnf['S0'] = ['S','e']
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
    
    # Remove non-reachable productions
    reachable = set(['S0'])
    changed = True
    while changed:
        changed = False
        for key, value in cnf.items():
            if key in reachable:
                for prod in value:

                    for symbol in prod:
                        if symbol.isupper() and symbol not in reachable:
                            reachable.add(symbol)
                            changed = True
                            cnf = {key: value for key, value in cnf.items() if key in reachable}


    # Remove non-productive productions
    productive = set()
    for key, value in cnf.items():
        for prod in value:
            if all(symbol not in prod for symbol in cnf.keys()):
                productive.add(key)

    cnf = {key: value for key, value in cnf.items() if key in productive}

    return cnf


def convert_to_cnf(cfg):
    cnf = cfg.copy()
    # Replace terminals in productions with new non-terminals
    new_non_terminals = {}
    temp_cnf = cnf.copy()
    for key, value in temp_cnf.items():
        new_productions = []
        for prod in value:
            new_prod = []
            for symbol in prod:
                if symbol.isupper():
                    new_prod.append(symbol)
                else:
                    if symbol not in new_non_terminals:
                        new_non_terminal = get_new_non_terminal(cnf.keys())
                        new_non_terminals[symbol] = new_non_terminal
                        cnf[new_non_terminal] = [symbol]
                    new_prod.append(new_non_terminals[symbol])
            new_productions.append(''.join(new_prod))
        cnf[key] = new_productions

    # Eliminate non-binary productions
    #temp_cnf = cnf.copy()
    for key,value in temp_cnf.items():
        new_productions = []
        for prod in value:
            if len(prod) > 2:
                for i in range(len(prod)-2):
                    new_non_terminal = get_new_non_terminal(cnf.keys())
                    cnf[new_non_terminal] = [prod[i]+new_non_terminal]
                    if i == 0:
                        new_productions.append(new_non_terminal)
                    prod = new_non_terminal + prod[i+1:]
                new_productions.append(prod)
            else:
                new_productions.append(prod)
        cnf[key] = new_productions

    return cnf


def get_new_non_terminal(existing):
    i = 0
    while True:
        new_nt = 'X' + str(i)
        if new_nt not in existing:
            return new_nt
        i += 1


def print_cfg(cfg):
    for key, value in cfg.items():
        print(key, "->", " | ".join(value))


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