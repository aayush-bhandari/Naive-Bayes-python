import pandas,math,sys,glob,os
from stop_words import get_stop_words
#stop_words = get_stop_words('english')
stop_words = set(get_stop_words('english'))
stop_words.update(['from:','subject:','>','>|'])


# file_os = os.listdir("20news-bydate/20news-bydate-test/misc.forsale/")
# print(file_os)

file_forsale = glob.glob("20news-bydate/20news-bydate-test/misc.forsale/*")
print(file_forsale)

path = "20news-bydate/20news-bydate-test-5/"
all_folders_test = os.listdir(path)
print(all_folders_test)


'''for file in file_forsale:
    with open(file) as f:
        text = f.read()
        #print(text)'''

#Merge all the files and create one
count =0
merged_file_names = []
for folder in all_folders_test:
    count = count+1
    all_files = glob.glob(path+folder+'/*')
    outputfile = 'out'+str(count)+'.txt'
    merged_file_names.append(outputfile)
    '''with open(outputfile,'w') as outfile:
        for fname in all_files:
            with open(fname) as infile:
                outfile.write(infile.read())'''

#remove stop
def remove_stopwords():
    processed_list = []
    for file in merged_file_names:
     preprocessing_file = glob.glob(file)
     with open(preprocessing_file[0],'r') as o:
        for line in o:
            if(line.strip()): # to check if line is a empty line
                a = line.rstrip().lower()
                split = a.split()
                #print(split)
                processed_list.append([word for word in split  if word not in stop_words])
        print(processed_list)
'''
#Merge all the files and create one
with open('output.txt','w') as outfile:
    for fname in file_forsale:
        with open(fname) as infile:
            outfile.write(infile.read())

concatenated_file = glob.glob("output.txt")

#print("hello",concatenated_file)

def remove_stopwords():
    processed_list = []
    with open(concatenated_file[0],'r') as o:
        for line in o:
            if(line.strip()): # to check if line is a empty line
                a = line.rstrip().lower()
                split = a.split()
                #print(split)
                processed_list.append([word for word in split  if word not in stop_words])
        print(processed_list)

'''
def main():
    remove_stopwords()


main()