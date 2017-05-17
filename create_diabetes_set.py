import os


##Create a list of paths for the 70 diabetes-data files & remove non-data files
paths=[]

for filename in os.listdir('Diabetes-Data'):
    paths.append((os.path.join('Diabetes-Data', filename)))


paths.remove('Diabetes-Data/Domain-Description')
paths.remove('Diabetes-Data/README-DIABETES')
paths.remove('Diabetes-Data/.DS_Store')
paths.remove('Diabetes-Data/Data-Codes')

#print paths

##Create a list of tuples, where tuple[0] is the path & tuple[1] is the count of lines in that path. The results will
##give an idea of how much data is in each source file
list_of_counts =[]


test = 0
i=0
while i < len(paths):
    for line in open(paths[i], 'rU'):
        test = test + 1
    list_of_counts.append((paths[i],test))
    i = i + 1
    test = 0

print list_of_counts

##Add all of the line counts in a variable called total. Compare total to subsequent variable, counts, to make sure concatenated diabetes file has all data

total = 0
for couple in list_of_counts:
    total = total + couple[1]
print total



##Concatenate the 70 files of diabetes input into one file called diabetes_concatenated.txt. Compare sum of lines (count) to sum of individual file's lines
count = 0
with open('diabetes_concatenated.txt', 'w') as outfile:             #http://stackoverflow.com/questions/13613336/python-concatenate-text-files
    for fname in paths:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
                count = count + 1
print count