#author: Kyle Wiese
#CSCI 5832
#Programming Assignment 2
import sys
import math

#Global variables to count tokens, sentences, and types
tokens = 0
types = 0
sentence_count = 0

#Arguments: Training File
#Return Values: A dictionary containing all unigrams and their respective counts
#This function takes in a training file, parses it based on white space, and counts each
#unigram found
def unigramTraining(training_filename):
    #define variables
    unigram_occurances = {}
    global tokens
    global types
    global sentence_count
    try:
        #open file and parse it
        with open(training_filename, "r") as f:
            for line in f:
                words = line.split()
                
                #for each word, add 1 to token.
                for word in words:
                    word = word.lower()
                    tokens = tokens + 1
                    
                    #for each new word, add to dictionary aswell as adding 1 to types
                    if word not in unigram_occurances:
                        unigram_occurances[word] = 1
                        types = types + 1
                        
                    #each time a word is seen thats in the dictionary, add one to its value
                    else:
                        unigram_occurances[word] = unigram_occurances[word] + 1
                        
                #each line is equivalent to a sentence, so add 1 to "sentence_count" for each new line
                sentence_count = sentence_count + 1
            f.close()
    except IOError: #simple file error handling
        print("Error: Could not read the training file: {}".format(training_filename))
        return -1
    return unigram_occurances

#Arguments: Training File
#Return Values: A dictionary containing all birgrams and their respective counts
#This function takes in a training file, parses it based on white space, and counts each
#possible found
def bigramTraining(training_filename):
    #declare dictionary
    bigram_occurances = {}
    try:
        #open file and parse it
        with open(training_filename, "r") as f:
            for line in f:
                words = line.split()
                
                #insert begining and end tags
                words.insert(0,"<s>")
                words.append("</s>")
                i = 0
                
                #iterate through all words in the sentence (word = current word = w(n-1) in the bigram)
                for word in words:
                    word = word.lower()
                    
                    #for each word (not ending tag) make a bigram of that word and the next
                    if word != "</s>":
                        var = word + " " + words[i+1]
                        
                        #if the bigram isnt in the dictionary add it
                        if var not in bigram_occurances:
                            bigram_occurances[var] = 1
                            
                        #else, add 1 to that bigram's dictionary value
                        else:
                            bigram_occurances[var] = bigram_occurances[var] + 1
                    i = i + 1
            f.close()
    except IOError: #simple file error handling
        print("Error: Could not read the training file: {}".format(training_filename))
        return -1
    return bigram_occurances

#Returns the probabilities to stdout
def main():
    #declare variables
    global tokens
    global types
    global sentence_count
    
    #use training set to get data set
    unigram_table = unigramTraining(sys.argv[1])
    bigram_table = bigramTraining(sys.argv[1])
    try:
        #open test file and parse it
        with open(sys.argv[2], "r") as f:
            for line in f:
                print("")
                print("S = " + line)
                
                #declare sentence variables
                u_prob = []
                b_prob = []
                s_b_prob = []
                final_u_prob = 0
                final_b_prob = 0
                final_s_b_prob = 0
                
                words = line.split()
                
                #add start and end tags to line
                words.insert(0,"<s>")
                words.append("</s>")
                i = 0
                sentence_flag = 0 #Set to one when a sentence is found to be invalid (a bigram doesnt appear)
                
                #iterate through all words in the sentence (word = current word = w(n-1) in the bigram)
                for word in words:
                    word = word.lower()
                   
                    #Unigram Prob:
                    #if the current word does not equal an end or beginning tag (Unigrams don't take them into account)
                    #check to see if the current word is in the unigram dictionary
                    if (word != "<s>" and word != "</s>"):
                       
                        #if the current word is in the dictionary, take the number of occurences/number of tokens to get the probability
                        if word in unigram_table:
                            prob = math.log10(unigram_table[word]/tokens)
                            u_prob.append(prob)
                        
                        #if the word isnt in the unigram dictionary, the probability of that word is 0
                        else:
                            u_prob.append(0)
                   
                    #Bigram Prob:
                    #if the word isnt an end tag (since no bigrams should start with that tag) go into bigram checks
                    if word != "</s>":
                        
                        #form a bigram from the current word and the following word
                        b_check = word + " " + words[i + 1]
                        
                        #if that bigram is present in the bigram dictionary, go into probability calculations
                        if b_check in bigram_table:
                           
                            #grab w(n-1)'s count from the unigram dictionary
                            if word in unigram_table:
                               
                                #if the sentence is still valid, calculate the probability of that bigram using MLE
                                if(sentence_flag == 0):
                                    prev_count = unigram_table[word]
                                    b_count = bigram_table[b_check]
                                    prob = math.log10(b_count/prev_count)
                                    
                                    #append probability to list
                                    b_prob.append(prob)

                                #for smoothed bigrams, no need to check for sentence validity and use the add-one smoothing equation
                                sprev_count = unigram_table[word] + types
                                b_count = bigram_table[b_check] + 1
                                prob = math.log10(b_count/sprev_count)
                                
                                #append probability to list
                                s_b_prob.append(prob)
                            #since unigrams do not consider the sentence tag, check to see if the current word is the beginning sentence tag
                            elif word == "<s>":
                                #if the sentence is still valid, use the sentence count for the w(n-1) count and calculate the MLE probability for the bigram
                                if(sentence_flag == 0):
                                    prev_count = sentence_count
                                    b_count = bigram_table[b_check]
                                    prob = math.log10(b_count/prev_count)
                                    #append probability to list
                                    b_prob.append(prob)

                                #for the smoothed bigrams, no need to check for sentence validity and use the sentence count for the w(n-1) count and use add-one smoothing to calculate the probability of that bigram
                                sprev_count = sentence_count + types
                                b_count = bigram_table[b_check] + 1
                                prob = math.log10(b_count/sprev_count)
                                #append probability to list
                                s_b_prob.append(prob)

                        #if bigram is not in the bigram dictionary
                        else:
                            #for non-smoothed bigrams, make the sentence probability 0 and set the "sentence flag" to 1 to mark the sentence invalid
                            b_prob = [0]
                            sentence_flag = 1
                            
                            #Smoothed Bigrams:
                            #Check to see if the word (w(n-1)) is in the unigram table and calculate the probability using that
                            if word in unigram_table:
                                s_b_prob.append(math.log10(1/(unigram_table[word] + types)))
                            
                            #else if the word is a start tag, use the sentence count as w(n-1)'s count
                            elif word == "<s>":
                                s_b_prob.append(math.log10(1/(sentence_count + types)))
                           
                            #if non of the above cases is met, use 0 as the count for w(n-1)'s count
                            else:
                                s_b_prob.append(math.log10(1/types))

                    i = i + 1

                #calculate the final probabilities for the unigrams, bigrams, and smoothed bigrams by adding up the individual probabilities
                for x in u_prob:
                    final_u_prob = final_u_prob + x

                for k in b_prob:
                    final_b_prob = final_b_prob + k

                for j in s_b_prob:
                    final_s_b_prob = final_s_b_prob + j


                #format the output (if probability is 0, print undefined instead)
                if final_u_prob == 0:
                    final_u_prob = "Undefined"
                    print("Unigrams: logprob(S) = {}".format(final_u_prob))
                else:
                    print("Unigrams: logprob(S) = {:.4f}".format(final_u_prob))

                if final_b_prob == 0:
                    final_b_prob = "Undefined"
                    print("Bigrams: logprob(S) = {}".format(final_b_prob))
                else:
                    print("Bigrams: logprob(S) = {:.4f}".format(final_b_prob))

                if final_s_b_prob == 0:
                    final_s_b_prob = "Undefined"
                    print("Smoothed Bigrams: logprob(S) = {}".format(final_s_b_prob))
                else:
                    print("Smoothed Bigrams: logprob(S) = {:.4f}".format(final_s_b_prob))

            f.close()

    except IOError: #simple file error handling
        print("Error: Could not read the test file: {}".format(sys.argv[2]))
        return -1

if __name__ == "__main__":
    main()
