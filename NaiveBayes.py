import pandas,math,sys,glob,os, shutil
from stop_words import get_stop_words
from collections import Counter

stop_words = set(get_stop_words('english'))
stop_words.update(['from:','subject:','>','>|'],',',':','.')


# pathTrain = "20news-bydate/20news-bydate-train-Sample/"
pathTrain = sys.argv[1]
all_folders_train = os.listdir(pathTrain)
print("Classes in traning data: ", all_folders_train)


# pathTest = "20news-bydate/20news-bydate-test-Sample/"
# pathTest = "20news-bydate/20news-bydate-test-5/"
pathTest = sys.argv[2]
all_folders_test = os.listdir(pathTest)
print("Classes in test data: ", all_folders_test)

predictedRight = 0
predictedWrong = 0


def removestopwordstest(listOfClasses, pathToClasses):
    if os.path.exists(pathToClasses + "test/"):
        shutil.rmtree(pathToClasses + "test/")

    for folder in listOfClasses:
        all_files = os.listdir(pathToClasses + folder + '/')
        for fname in all_files:
            outputdirectory = pathToClasses + "test" + "/" + folder + "/"
            if not os.path.exists(outputdirectory):
                os.makedirs(outputdirectory)
            ip = pathToClasses + folder + '/' + fname

            with open(os.path.join(outputdirectory, os.path.basename(fname)), 'w') as outfile:
                with open(ip) as infile:
                    for line in infile:
                        if (line.strip()):  # to check if line is a empty line
                            a = line.rstrip().lower()
                            split = a.split()
                            for word in split:
                                if word not in stop_words:
                                    outfile.write(word + " ")


def testmodel(trainedModel, path, priorDict):
    all_folders = os.listdir(path)
    for folder in all_folders:
        # print("Folder: ", folder)
        with open(folder) as f:
            totalwordsdict = Counter(f.read().split())
            totalword = getTotalWords(totalwordsdict)
            # print("Total words test: ", totalword)
            uniquewords = len(totalwordsdict)
            # print("Unique words test: ", uniquewords)

            all_files = glob.glob(path + folder + '/*')
            # print("All files length", len(all_files))
            for fname in all_files:
                maxValue = -1 * (sys.maxsize) - 1
                maxClass = ""
                for key in trainedModel:
                     sum = 0
                     with open(fname) as infile:
                        for line in infile:
                            if (line.strip()):  # to check if line is a empty line
                                a = line.rstrip().lower()
                                split = a.split()
                                for word in split:
                                    if word not in trainedModel[key]:
                                        sum = sum + math.log(1 / (uniquewords + totalword))
                                    else:
                                        sum = sum + math.log(trainedModel[key][word])
                        sum = sum + math.log(priorDict[key])
                        # print("Sum: %f Class %s", sum, key)
                        if sum > maxValue:
                            maxValue = sum
                            maxClass = key
                if(maxClass != folder):
                    global predictedWrong
                    predictedWrong = predictedWrong + 1
                else:
                    global  predictedRight
                    predictedRight = predictedRight + 1


def getTotalWords(dict):
    totalwords = 0
    for key in dict:
        totalwords = totalwords + dict[key]
    return totalwords


def calculate_frequency(outerclass, innerclass, d):
    with open(outerclass) as f:
        totalwordsdict = Counter(f.read().split())

        total = getTotalWords(totalwordsdict)
        # print("Totalwords: ", total)
        uniquewords = len(totalwordsdict)
        # print("Unique Words: ", uniquewords)

        if outerclass == innerclass:
            for word in totalwordsdict:
                totalwordsdict[word] = (totalwordsdict[word] + 1)  / (total + uniquewords)

    return totalwordsdict


def findPrior(priorDict):
     totalNumberOfFiles = 0
     numberOfFilesInFolder = {}

     for folder in all_folders_train:
         all_files_in_class = glob.glob(pathTrain + folder + '/*')
         numberOfFilesInFolder[folder] = len(all_files_in_class)
         totalNumberOfFiles = totalNumberOfFiles + len(all_files_in_class)

     for folder in all_folders_train:
         priorDict[folder] = numberOfFilesInFolder[folder] / totalNumberOfFiles


# Removes stop words and also creates a common file for each class
def preprocessing(listOfClasses, pathToClasses):
    # print("Path to training classes: ", pathToClasses)
    for eachClass in listOfClasses:
        all_files_in_class = glob.glob(pathToClasses + eachClass + '/*')
        outputfile = eachClass
        with open(outputfile,'w') as outfile:
            for fname in all_files_in_class:
                with open(fname) as infile:
                    for line in infile:
                        if (line.strip()):  # to check if line is a empty line
                            a = line.rstrip().lower()
                            split = a.split()
                            for word in split:
                                if word not in stop_words:
                                 outfile.write(word+" ")


def main():
    preprocessing(all_folders_train, pathTrain)

    # Calculating Prior for each class
    priorDict = {}
    findPrior(priorDict)
    print("Prior Dict: ", priorDict)

    # Calculating probability of each word in their respective file
    trainedModel = {}
    for outerclass in all_folders_train:
        #for innerclass in all_folders_test:
        trainedModel[outerclass] = calculate_frequency(outerclass, outerclass, trainedModel)
    # print("Trained Model: ", trainedModel)

    removestopwordstest(all_folders_test, pathTest)
    processedtestdatapath = pathTest + "test/"
    testmodel(trainedModel, processedtestdatapath, priorDict)

    print("Predicted right: ", predictedRight)
    print("Predicted wrong: ", predictedWrong)
    percentError = (predictedWrong/(predictedRight+predictedWrong)) * 100
    print("Percent error: ", percentError)

main()