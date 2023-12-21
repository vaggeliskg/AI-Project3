import os

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
data_from_txt = read_var_file(rlfap_folder_path,'var2-f24.txt')


def read_dom_file(rlfap_folder_path, file_name_dom):
    dom_file_path = os.path.join(rlfap_folder_path, file_name_dom)
    dom_dict = {}
    rests = []

    var_dict = read_var_file(rlfap_folder_path, 'var2-f24.txt')  # Get the dictionary of variables and indicators
    
    with open(dom_file_path, 'r') as file:
        dom_lines = file.readlines()[1:]  # Skip the first line

        for line in dom_lines:
            first_number,rest = line.split(maxsplit=1)  # Split the line into individual numbers
            rests.append(rest)

    var_file_path = os.path.join(rlfap_folder_path, 'var2-f24.txt')
    with open(var_file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line
        for line in lines:
            first_num, second_num = line.split()
            if second_num == first_number[0]: 
                dom_dict[first_num] = {rests[0]}
            else:
                dom_dict[first_num] = {rest[1]}

    return dom_dict

data_from_dom = read_dom_file(rlfap_folder_path,'dom2-f24.txt')
print(data_from_dom)