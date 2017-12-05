import glob
import re
import sys
import collections as cl

''' Function which takes input a stop words file and returns a list
    Input:  <stopwords file (with full location)>
    Output: <List containing all the stop words>                            '''
def readStopwords(stopwordsFile):
    stopwords = []
    #open the file to read contents
    with open(stopwordsFile, "r") as sf:
        for words in sf:
            words = words.split() [0]
            stopwords.append(words)
    return stopwords
        
''' Function which takes list containing file content and stopwords and 
    returns a dictionary containing the frequency of each word
    Input:  <filename(with full location)> <list containing stop words> 
    Output: <Dictionary containing words(filtered the stop words) and their 
            respective count>                                               '''                                                                               
def index(list1, stopwords):
    fileText = []
    pattern = '\'()*\".,:- '
    validString = '[^a-zA-Z0-9-_*\'.$-]'
    mydict = {}
    #Process file data and store in a list
    for lines in list1:
        #Convert the data in lower case
        lines = lines.lower()
        lines = (lines.split(' '))
        fileText.append(lines)
    #Process fileText and store in dictionary
    for i in range(len(fileText)):
        for j in range(len(fileText[i])):
            #Check if valid string or not
            t = re.sub(validString, '', fileText[i][j])
            #Remove front and trailing special characters
            t = t.strip('\n')
            t = t.strip(pattern)
            #Check if the processed word is not a stopword or empty
            if (t == '' or t in stopwords):
                continue;
            #Create Key Value pair and compute frequency of the key
            mydict[t] = mydict.get(t, 0) + 1
    return mydict

'''Function which takes input query, the Dictionary containing docId and 
    word frequencies and stopwords and returns the query search result 
   Input:  <query> <Dictionary (Query_word:Dictonary<docId:Word frequency>)>
           <stopwords>
   Output: <Dictionary (DocId:Word frequency in each document)>             '''
def search(query, finalDict, stopwords):
    #use the index function to get the word count
    mydict = index([query], stopwords)
    outDict = {}
    for key_input in mydict:
        eachDict = {}
        for key, valueDict in finalDict.iteritems():
            if (key_input in valueDict):
                eachDict[key] = valueDict[key_input]
            else:
                eachDict[key] = 0
            eachDict = cl.OrderedDict(sorted(eachDict.items()))
            outDict[key_input] = eachDict;
    return outDict

''' Function which takes input the path (where all .txt files are present), 
    stopwords list and returns a dictionary 
    Input:  <Full File Path (where .txt files are present)
    Output: Dictionary containing docId as key and frequencies of words (dict)
            as values                                                       '''
def question1(path, stopwords):
    finalDict = {}
    path += '/*.txt'
    for filename in glob.glob(path):
        with open(filename, "r") as f:
            list1 = []
            for lines in f:
                list1.append(lines)
        mydict = index(list1, stopwords)
        filename = filename.split('.')
        finalDict[filename[-2][-2:]] = mydict 
    return finalDict

''' Function which takes input the Dictionary containing docId and 
    word frequencies and returns the result                                
    Input:  <Dictionary (docId:Word Frequencies)>
    Output: Result to the query                                             '''
def question2(finalDict, stopwords):
    query = str(raw_input('Enter a query: '))
    print 'Processing input...'
    outDict = search(query, finalDict, stopwords)
    return outDict

'''Function which takes input the Dictonary containing docID and
   word frequencies of the given query and prints key and values
   Input:  <Dictionary (DocId:Word frequency)>
   Output: None                                                             '''    
def myprint(d):
    for key, value in d.iteritems():
        if isinstance(value, dict):
            print >> outf,"Word: ", key
            myprint(value)
        else:
            print >> outf,"\t", "doc: {0}, freq: {1}".format(key, value)

'''Function which takes input the Dictonary containing docID and
   word frequencies of the given query and prints in descending order
   Input:  <Dictionary (DocId:Word frequency)>
   Output: None                                                             '''
def myprint_descend(myList):
    sortedKeys = sorted(myList, key=myList.get, reverse=True)
    flag = 1
    for k in sortedKeys:
        flag = 0
        print >> outf,"\t", "({0}, {1})".format(k, myList[k])
    if (flag):
        print >> outf,"\t", "No results found!"

'''Function which takes input the Dictonary containing docID and
   word frequencies of the given query and returns the total frequency
   Input:  <Dictionary (DocId:Word frequency)>
   Output: <Dictionary (DocId:Total Word frequency)>                        '''
def getTotalFrequencyDoc(outDict, docs):
    myFreq = {}
    for key in outDict:
        for doc in docs:
            myFreq[doc] = myFreq.get(doc, 0) + outDict[key][doc]
    myFreq = cl.OrderedDict(sorted(myFreq.items()))
    return myFreq

'''Function which takes input the Dictonary containing docID and
   word frequencies of the given query and returns score greater than zero
   Input:  <Dictionary (DocId:Word frequency)>
   Output: <Dictionary (DocId:Total Word frequency > 0)>                    '''
def getScoreGreaterZero(outFreq):
    myFreqScore = {}
    for key, value in outFreq.iteritems():
        if value:
            myFreqScore[key] = value
    return myFreqScore

''' Main function '''
def main():

    folderPath = sys.argv[1]
    stopwordsFile = sys.argv[2]
    stopwords = readStopwords(stopwordsFile)
    finalDict = question1(folderPath, stopwords)
    outDict = question2(finalDict, stopwords)
    #Freq of each word in query - frequency in each document
    print >> outf,'\n', 'Word wise frequency per doc'
    myprint(outDict)
    #Total Frequency per doc
    outFreq = getTotalFrequencyDoc(outDict, finalDict.keys())
    print >> outf,'\n', 'Total Frequency per doc'
    myprint (outFreq)
    #docs whose score is greater than 0
    myFreqScore = getScoreGreaterZero(outFreq)
    print >> outf,'\n', 'Output list (search result): format (docid, score)'
    myprint_descend(myFreqScore)
    print 'Processing done.'
    
''' Calling the main function - starting point '''
if __name__ == "__main__":    
    #Redirects result to output file
    outFile = 'output.txt'
    outf = open(outFile, "w")
    main()
    print 'Please check the following file for output: ./', outFile
    outf.close()
    