import os
import csp
from time import sleep
from threading import Thread
# Path to the folder containing the rlfap folder
folder_path = 'C:\\Users\\vagge\\OneDrive\\Desktop\\AI'

# Path to the rlfap folder
rlfap_folder_path = os.path.join(folder_path, 'rlfap')

# Path to the specific .txt file within rlfap folder
#dom_file_path = os.path.join

def read_var_file(rlfap_folder_path, file_name_var):
    var_file_path = os.path.join(rlfap_folder_path, file_name_var)
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

# Call the function to read the .txt file and store its contents in a list
data_from_var = read_var_file(rlfap_folder_path,'var2-f25.txt')
#print(data_from_txt)

def read_dom_file(rlfap_folder_path, file_name_dom):
    dom_file_path = os.path.join(rlfap_folder_path, file_name_dom)
    dom_dict = {}
    rests = []
    with open(dom_file_path, 'r') as file:
        dom_lines = file.readlines()[1:]  # Skip the first line

        for line in dom_lines:
            first_number, rest = line.split(maxsplit=1)  # Split the line into individual numbers
            rests.append(list(map(int, rest.strip().split())))  # Split values into integers and store as lists
    
    var_file_path = os.path.join(rlfap_folder_path, 'var2-f25.txt')
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

data_from_dom = read_dom_file(rlfap_folder_path,'dom2-f25.txt')
#print(data_from_dom)

def read_neigh_file(rlfap_folder_path, file_name_neigh):
    neigh_file_path = os.path.join(rlfap_folder_path, file_name_neigh)
    
    neigh_dict = {var: [] for var in data_from_var}
    with open(neigh_file_path, 'r') as file:
        n_lines = file.readlines()[1:]  # Skip the first line

        for var in data_from_var:
            for line in n_lines:
                first_number, second_number,symbol,value = line.split()  # Split the line into individual numbers
                first_number = int(first_number)
                second_number = int(second_number)
                if var == first_number:
                    neigh_dict[var].append(second_number)
                elif var == second_number:
                    neigh_dict[var].append(first_number)
    return neigh_dict

data_from_neigh = read_neigh_file(rlfap_folder_path,'ctr2-f25.txt')
#print(data_from_neigh)


def read_constr_file(rlfap_folder_path, file_name_constr):
    constr_file_path = os.path.join(rlfap_folder_path, file_name_constr)
    with open(constr_file_path, 'r') as file:
        lines = file.readlines()[1:]  
        constraints = []
        for line in lines:
            A, B, symbol, value = line.split()
            constraints.append((int(A), int(B), symbol, int(value)))
    return constraints

constr_data = read_constr_file(rlfap_folder_path, 'ctr2-f25.txt')

def constraints(A, a, B, b):
    for c in constr_data:
        if (c[0] == A and c[1] == B) or (c[0] == B and c[1] == A):
            if c[2] == '=':
                if abs(a-b) == c[3]:
                   return True
            elif c[2] == '>':
                if abs(a-b) > c[3]:
                    return True
    return False  


#result1 = constraints(0,240,1,2)
#print(result1)  

var_weight = {}

class RLFA(csp.CSP):
    def __init__(self,weight):
        csp.CSP.__init__(self,data_from_var,data_from_dom,data_from_neigh,constraints)

        self.weight = weight
        self.weights = {}  # Dictionary to hold value-weight associations

    def assign_weight_to_value(self, edge, weight):
        self.weights[edge] = weight
    
    # def find_const(self,var1,var2):
    #     c_tuple = ()
    #     tuple = ()
    #     for c in constr_data:
    #         if((c[0] == var1 and c[1] == var2) or (c[1] == var1 and c[0] == var2)):
    #             tuple = c_tuple + (c,)
    #     return tuple

problem = RLFA(1)
def initiliaze():
    for c in constr_data:
        var1 = c[0]
        var2 = c[1]
        edge1 = (var1,var2)
        edge2 = (var2,var1)
        
        problem.assign_weight_to_value(edge1,problem.weight)
        problem.assign_weight_to_value(edge2,problem.weight)

    for var in data_from_var:
        var_weight[var] = 0

initiliaze()

def fix_var_weights():
    for c in constr_data:
        var_1 = c[0] 
        var_2 = c[1]
        var_weight[var_1] += problem.value_weights[c] 
        var_weight[var_2] += problem.value_weights[c] 


def my_heuristic(assignment, csp):
    # csp.support_pruning()
    # min_fraction = float('inf')
    # selected_var = None
    # fix_var_weights()

    # for var in csp.variables:
    #     if var not in assignment:
    #         remaining_domain = len(csp.curr_domains[var])
    #         if remaining_domain > 0:
    #             fraction_calc = remaining_domain / var_weight[var]
    #             if fraction_calc < min_fraction:
    #                 min_fraction = fraction_calc
    #                 selected_var = var

    #return selected_var
    csp.support_pruning()  
    total_weight = {}
    for edge in csp.weights:
        var1, var2 = edge
        # if var1 in assignment.keys() or var2 in assignment.keys():
        #     continue 
        if var1 in total_weight.keys():
            value = total_weight[var1]
            value += csp.weights[edge]
            total_weight.update({var1 : value})
        else:
            total_weight[var1] = csp.weights[edge]
        if var2 in total_weight.keys():
            value = total_weight[var2]
            value += csp.weights[edge]
            total_weight.update({var2 : value})
        else:
            total_weight[var2] = csp.weights[edge]

    minim = None
    for var in total_weight:
        if var in assignment:
            continue
        cur_dom_wdeg = len(csp.curr_domains[var]) / total_weight[var]
        if minim == None:
            minim = (cur_dom_wdeg, var)
        elif cur_dom_wdeg < minim[0]:
            minim = (cur_dom_wdeg, var)
    if minim == None:
        pass
    return minim[1]


def call_search():
    result = csp.backtracking_search(problem,my_heuristic,csp.unordered_domain_values,csp.forward_checking)
    for i in result:
      print("result[{}] = ".format(str(i)), result[i])
    return result

t = Thread(target=call_search)

t.daemon = True

snooziness = 500
sleep(snooziness)

 

#print(len(result.keys()))

