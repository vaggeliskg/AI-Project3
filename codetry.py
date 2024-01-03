import os
import csp
from time import sleep
from time import time
from threading import Thread
# Path to the folder containing the rlfap folder
folder_path = 'C:\\Users\\vagge\\OneDrive\\Desktop\\AI'

# Path to the rlfap folder
rlfap_folder_path = os.path.join(folder_path, 'rlfap')

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


def read_dom_file(rlfap_folder_path, file_name_dom):
    dom_file_path = os.path.join(rlfap_folder_path, file_name_dom)
    dom_dict = {}
    rests = []
    with open(dom_file_path, 'r') as file:
        dom_lines = file.readlines()[1:]  # Skip the first line

        for line in dom_lines:
            first_number, rest = line.split(maxsplit=1)  # Split the line into individual numbers
            rests.append(list(map(int, rest.strip().split())))  # Split values into integers and store as lists
    
    var_file_path = os.path.join(rlfap_folder_path, 'var3-f11.txt')
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

def read_constr_file(rlfap_folder_path, file_name_constr):
    constr_file_path = os.path.join(rlfap_folder_path, file_name_constr)
    with open(constr_file_path, 'r') as file:
        lines = file.readlines()[1:]  
        constraints = []
        for line in lines:
            A, B, symbol, value = line.split()
            constraints.append((int(A), int(B), symbol, int(value)))
    return constraints

data_from_var = read_var_file(rlfap_folder_path,'var3-f11.txt')
data_from_dom = read_dom_file(rlfap_folder_path,'dom3-f11.txt')
data_from_neigh = read_neigh_file(rlfap_folder_path,'ctr3-f11.txt')
constr_data = read_constr_file(rlfap_folder_path, 'ctr3-f11.txt')

def constraints(A, a, B, b):
    for c in constr_data:
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

#var_weight = {}

class RLFA(csp.CSP):
    def __init__(self,weights,data_from_var,data_from_dom,data_from_neigh,constraints):
        csp.CSP.__init__(self,data_from_var,data_from_dom,data_from_neigh,constraints)

        self.weights = weights  # Dictionary to hold value-weight associations

    # def assign_weight_to_value(self, edge, weight):
    #     self.weights[edge] = weight
    
    # def find_const(self,var1,var2):
    #     c_tuple = ()
    #     tuple = ()
    #     for c in constr_data:
    #         if((c[0] == var1 and c[1] == var2) or (c[1] == var1 and c[0] == var2)):
    #             tuple = c_tuple + (c,)
    #     return tuple
        
def initiliaze():
    weights = {}
    for c in constr_data:
        var1 = int(c[0])
        var2 = int(c[1])
        edge1 = (var1,var2)
        edge2 = (var2,var1)

        if edge1 not in weights:
            #problem.assign_weight_to_value(edge1,problem.weight)
            weights[edge1] = 1
        if edge2 not in weights:
            #problem.assign_weight_to_value(edge2,problem.weight)
            weights[edge2] = 1

    return weights
    # for var in data_from_var:
    #     var_weight[var] = 0

weights = initiliaze()
problem = RLFA(weights,data_from_var,data_from_dom,data_from_neigh,constraints)

# def fix_var_weights():
#     for c in constr_data:
#         var_1 = c[0] 
#         var_2 = c[1]
#         var_weight[var_1] += problem.value_weights[c] 
#         var_weight[var_2] += problem.value_weights[c] 


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
    return minim[1]


def call_search():
    result = csp.backtracking_search(problem,my_heuristic,csp.unordered_domain_values,csp.forward_checking)
    for i in result:
      print("result[{}] = ".format(str(i)), result[i])
    print(len(result.keys()))
    return result

t = Thread(target=call_search)

t.daemon = True
t.start()

snooziness = 500
t.join(snooziness)

# import csp

# def getDomains_available(dom_file):
#     """Returns the Domains available"""

#     # For the domain file
#     domains_avail = {}
#     file = open(dom_file, 'r')
#     lines = file.readlines()
#     first_line = True
#     for line in lines:
#         if first_line:
#             first_line = False
#             continue
#         line_data = line.split()
#         cur_domain = line_data[0]
#         line_data.pop(0)
#         line_data.pop(0)
#         for i in range(len(line_data)):
#             line_data[i] = int(line_data[i])
#         domains_avail[cur_domain] = line_data

#     file.close()
#     return domains_avail


# def getVar_Dom(domains_avail, var_file):
#     """ Returns the Variables list and Domains dictionary"""
    
#     # For the variable file
#     domains = {}
#     variables = []
#     file = open(var_file, 'r')
#     lines = file.readlines()
#     first_line = True
#     for line in lines:
#         if first_line:
#             first_line = False
#             continue
#         line_data = line.split()
#         cur_var = line_data[0]
#         cur_domain = line_data[1]
#         variables.append(cur_var)
#         domains[cur_var] = domains_avail[cur_domain]

#     file.close()
#     return (variables, domains)


# save_ctr_data = {}
# has_constrains = {}
# def getNeighbors(variables, ctr_file):
#     """Returns the Neighbors dictionary and initializes save_ctr_data"""

#     # Initialize has_constrains dictionary
#     for i in range(len(variables)):
#         has_constrains[str(i)] = False

#     # For the constrains file
#     neighbors = {}
#     file = open(ctr_file, 'r')
#     lines = file.readlines()
#     first_line = True
#     for line in lines:
#         if first_line:
#             first_line = False
#             continue
#         line_data = line.split()

#         # For x
#         x = line_data[0]
#         has_constrains[x] = True
#         constrain_var = line_data[1]
#         keys = neighbors.keys()
#         if x in keys:
#             new_neighbors = neighbors[x]
#             new_neighbors.append(constrain_var)
#             neighbors.update({x : new_neighbors})
#         else:
#             neighbors[x] = [constrain_var]

#         # For constraints function
#         keys = save_ctr_data.keys()
#         if x in keys:
#             new_list = save_ctr_data[x]
#             new_list.append(line_data)
#             save_ctr_data.update({x : new_list})
#         else:
#             save_ctr_data[x] = [line_data]

#         # For y
#         y = line_data[1]
#         # has_constrains[y] = True
#         constrain_var = line_data[0]
#         keys = neighbors.keys()
#         if y in keys:
#             new_neighbors = neighbors[y]
#             new_neighbors.append(constrain_var)
#             neighbors.update({y : new_neighbors})
#         else:
#             neighbors[y] = [constrain_var]

#     for i in variables:
#         if neighbors.get(i) == None:
#             neighbors[i] = []

#     file.close()
#     return neighbors


# def constraints(A, a, B, b):
#     """ Uses "save_ctr_data" to not constantly open and close the file
#         to check every constrain """
    
#     A = str(A)
#     B = str(B)

#     # Check A constrains
#     if has_constrains[A] == True:
#         A_constr = save_ctr_data[A]
#         # print(A_constr)
#         for constrain in A_constr:
#             y = constrain[1]
#             compare = constrain[2]
#             k = int(constrain[3])
#             if y == B:
#                 if compare == '>':
#                     if abs(a-b) > k:
#                         continue
#                     else:
#                         return False
#                 elif compare == '=':
#                     if abs(a-b) == k:
#                         continue
#                     else:
#                         return False
                
#     # Check B constrains
#     if has_constrains[B] == True:
#         B_constr = save_ctr_data[B]
#         for constrain in B_constr:
#             y = constrain[1]
#             compare = constrain[2]
#             k = int(constrain[3])
#             if y == A:
#                 if compare == '>':
#                     if abs(b-a) > k:
#                         continue
#                     else:
#                         return False
#                 elif compare == '=':
#                     if abs(b-a) == k:
#                         continue
#                     else:
#                         return False

#     # Passed all constrains
#     return True
        

# def update_conflict_set(conflict_set, var, neighbor):
#     """Updates conflict set"""
#     if var in conflict_set.keys():
#         if neighbor not in conflict_set[var]:
#             new_conflicts = conflict_set[var]
#             new_conflicts.append(neighbor)
#             conflict_set.update({var : new_conflicts})
#     else:
#         conflict_set[var] = [neighbor]

# class RLFA(csp.CSP):
#     """Class to solve RLFA problem"""

#     def __init__(self, variables, domains, neighbors, constraints, weights, conflict_set):
#         """Initialize data structures for RLFA."""
#         csp.CSP.__init__(self, variables, domains, neighbors, constraints)
#         self.weights = weights
#         self.conflict_set = conflict_set

#     # def support_pruning(self):
#     #     """Make sure we can prune values from domains. (We want to pay
#     #     for this only if we use it.)"""
#     #     if self.curr_domains is None:
#     #         self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

#     def RLFA_nconflicts(self, var, val, assignment):
#         """Return the number of conflicts var=val has with other variables
#         and update the conflict set"""

#         # Subclasses may implement this more efficiently
#         def conflict(var2):
#             if var2 in assignment:
#                 if not self.constraints(var, val, var2, assignment[var2]):
#                     update_conflict_set(self.conflict_set, var, var2)
#                     return True
#             return False

#         return csp.count(conflict(v) for v in self.neighbors[var])

# def dom_wdeg(assignment, csp):
#     """Find the variable with min dom_size/weight"""
#     csp.support_pruning()  
#     total_weight = {}
#     for edge in csp.weights:
#         var1, var2 = edge
#         # if var1 in assignment.keys() or var2 in assignment.keys():
#         #     continue 
#         if var1 in total_weight.keys():
#             value = total_weight[var1]
#             value += csp.weights[edge]
#             total_weight.update({var1 : value})
#         else:
#             total_weight[var1] = csp.weights[edge]
#         if var2 in total_weight.keys():
#             value = total_weight[var2]
#             value += csp.weights[edge]
#             total_weight.update({var2 : value})
#         else:
#             total_weight[var2] = csp.weights[edge]

#     minim = None
#     for var in total_weight:
#         if var in assignment:
#             continue
#         cur_dom_wdeg = len(csp.curr_domains[var]) / total_weight[var]
#         if minim == None:
#             minim = (cur_dom_wdeg, var)
#         elif cur_dom_wdeg < minim[0]:
#             minim = (cur_dom_wdeg, var)
#     if minim == None:
#         pass
#     return minim[1]

# def CBJ(problem, select_unassigned_variable, order_domain_values, inference):
#     """Implementation of conflict-directed-backjumping - CBJ"""

#     def backjump(assignment, conflict_set):
#         if len(assignment) == len(problem.variables):
#             return assignment
#         var = select_unassigned_variable(assignment, problem)
#         for value in order_domain_values(var, assignment, problem):
#             if 0 == problem.RLFA_nconflicts(var, value, assignment):
#                 problem.assign(var, value, assignment)
#                 removals = problem.suppose(var, value)
#                 if inference(problem, var, value, assignment, removals):
#                     result = backjump(assignment, conflict_set)
#                     # if result is not None:
#                     #     return result 
#                     if type(result) == dict:
#                         return result
#                     elif type(result) == tuple:
#                         print("hello!")
#                         dest_var, extent_conflicts = result
#                         if var != dest_var:
#                             return result
#                         elif var == dest_var:
#                             new_conflicts = conflict_set[var]
#                             new_conflicts.append(extent_conflicts)
#                             conflict_set.update({var : new_conflicts})
#                 problem.restore(removals)
#             else:
#                 print("hello!")
#         problem.unassign(var, assignment)

#         if var in conflict_set:
#             conflicting_neighbors = conflict_set[var]
#             last_conflict_neighbor = conflicting_neighbors.pop()
#             return (last_conflict_neighbor, conflicting_neighbors)
#         else:
#             return None



#     # conflict_set = {}
#     result = backjump({}, problem.conflict_set)
#     assert result is None or problem.goal_test(result)
#     return result

# def create_names(file_id):
#     """Creates the names for the files with the argument file_id"""
#     var_file = "rlfap\\" + "var" + file_id + ".txt"
#     dom_file = "rlfap\\" + "dom" + file_id + ".txt"
#     ctr_file = "rlfap\\" + "ctr" + file_id + ".txt"
#     return (var_file, dom_file, ctr_file)

# def solve_instance(instance_number, search_algorithm, var_heuristic, Inference):
#     """Solve an instance of the problem, with a search algorithm a variable heuristic
#     and an Inference"""

#     # Choose the instance you want to run
#     # Change the number of instance_number for a different instance
#     instance_number = instance_number
#     file = open('file_names.txt', 'r')
#     lines = file.readlines()
#     file_id = str(lines[instance_number])
#     file_id = file_id[0 : len(file_id)-1]
#     file.close()

#     # Get the file names
#     names = create_names(file_id)

#     # Create variables, domains and neightbors
#     domains_avail = getDomains_available(names[1])
#     var_dom = getVar_Dom(domains_avail, names[0])
#     variables = var_dom[0]
#     domains = var_dom[1]
#     neighbors = getNeighbors(variables, names[2])

#     # Initialize weights
#     weights = {}
#     for var in save_ctr_data:
#         for ctr in save_ctr_data[var]:
#             # Each edge has 2 sides
#             edge1 = (ctr[0], ctr[1])
#             if edge1 not in weights.keys():
#                 weights[edge1] = 1
#             edge2 = (ctr[1], ctr[0])
#             if edge2 not in weights.keys():
#                 weights[edge2] = 1


#     # Solve the problem
#     problem = RLFA(variables, domains, neighbors, constraints, weights, {})
#     result = search_algorithm(problem, var_heuristic, csp.unordered_domain_values, Inference)
    
#     # Print Result
#     if result == None:
#         print("result:", result)
#     else:
#         print("result:")
#         for i in result:
#             print("result[{}] = ".format(str(i)), result[i])
#     print("\ninstance:", file_id)

#     return True

# # Main
# from time import sleep
# from time import time
# from threading import Thread

# def solve():
#     instance_number = 3
#     start_time = time()
#     solve_instance(instance_number, csp.backtracking_search, dom_wdeg, csp.forward_checking)
#     print("time needed:", time() - start_time)

# cur_thread = Thread(target=solve)
# cur_thread.daemon = True
# cur_thread.start()
# seconds = 500
# sleep(seconds)










