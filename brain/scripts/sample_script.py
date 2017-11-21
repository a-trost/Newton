import datetime
import sys,os
from os import listdir
import re


from brain.models import StudentRoster

from brain.models import ReadingStats
import csv

csv_list = listdir('brain/scripts/csvdownloads')  # Gets the downloaded file list from the directory
lexile_files = []
score_grid_files = []
ixl_stats_files = []
for x in range(len(csv_list)):  # Starts to sort all the data into 1 csv for each data type
    current_file = csv_list[x]
    # Figure out which file we're working with (lexile, Score-Grid, or ixlstats)
    if 'lexile' in current_file:
        lexile_files.append(current_file)
        print("File {} is Lexile".format(current_file))
    elif 'Score-Grid' in current_file:
        score_grid_files.append(current_file)
        print("File {} is Score Grid".format(current_file))
    elif 'ixlstats' in current_file:
        print("File {} is IXL Stats".format(current_file))
    else:
        print("File {} Not Recognized".format(current_file))

for file in lexile_files:
    dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0] == 'student_user_id':
            continue
        elif row[0] != 'student_user_id':
            last_name = row[2]
            print("Last Name: {}".format(last_name))
            first_name = row[3]
            print("First Name: {}".format(first_name))
            test_count = row[12]
            print("Test count : {}".format(test_count))
            lexile_score = row[8]
            print("Lexile Score : {}".format(lexile_score))
            try:
                student = StudentRoster.objects.get(first_name=first_name, last_name=last_name)
                defaults = {'current_lexile': lexile_score, 'myon_tests_taken': test_count}
                obj, created = ReadingStats.objects.update_or_create(
                    student=student,
                    defaults=defaults,
                )
                print("Object: {}, Created: {}".format(obj, created))
            except:
                print("Couldn't find Student Object")
