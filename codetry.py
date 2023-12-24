import os
import csp

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
data_from_var = read_var_file(rlfap_folder_path,'var3-f10.txt')
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
    
    var_file_path = os.path.join(rlfap_folder_path, 'var3-f10.txt')
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

data_from_dom = read_dom_file(rlfap_folder_path,'dom3-f10.txt')
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

data_from_neigh = read_neigh_file(rlfap_folder_path,'ctr3-f10.txt')
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

constr_data = read_constr_file(rlfap_folder_path, 'ctr3-f10.txt')

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

#class RLFA(csp.CSP):
    #def __init__(self)

problem = csp.CSP(data_from_var,data_from_dom,data_from_neigh,constraints)
result = csp.backtracking_search(problem,csp.mrv,csp.unordered_domain_values,csp.forward_checking)
print(len(result.keys()))