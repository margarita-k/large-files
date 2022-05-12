import os
import sqlite3


# Function to save all the file paths and sizes in the selected directory
def get_full_paths(root_folder):
    files_dict = {}
    for root, directories, files in os.walk(root_folder):
        for file in files:
            full_path = os.path.join(root,file)
            size = os.path.getsize(full_path)
            files_dict[full_path] = size
    return files_dict

# Function to select the top N files from the input dictionary of files and sizes
def top_largest_files(files_dict, n):
    
    items_shown = 0
    file_sizes = {}

    for path, size in sorted(files_dict.items(), key = lambda x: x[1], reverse=True):
        if items_shown > n:
            break
        file_sizes[path] = size
        items_shown += 1
    return file_sizes

path = input('Please enter the full path to a folder to traverse: ')
max = int(input('Please enter the max amount of large files: '))

files_dict = get_full_paths(path)
large_files = top_largest_files(files_dict, max)


#Creating sqlite DB
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()
table = 'CREATE TABLE large_files(id integer primary key, path TEXT, bytes INTEGER)'
cursor.execute(table)
connection.commit()

# Adding large files to the database
for file, size in large_files.items():
    item = [file, size]
    cursor.execute('INSERT INTO large_files (path, bytes) VALUES(?,?)', item)
connection.commit()

for result in cursor.execute('SELECT * FROM large_files'):
    print(result)


# Ask user for a search query
num = -1
while num != 0:
    num = int(input("Please select the best option:\n0: exit\n1: search in path\n2: search in size\n>>"))
	
    if num == 1:
        query = input('Please enter a SQL search query to look in path: ')
        for result in cursor.execute(f'SELECT id, path, bytes FROM large_files WHERE path LIKE "{query}"'):
            print(result)

    elif num == 2:
        
        max = input('Please enter the maximum size (if none, leave empty):')
        min = input('Please enter the min size (if none, leave empty):')
        if max != '' and min != '':
            for result in cursor.execute(f"""SELECT id, path, bytes FROM large_files 
                WHERE bytes>{min}
                AND bytes<{max}"""):
                print(result)
        elif max == '' and min != '':
            for result in cursor.execute(f"""SELECT id, path, bytes FROM large_files 
                WHERE bytes>{min}"""):
                print(result)
        elif max != '' and min == '':
            for result in cursor.execute(f"""SELECT id, path, bytes FROM large_files 
                WHERE bytes<{max}"""):
                print(result)
        elif max == '' and min == '':
            print('Wrong request: at least one condition should be specified')


