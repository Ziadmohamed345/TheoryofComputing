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
    Eliminate_nullable_productions(cnf)
    print_cfg(cnf)

    # 3rd Eliminate unit productions
    print("---------------------------------------")
    print("3rd Eliminate unit productions")
    print("---------------------------------------")
    Eliminate_unit_productions(cnf)
    print_cfg(cnf)

    # 4th Eliminate useless productions
    print("---------------------------------------")
    print("4th Eliminate useless productions")
    print("---------------------------------------")
    Eliminate_useless_productions(cnf)
    print_cfg(cnf)

    # 5th Convert to Chomsky Normal Form
    print("---------------------------------------")
    print("5th Convert to Chomsky Normal Form")
    print("---------------------------------------")
    Convert_to_CNF(cnf)
    print_cfg(cnf)

    return cnf

##############################################################
# Helper Functions
##############################################################

def Eliminate_nullable_productions(dict):
    list_to_remove = []
    for key, value in dict.items():

        # Don't eliminate e productions in start state
        if 'S' in key:
            continue

        # Check for e
        if 'e' in value:
            value.remove('e')
            list_to_remove.append(key)
    
    for e_to_remove in list_to_remove:
        for key, value in dict.items():
            for e in value:
                if e_to_remove in e and e_to_remove != e and e.replace(e_to_remove, '') not in value:
                    value.append(e.replace(e_to_remove, ''))


    return dict

def Eliminate_unit_productions(dict):
    has_unit_production = True

    while has_unit_production:
        has_unit_production = False

        for key, value in dict.items():
            new_values = []

            for prod_value in value:
                if len(prod_value) == 1 and prod_value.isupper() and prod_value != key:
                    has_unit_production = True
                    new_values.extend(dict[prod_value])
                else:
                    new_values.append(prod_value)

            dict[key] = new_values

    return dict

def Eliminate_useless_productions(dict):
    
    return dict

def Convert_to_CNF(dict):

    return dict

##############################################################
# Printing CFG
##############################################################

def print_cfg(dict):
    for key, value in dict.items():
        print(key, "->", " | ".join(value))

##############################################################
# Testing
##############################################################

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

# # Instructions
# print("---------------------------------------")
# print("Enter the CFG in the following format:")
# print("---------------------------------------")
# print("S->ASB|a")
# print("A->aAS|a|e")
# print("B->SbS|A|bb")
# print("---------------------------------------")
# print("Enter 'q' to stop entering the CFG")
# print("---------------------------------------")
# print("Enter the CFG: ")

# # User Input
# CFG_input = {}
# user_input = ""

# # Getting the CFG from the user
# while True:
#     user_input = input()
#     if user_input != 'q':
#         user_input = user_input.split('->')
#         CFG_input[user_input[0]] = user_input[1].split('|')
#     else:
#         break

# # Printing the CFG
# print("The CFG you entered is:")
# print_cfg(CFG_input)

# # TODO: Output the CFG in CNF form