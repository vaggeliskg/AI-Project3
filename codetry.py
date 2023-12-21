import os

# Path to the folder containing the rlfap folder
folder_path = '/Users/vaggelis_kalabokis/Desktop/AI_Project_3/My_project'

# Path to the rlfap folder
rlfap_folder_path = os.path.join(folder_path, 'rlfap')

# Path to the specific .txt file within rlfap folder
txt_file_path = os.path.join(rlfap_folder_path, 'var2-f24.txt')

def read_txt_file():
    data_list = []
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
        # Skip the first line
        for line in lines[1:]:
            # Split each line by space and take the first number
            first_number = line.split()[0]
            # Append the first number to the data_list
            data_list.append(int(first_number))  # Convert to int and append
    
    return data_list

# Call the function to read the .txt file and store its contents in a list
data_from_txt = read_txt_file()

print(data_from_txt)

