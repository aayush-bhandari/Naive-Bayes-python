import pandas,math,sys,glob,os
from stop_words import get_stop_words
from collections import Counter

stop_words = set(get_stop_words('english'))
stop_words.update(['from:','subject:','>','>|'],',',':','.')


pathTrain = "20news-bydate/20news-bydate-train-5/"
all_folders_train = os.listdir(pathTrain)
print(all_folders_train)


pathTest = "20news-bydate/20news-bydate-test-5/"
all_folders_test = os.listdir(pathTest)
print(all_folders_test)

predictedRight = 0
predictedWrong = 0

def preprocessing(directory, path):

    for folder in directory:
        all_files = glob.glob(path + folder + '/*')
        print("All files length", len(all_files))
        outputfile = folder
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

def removestopwordstest(directory, path):
    print("Path", path)
    for folder in directory:
        all_files = os.listdir(path + folder + '/')
        #outputfile = folder
        for fname in all_files:
            outputdirectory = path + "test" + "/" + folder + "/"
            if not os.path.exists(outputdirectory):
                os.makedirs(outputdirectory)

            outputfile = outputdirectory + fname
            # outputfile = fname
            print("Output file: ", outputfile)
            fname = path + folder + '/' + fname
            print("Fname: ", fname)
            with open(outputfile, 'w') as outfile:
             with open(fname) as infile:
                for line in infile:
                    #print("Line: ", line)
                    if (line.strip()):  # to check if line is a empty line
                        a = line.rstrip().lower()
                        split = a.split()
                        for word in split:
                            #print("Word:", word)
                            if word not in stop_words:
                                outfile.write(word + " ")


def calculate_frequency(outerclass, innerclass, d):
    #Total words
    with open(outerclass) as f:
        totalwordsdict = Counter(f.read().split())
    total = totalword(totalwordsdict)
    print("Totalwords", total)
    uniquewords = len(totalwordsdict)
    print("Unique Words", uniquewords)

    if(outerclass == innerclass):
        with open(outerclass) as f:
            for word in totalwordsdict:
                totalwordsdict[word] = (totalwordsdict[word] + 1)  / (total + uniquewords)
            #print(totalwordsdict)
    '''else:
        with open(innerclass, 'r') as o:
            #with open(preprocessing_file[0], 'r') as o:
                for line in o:

                    if (line.strip()):  # to check if line is a empty line
                        a = line.rstrip().lower()
                        split = a.split()
                        for word in split:
                            if word not in stop_words

            for word in tmplist:
            tmplist = Counter(f.read().split())
            totalwords = 0
            uniquewords = len(tmplist)

            print("unique words", uniquewords)
            for word in tmplist:
               tmplist[word] = (tmplist[word] + 1)  / (totalwords + uniquewords)
            print(tmplist)'''

    return totalwordsdict


#cound cross count
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
    totalwords = 0
    for words in clas:
        totalwords = totalwords + clas[words]
    return totalwords

def findPrior(priorDict):
    totalNumberOfFiles = 0
    numberOfFilesInFolder = {}

    for folder in all_folders_train:
        all_files = glob.glob(pathTrain + folder + '/*')
        print("All files length", len(all_files))
        numberOfFilesInFolder[folder] = len(all_files)
        totalNumberOfFiles = totalNumberOfFiles + len(all_files)

    for folder in all_folders_train:
        priorDict[folder] = math.log(numberOfFilesInFolder[folder]/totalNumberOfFiles)


def testmodel(d, path, priorDict):
    for folder in path:
        classdict = d[folder]
        uniquewords = len(classdict)
        totalword = totalword(classdict)
        all_files = glob.glob(path + folder + '/*')
        print("All files length", len(all_files))
        maxValue = 0
        maxClass = ""
        for fname in all_files:
            for key in d:
                 sum = 0
                 with open(fname) as infile:
                    for line in infile:
                        if (line.strip()):  # to check if line is a empty line
                            a = line.rstrip().lower()
                            split = a.split()
                            for word in split:
                                if word not in d[key]:
                                    sum = sum + math.log(1 / (uniquewords + totalword))
                                else:
                                    sum = sum + math.log(d[key][word])
                    sum = sum + priorDict[key]
                    if(sum > maxValue):
                        maxValue = sum
                        maxClass = key
            if(maxClass != folder):



def main():
    preprocessing(all_folders_train, pathTrain)

    # Calculating Prior for each class
    priordict = {}
    findPrior(priordict)
    print("Prior Dict: ", priordict)

    # Calculation probability of each word in their respective file
    d = {}
    for outerclass in all_folders_train:
        d[outerclass] = {}
        #for innerclass in all_folders_test:
        d[outerclass] = calculate_frequency(outerclass, outerclass, d)
        #print(d[outerclass])
    print(d)

    removestopwordstest(all_folders_test, pathTest)
    processedtestdatapath = pathTest + "test/"
    testmodel(d, processedtestdatapath, priordict)
main()