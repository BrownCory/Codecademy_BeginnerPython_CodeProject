"""
These are the emails you will be censoring. The open() function is opening 
the text file that the emails are contained in and the .read() method is 
allowing us to save their contents to the following variables:
"""
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

"""
This function censors the string 'phrase' in the body of text 'text' by 
replacing it with the censor_string. 

The phrase is censored whether it is all lowercase, all uppercase, or in the 
title format. It also preserves punctuation surrounding the phrase and the
length of the pharse. Finally, plural versions that end in 's' are also 
censored.
"""

censor_symbol = "*" # choose symbol: @, #, $, %, &, *

def censor_phrase(phrase, text):
    # create a censored phrase the same length of the input phrase
    censored_phrase = [symbol if symbol == " " else censor_symbol for symbol\
                       in phrase]
    censored_phrase = "".join(censored_phrase)
    
    # censor phrase
    preceding_characters = [" ", "\n", "("]
    succeeding_characters = [" ", ",", ".", "!", "?", ")"]
    phrases = [precede + phrase + succeed for precede in preceding_characters\
               for succeed in succeeding_characters]

    for word in phrases:
        text = text.replace(word, word[0] + censored_phrase + word[len(word)-1])
        text = text.replace(word.title(), word[0] + censored_phrase + word[len(word)-1])
        text = text.replace(word.upper(), word[0] + censored_phrase + word[len(word)-1])
    
    # censor phrase with s add (making it plural)
    censored_phrase = censored_phrase + "*"
    succeeding_characters_with_s = ["s ", "s,", "s.", "s!", "s?", "s)"]
    phrases = [precede + phrase + succeed for precede in preceding_characters\
               for succeed in succeeding_characters_with_s]
    for word in phrases:
        text = text.replace(word, word[0] + censored_phrase + word[len(word)-1:])
        text = text.replace(word.title(), word[0] + censored_phrase + word[len(word)-1:])
        text = text.replace(word.upper(), word[0] + censored_phrase + word[len(word)-1:])
    return text

"""
Censor the phrase "learning algorithms" from email_one.txt
"""
new_email_one_str = censor_phrase("learning algorithms", email_one)
email_one_censored = open("email_one_censored.txt", "w+").write(new_email_one_str)

"""
This function censors all the words in the list of phrases 'list_of_phrases'
in the body of the text 'text' by replacing it with the string "*****"
"""
def censor_list_of_phrases(list_of_phrases, text):
    for phrase in list_of_phrases:
        text = censor_phrase(phrase,text)
    return text
    
"""
Censor the phrases "she", "personality matrix", "sense of self", 
"self-preservation", "learning algorithm", "her", and "herself" from 
email_two.txt
"""
proprietary_terms = ["she", "personality matrix", 
"sense of self", "self-preservation", "learning algorithm", "her", "herself"]
new_email_two_str = censor_list_of_phrases(proprietary_terms,
                                           email_two)
email_two_censored = open("email_two_censored.txt", "w").write(new_email_two_str)

"""
This function censors all proprietary_terms from 'text', as well as all 
negative_words after they have occured twice.
"""
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", 
                  "alarmed", "out of control", "help", "unhappy", "bad", 
                  "upset", "awful", "broken", "damage", "damaging", "dismal", 
                  "distressed", "concerning", "horrible", 
                  "horribly", "questionable"]
def censor_proprietary_and_negative_phrases(negative_words, list_of_phrases,
                                            text):
    text = censor_list_of_phrases(list_of_phrases, text)
    
    for word in negative_words:
        #find first occurence
        location = text.find(word)
        if location == -1:
            break
        else:
            prestring = text[:location + len(word)]
            substring = text[location + len(word):]
        #find second occurence
        location2 = substring.find(word)
        if location2 == -1:
            break
        else:
            prestring2 = substring[:location2 + len(word)]
            substring2 = substring[location2 + len(word):]
        #find third occurence
        location3 = substring.find(word)
        if location3 == -1:
            break
        else:
            prestring3 = substring[:location3 + len(word)]
            substring3 = substring[location3 + len(word):]
            substring3_censored = censor_phrase(word, substring3)
            
        #put strings together
        text = prestring + prestring2 + prestring3 + substring3_censored
    
    return text
        
"""
Censor the negative and proprietary terms from email_three
"""
new_email_three_str =\
censor_proprietary_and_negative_phrases(negative_words, proprietary_terms,
                                        email_three)
email_three_censored = open("email_three_censored.txt", "w").write(new_email_three_str)

def censor_letters_in_string(string):
    punctuation_symbols = ",.?!()\n"
    
    for index_in_string in range(len(string)):
        if punctuation_symbols.find(string[index_in_string]) == -1:
            # current symbol is a letter that need to be censored
            string = string[:index_in_string] + censor_symbol +\
            string[index_in_string + 1:]
            
    return string
        
        

"""
This function censors all proprietary_terms and negative_terms from 'text'. In
addition it censors all words that occur before AND after a term in one of these
lists
"""
def censor_many_words(list_of_phrases, text):
    text = censor_list_of_phrases(negative_words + proprietary_terms, text)
    
    split_text = text.split(" ")
    
    # split elements of split_text at new lines - \n\n
    double_split_text = split_text
    for index_in_split_text in range(len(split_text)):
        double_split_text[index_in_split_text] = \
        double_split_text[index_in_split_text].split("\n\n")
    
    # censor previous and post words
    index1_in_double_split_text = 0
    index2_in_double_split_text = 0
    while index1_in_double_split_text < len(double_split_text):
        while index1_in_double_split_text < len(double_split_text) and\
        index2_in_double_split_text < len(double_split_text\
                                          [index1_in_double_split_text]):
            
            #check to see if current word is already censored
            if double_split_text[index1_in_double_split_text]\
            [index2_in_double_split_text].\
            find(censor_symbol) > -1:
                # current word is already censroed and need to censor previous
                # and following words
                
                #censor previous word
                if index2_in_double_split_text > 0:
                    #previous word is in same list element
                    double_split_text[index1_in_double_split_text]\
                    [index2_in_double_split_text - 1] = \
                    censor_letters_in_string(double_split_text\
                                             [index1_in_double_split_text]\
                                             [index2_in_double_split_text - 1])
                    
                elif index1_in_double_split_text > 0:
                    # previous word is in a different list element and
                    # current word is not first word of text
                    double_split_text[index1_in_double_split_text - 1]\
                    [len(double_split_text[index1_in_double_split_text - 1])\
                     - 1] = \
                    censor_letters_in_string(double_split_text\
                                             [index1_in_double_split_text - 1]\
                                             [len(double_split_text\
                                                  [index1_in_double_split_text\
                                                   - 1]) - 1])
                    
                # censor following word
                if index2_in_double_split_text <\
                len(double_split_text[index1_in_double_split_text]) - 1:
                    # following word is in same list element
                    
                    # check to see if following word is already censored
                    if double_split_text[index1_in_double_split_text]\
                    [index2_in_double_split_text + 1].find(censor_symbol) > - 1:
                    #following word is already censored
                    
                        #update indices to next word in same element of list
                        index2_in_double_split_text += 1
                    
                    else: #following word needs to be censored
                        double_split_text[index1_in_double_split_text]\
                        [index2_in_double_split_text + 1] =\
                        censor_letters_in_string(double_split_text\
                                                 [index1_in_double_split_text]\
                                                 [index2_in_double_split_text + 1])
                    
                        #update indices
                        if index2_in_double_split_text + 1 <\
                        len(double_split_text[index1_in_double_split_text]) - 1:
                            # stay in same list element
                            index2_in_double_split_text += 2
                            
                        else:
                            # go to next list element
                            index1_in_double_split_text += 1
                            index2_in_double_split_text = 0
                    
                elif not(index1_in_double_split_text ==\
                         len(double_split_text) - 1 and\
                         index1_in_double_split_text == len(double_split_text\
                         [index1_in_double_split_text]) - 1):
                    # following word is in next list element and
                    # current word is not last word of text
                    
                    # check to see if following word is already censored
                    if double_split_text[index1_in_double_split_text + 1]\
                    [0].find(censor_symbol) > - 1:
                        #following word is alread censored
                        
                        #update indices to first word of next list element
                        index1_in_double_split_text += 1
                        index2_in_double_split_text = 0
                    
                    else:#following word is not censored
                        
                        #censor following word
                        double_split_text[index1_in_double_split_text + 1][0] =\
                        censor_letters_in_string(double_split_text\
                                                 [index1_in_double_split_text + 1]\
                                                 [0])
                        
                        #update indices
                        if len(double_split_text[index1_in_double_split_text + 1])\
                        == 1:
                            # need to skip a list element
                            index1_in_double_split_text += 2
                            index2_in_double_split_text = 0
                        else:
                            # need to skip list element and one entry of element
                            index1_in_double_split_text += 1
                            index2_in_double_split_text += 1
                        
            
            else: # current word is not censored and need to go to next word 
            
                if index2_in_double_split_text ==\
                len(double_split_text[index1_in_double_split_text]) - 1:
                    # need to move to next list element
                    
                    index1_in_double_split_text += 1
                    index2_in_double_split_text = 0
                    break
                
                else: # stay in same list element
    
                    index2_in_double_split_text += 1
    
    
    # join text back together
    for index_in_split_text in range(len(split_text)):
        split_text[index_in_split_text] = "\n\n".join(double_split_text\
                  [index_in_split_text])
        
    text = " ".join(split_text)

    return text
            
new_email_four_str =\
censor_many_words(negative_words + proprietary_terms, email_four)
email_four_censored = open("email_four_censored.txt", "w").write(new_email_four_str)        
            
            
        
    
    



        
    



