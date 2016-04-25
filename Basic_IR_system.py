import sys
import math

arg = sys.argv[1] # call index.txt file in terminal; file created by perl command

''' 
The following function takes the index file as input and:
creates dictionary terms. 		Key = term, Value = lines in which the term appears, as a list
creates dictionary freq_dict. 	Key = term, Value = number of lines in which the term appears (frequency), as an integer
creates list words		    List of all unique terms in text 	For evaluating vocab size differences lower-case & upper-case
creates list postings		List of all lines (also called postings) in text
'''
def create_dict(arg): 
    with open(arg, 'r', encoding = 'utf-8') as fin: 
        terms = {}
        freq_dict = {}
        #words = []
        postings = []

        for line in fin: #iterate once over the text

            split_line = line.split() #splits each line into list of 2 values. First value is the term, second value is the line in which it appears
            #words.append(split_line[0])
            postings.append(split_line[1])

            if split_line[0] in terms:
                terms[split_line[0]].append(split_line[1])
                freq_dict[split_line[0]] += 1
            else:
                terms[split_line[0]]=[split_line[1]]
                freq_dict[split_line[0]]= 1
            
        #words = list(sorted(set(words)))
        return(terms, freq_dict, postings) #words


'''
The function prints and returns the number of words and the number of postings in the file. 
It takes as input:
Terms: is a dictionary whose keys are the (unique) terms in the text.
Postings: is a list of all the postings (including duplicates) in the text.
'''
def count_dict(terms, postings):
    t_size = len(terms)
    p_size = len(postings)
    print("Dictionary Size: ", t_size,"\nPostings: ", p_size)
    return t_size, p_size


'''
This function creates an inverted frequency dictionary called inv_index from the frequency dictionary created above.
inv_index has: Key = frequency, Value = words with this frequency
The main purpose of this function is to find the 10 most frequent words and return them as a list of stopwords, to be removed at wish in a separate function.
'''
def invert_dict(freq_dict):
    inv_index = {}
    freq_list = []
    for words, freqs in freq_dict.items():
        inv_index[freqs] = inv_index.get(freqs, [])
        inv_index[freqs].append(words)
    freq_list = inv_index.keys()
    top_ten = (sorted(freq_list, reverse = True)[:10]) #takes highest 10 frequencies and finds their corresponding terms
    stopwords = ([inv_index[x] for x in top_ten])
    stopwords = [num for elem in stopwords for num in elem] #flattening the list using list comprehension. Returns a list of all terms found in top 10 frequency
    #print(stopwords)
    stopwords = stopwords[:10] #reduce this list to first 10 terms
    return(inv_index, stopwords)

'''
This function removes the stopwords from the original dictionary (terms) containing words and their postings.
Stopwords are the terms which occur most often in a text and are unlikely to be queried, such as punctuation, determiners, coordination words etc.
'''
def stopword_inv_index(stopwords, index):
    for word in stopwords:
        if word in index.keys():
            del index[word]
    print ("Stopwords removed.")
    return(index)
    

#This function allows us to print and return the number of terms and postings in the dictionary of terms.
def count_dict2(index):
    count_term = len(index)
    print("Dictionary Size: ", count_term)

    count_post = 0
    posting = index.values()
    indices = [num for value in posting for num in value]
    for elem in indices:
        count_post+=1
    print("Postings: ", count_post)
    return count_term, count_post


# takes an index and a list of terms as arguments and returns a list contaning the postings for each word in the form of a sublist
def get_posting_lst(index, lst):
    posting_lst = []
    error = False
    for elem in lst:
        if elem in index:
            posting_lst.append(index[elem])
        else:
            print("Word in query missing from text: " + elem)
            raise SystemExit
    return posting_lst


def sort_posting_lst(lst): # sorts the elements in the lists (sublists of postings) according to their length
    return sorted(lst, key=len)

def intersection(lst1, lst2): # returns the intersection of two lists in a new list and counts the number of comparisons it takes to find the intersection
    intersected_lst = []
    count = 0
    for elem in lst1:
        count += 1
        if elem in lst2:
            count += 1
            intersected_lst.append(elem)

    return intersected_lst, count

'''
This function returns and prints the list of lines in which given terms occur together. It takes a list of terms as input. It makes use of the interesction function defined above.
It also prints the number of comparisions needed to find this result.
'''
def multiple_intersection(lst):
    if len(lst) == 1: # if there is only one term, it returns the posting for that term
        total_count = 0
        return lst, total_count
    else: # if there is more than one term, it calls the intersection function to compare the first with the second and, the resulting list is compared to the next one and so on
        final_intersection = lst[0]
        total_count = 0
        for number in range(1, len(lst)):
            final_intersection, count = intersection(final_intersection, lst[number])
            total_count += count
        print("Number of comparisons made: ", total_count)
        print("The terms in the query occur together in the following documents:")
        print(final_intersection)
        return final_intersection, total_count


#This function returns all postings of a given word, ie, the number of each line in which it appears.
def query(index, word):
    #print("Postings for " + word + ":")
    #print(inv_index[word])
    if word in index:
        return(index[word])
    else:
        print("Word not found")

'''
This function calculates the inverse document frequency of a given term. This IDF value indicates how "rare" a term is, and thus how informative its presence is in a certain document.
'''
def inverse_document_frequency(index):
    word = input("Enter term to calculate IDF: ")
    if word in index:    
        postings = query(index, word) # uses the query function to obtain the list of postings for the given term
    else:
        print ("Word not in text.")
        raise SystemExit
    doc_frequency = len(postings) # counts the number of postings to see how frequently the word occurs
    inverse_doc_frequency = math.log(1000/doc_frequency) # calculates the IDF: the logarithm of the total number of lines divided by the number of lines in which the   queried term occurs.
    print("IDF: ", inverse_doc_frequency)
    return(inverse_doc_frequency)


##################################################################################

terms, freq_dict, postings = create_dict(arg)


inv_dict, stopwords = invert_dict(freq_dict) # inv_dict no longer needed

count_dict2(terms) # count/print the number of words and postings
terms = stopword_inv_index(stopwords, terms) # remove the stopwords
count_dict2(terms) # count/print the number of words and postings

queried = input("Enter the terms of your query in lower case and separated by AND : ") # interface where the user enters the words of the query
queried_lst = queried.split(" AND ") # error handling to be added

posting_lst = get_posting_lst(terms, queried_lst) # create a list of lists containing the postings for each word in the query

sorted_posting_lst = sort_posting_lst(posting_lst) # this optimises the number of comparisons which need to be made to find the intersection of postings

final_intersection_list, total_count = multiple_intersection(sorted_posting_lst) # the list of lines in which the terms of the query occur together is printed and returned. The number of comparisons made to find the results is also printed and returned.

inverse_document_frequency(terms) # The value of the IDF is not saved, only printed. 
'''
The IDF value of a word is used to determine how informative it is about the texts which contain it 
(high IDF means high information value). 
It is used for ranking query results according to their relevance for the user. 
To complete the IR system, query ranking needs to be returned, along with the lines corresponding to posting numbers.
'''



