import csp
import sys
from time import sleep
from time import time
from threading import Thread


# returns list with variables
def read_var_file(var_file_path):
    var_list = []
    with open(var_file_path, 'r') as file:
        lines = file.readlines()
        # Skip the first line
        for line in lines[1:]:
            # Split each line by space and take the first number
            first_number = line.split()[0]
            # Append the first number to the data_list
            var_list.append(int(first_number))  # Convert to int and append
    
    return var_list

# returns dictionary with domains
def read_dom_file(dom_file_path,var_file_path):
    dom_dict = {}
    rests = []
    with open(dom_file_path, 'r') as file:
        dom_lines = file.readlines()[1:]  # Skip the first line

        for line in dom_lines:
            first_number, rest = line.split(maxsplit=1)  # Split the line into individual numbers
            rests.append(list(map(int, rest.strip().split())))  # Split values into integers and store as lists
    
    with open(var_file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line
        for line in lines:
            first_num, second_num = line.split()
            first_num = int(first_num)
            second_num = int(second_num)
            if second_num == 0:
                dom_dict[first_num] = rests[0]  # Assign the split values directly for keys with '0'
            else:
                dom_dict[first_num] = rests[1]  # Assign the split values directly for keys with '1'

    return dom_dict

# returns list with constraints
def read_ctr_file(constr_file_path):
    with open(constr_file_path, 'r') as file:
        lines = file.readlines()[1:]  
        constraints = []
        for line in lines:
            A, B, symbol, value = line.split()
            constraints.append((int(A), int(B), symbol, int(value)))
    return constraints

# returns dict with neighbours
def read_neigh_file(neigh_file_path,var_file_path):
    var_list = []
    with open(var_file_path, 'r') as file:
        lines = file.readlines()
        # Skip the first line
        for line in lines[1:]:
            # Split each line by space and take the first number
            first_number = line.split()[0]
            # Append the first number to the data_list
            var_list.append(int(first_number))  # Convert to int and append

    neigh_dict = {var: [] for var in var_list}
    with open(neigh_file_path, 'r') as file:
        n_lines = file.readlines()[1:]  # Skip the first line

        for var in var_list:
            for line in n_lines:
                first_number, second_number,symbol,value = line.split()  # Split the line into individual numbers
                first_number = int(first_number)
                second_number = int(second_number)
                if var == first_number:
                    neigh_dict[var].append(second_number)
                elif var == second_number:
                    neigh_dict[var].append(first_number)
    return neigh_dict

     

# Main
def start():
    instance = sys.argv[1]
    varname = "rlfap\\" + "var" + instance + ".txt"
    domname = "rlfap\\" + "dom" + instance + ".txt"
    ctrname = "rlfap\\" + "ctr" + instance + ".txt"

    variables=read_var_file(varname)
    domains=read_dom_file(domname,varname)
    constraints=read_ctr_file(ctrname)
    neighbors = read_neigh_file(ctrname,varname)

    #constraint function
    def constrains_check(A,a,B,b):
        for c in constraints:
            if (c[0] == A and c[1] == B) or (c[0] == B and c[1] == A):
                if c[2] == '=':
                    if abs(a-b) == c[3]:
                        continue
                    else:
                        return False
                elif c[2] == '>':
                    if abs(a-b) > c[3]:
                        continue
                    else:
                        return False
        return True


    algorithm=sys.argv[2]
    problem = csp.CSP(variables,domains,neighbors,constrains_check,constraints)     # declare the problem

    # choose one of four algorithms 
    if algorithm=="fc":
        start_time = time()
        result=csp.backtracking_search(problem,select_unassigned_variable=csp.domwdeg,order_domain_values=csp.unordered_domain_values,inference=csp.forward_checking)
        if result[0] == None:
            print("result:", result[0])
        else:
            for i in result[0]:
                print("result[{}] = ".format(str(i)), result[0][i])
            print("fc total nodes: %d " % problem.nassigns)
            print("fc total checks: %d" % result[1])
            print("time:", time() - start_time)
    elif algorithm=="mac":
        start_time = time()
        result=csp.backtracking_search(problem,select_unassigned_variable=csp.domwdeg,order_domain_values=csp.unordered_domain_values,inference=csp.mac)
        if result[0] == None:
            print("result:", result[0])
        else:
            for i in result[0]:
                print("result[{}] = ".format(str(i)), result[0][i])
            print("mac total nodes: %d " % problem.nassigns)
            print("mac total checks: %d" % result[1])
            print("time:", time() - start_time)
    elif algorithm=="fc-cbj":
        start_time = time()
        result=csp.cbj_algorithm(problem,select_unassigned_variable=csp.domwdeg,order_domain_values=csp.unordered_domain_values,inference=csp.forward_checking)
        if result[0] == None:
            print("result:", result[0])
        else:
            for i in result[0]:
                print("result[{}] = ".format(str(i)), result[0][i])
            print("cbj total nodes: %d " % problem.nassigns)
            print("cbj total checks: %d" % result[1])
            print("time:", time() - start_time)
    elif algorithm=="min-con":
        start_time = time()
        result=csp.min_conflicts(problem)
        if result[0] == None:
            print("result:", result[0])
        else:
            for i in result[0]:
                print("result[{}] = ".format(str(i)), result[0][i])
            print("min conflicts total nodes: %d " % problem.nassigns)
            print("min conflicts total checks: %d" % result[1])
            print("time:", time() - start_time)

t = Thread(target = start)

t.daemon = True
t.start()

seconds = 500
t.join(seconds)

















