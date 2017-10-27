import pandas,math,sys,glob,os
from stop_words import get_stop_words
from collections import Counter
#stop_words = get_stop_words('english')
stop_words = set(get_stop_words('english'))
stop_words.update(['from:','subject:','>','>|'],',',':','.')


# file_os = os.listdir("20news-bydate/20news-bydate-test/misc.forsale/")
# print(file_os)

'''file_forsale = glob.glob("20news-bydate/20news-bydate-test/misc.forsale/*")
print(file_forsale)'''

path = "20news-bydate/20news-bydate-test-5/"
all_folders_test = os.listdir(path)
print(all_folders_test)


'''for file in file_forsale:
    with open(file) as f:
        text = f.read()
        #print(text)'''

#Merge all the files and create one
'''count =0
merged_file_names = []
for folder in all_folders_test:
    count = count+1
    all_files = glob.glob(path+folder+'/*')
    outputfile = 'out'+str(count)+'.txt'
    merged_file_names.append(outputfile)
    with open(outputfile,'w') as outfile:
        for fname in all_files:
            with open(fname) as infile:
                outfile.write(infile.read())'''



def preprocessing():
    #merged_file_names = []

    for folder in all_folders_test:
        all_files = glob.glob(path+folder+'/*')
        outputfile = folder
        #merged_file_names.append(outputfile)
        with open(outputfile,'w') as outfile:
            for fname in all_files:
                with open(fname) as infile:
                    for line in infile:
                        if (line.strip()):  # to check if line is a empty line
                            a = line.rstrip().lower()
                            split = a.split()
                            # print(split)
                            #processed_list.append([word for word in split if word not in stop_words])
                            for word in split:
                                if word not in stop_words:
                                 outfile.write(word+" ")

def calculate_frequencey(file):
    with open(file) as f:
        tmplist = Counter(f.read().split())
        totalwords = 0
        for words in tmplist:
            totalwords = totalwords + tmplist[words]
        uniquewords = len(tmplist)
        print(totalwords)
        print("unique words", uniquewords)
        for word in tmplist:
           tmplist[word] = (tmplist[word] + 1)  / (totalwords + uniquewords)
        print(tmplist)
        return tmplist

def cross_count(b):

    for classes in b:
        classdict = b[classes]
        uniquewords = len(classdict)
        totalwords = totalword(classdict)
        for innerclass in b:
            if(classes!=innerclass):
                for innerkey in innerclass:
                    if innerkey not in classdict:
                        b[classes][innerkey] = 1/(uniquewords+totalword)

def totalword(clas):
    for words in clas:
        totalwords = totalwords + clas[words]
    return totalwords
#remove stop
'''def remove_stopwords():
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
        print(processed_list)'''
'''

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
    preprocessing()
    d ={}

    for files in all_folders_test:
      d[files] = calculate_frequencey(files)
    print(d)




main()