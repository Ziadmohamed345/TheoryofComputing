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
    #cnf['S0'] = cnf['S']

    # 2nd Eliminate e productions
    Eliminate_e_productions(cnf)

    # 3rd Eliminate unit productions

    # 4th Eliminate useless productions

    # 5th Convert to Chomsky Normal Form

    return cnf

##############################################################
# Helper Functions
##############################################################

def Eliminate_e_productions(dict):
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
                if e_to_remove in e and e_to_remove != e:
                    value.append(e.replace(e_to_remove, '_'))


    return dict

def Eliminate_unit_productions(dict):

    return dict

def Eliminate_useless_productions(dict):
    
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

print("Before")
print_cfg(CFG_test)
print("-------------------------")
print("After")
print_cfg(cfg_2_cnf(CFG_test))


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