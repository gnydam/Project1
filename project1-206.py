import os
import filecmp
from dateutil.relativedelta import *
from datetime import date, datetime
import csv

def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows
	infile = open(file)
	data = csv.reader(infile)
	counter = 0
	list_of_dicts = []
	for row in data:
	    if counter == 0: # we have the keys
	        first = row[0]
	        last = row[1]
	        email = row [2]
	        class_ = row [3]
	        DOB = row[4]
	        counter += 1
	    else:
	        d = {}
	        d[first]= row[0]
	        d[last] = row[1]
	        d[email] = row[2]
	        d[class_] = row[3]
	        d[DOB] = row[4]
	        list_of_dicts.append(d)
	infile.close()
	return list_of_dicts

def mySort(data,col):
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	first_item = sorted(data, key = lambda x:x[col])[0]
	full_name = first_item["First"] + " " + first_item["Last"]

	return full_name



def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	num_students_in_class = {}
	for students in data:
	    if students['Class'] in num_students_in_class:
	        num_students_in_class[students["Class"]] += 1
	    else:
	        num_students_in_class[students["Class"]] = 1
	return sorted(num_students_in_class.items(), key = lambda x: x[1], reverse = True)


def findMonth(a):
# Find the most common birth month form this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
	birthday_dict = {}
	for d in a:
	    month = d["DOB"].split('/')[0]
	    if month in birthday_dict:
	        birthday_dict[month] += 1
	    else:
	        birthday_dict[month] = 1
	return int(sorted(birthday_dict, key = lambda x: birthday_dict[x], reverse = True)[0])


def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
	sorted_data = sorted(a, key=lambda x:x[col])
	with open(fileName, 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    for row in sorted_data:
	        first = row['First']
	        last = row['Last']
	        email = row['Email']
	        writer.writerow([first, last, email])


def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.
	li = []
	format = '%m/%d/%Y'
	for d in a:
		dob = d['DOB']
		dob = datetime.strptime(dob, '%m/%d/%Y')
		today = date.today()
		diff = relativedelta(today, dob).years
		li.append(diff)

	return round(sum(li) / len(li))

		# go from dob to age in years



################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
