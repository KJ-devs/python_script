import os
import time
import re
import xlsxwriter

def walk_directory(directory_path):
    workbook = xlsxwriter.Workbook('List_User_Printer.xlsx')
    
    worksheet = workbook.add_worksheet()
    worksheetHeader = ('User', 'PC', 'Reseau')
    for i in range(len(worksheetHeader)):
        row = 0
        col = 0
        worksheet.write(row, col + i, worksheetHeader[i])
    for foldername, subfolders, filenames in os.walk(directory_path):
        row = 1
        col = 0
        for filename in filenames:
            with open(os.path.join(foldername, filename), 'r') as open_file:
                lines = open_file.readlines()  # Read file line by line
                
                file = filename
                filename = filename.replace('.txt', '')
                data = filename.rsplit('.',1)
                user = data[0]
                pc = data[1]
                
                if os.path.getsize(os.path.join(foldername, file)) > 0:
                    matches = []
                    for line in lines:
                        match = re.findall(r'\\([^\\]*)$', line) # Apply regex for each line
                        matches.extend(match)
                    for match in matches:
                        worksheet.write(row, col, user)
                        worksheet.write(row, col+1, pc)
                        worksheet.write(row, col+2, match) 
                        row += 1
                else: 
                    # Continue to next file if current file is empty
                    continue
    workbook.close()

if __name__ == "__main__":
    start_time = time.time()
    
    print('Enter path to directory to scan: ')
    path = input();
    walk_directory(path)

    end_time = time.time()
    End_time_To_Minute = (end_time - start_time) / 60
    print(f"\nLe script a pris {End_time_To_Minute} minutes pour s'exécuter.")
