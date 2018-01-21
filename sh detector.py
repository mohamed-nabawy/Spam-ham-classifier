import os
import numpy as np
import operator
# def intTryParse(value):
# 	try:
#    		value = int(value)
#     	return True
# 	except ValueError:
#     	return False

file1 = open(r'Directory to train data' , 'r')# r is the defaullt access mode

# Get priors
# spam_prior =0
# ham_prior=0
# for line in file.readlines():
# 	line =line.split() 
# 	spam_or_ham = line[1]
	
# 	if spam_or_ham=='spam':
# 		spam_prior+=1
# 	else:
# 		ham_prior+=1
# print(spam_prior , ham_prior)

#Data structures , Inital Values from train dataset
# double division

spam_prior=5163.0
ham_prior=3837.0
temp = spam_prior+ham_prior
spam_prior=spam_prior/temp
ham_prior=ham_prior/temp

print( spam_prior ,ham_prior )
total_words_no_spam =0.0
total_words_no_ham =0.0

spam_Dic={}# has each word with its occurrences in spam docs
ham_Dic={}#has each word with its occurrences in ham docs


#			Training


for line in file1.readlines():
	line =line.split(' ') 
	spam_or_ham = line[1]
	line = line[2:]

	if spam_or_ham=='spam':

		for x in range(0 ,len(line)):
			if x % 2 == 0:
				if line[x] in spam_Dic :		#check if key is in this dictionary
					spam_Dic[line[x]]+= int(line[x+1])
				else:	
					spam_Dic[line[x]]= int(line[x+1])

				total_words_no_spam += int(line[x+1])
				
	elif spam_or_ham=='ham':
		for y in range(0 ,len(line)):
			if y % 2 == 0:
				if line[y] in ham_Dic: 
					ham_Dic[line[y]]+= int(line[y+1])
				else:	
					ham_Dic[line[y]]= int(line[y+1])

				total_words_no_ham += int(line[y+1])	
	
			



file1.close()


#print (ham_Dic)

#	test: take that doc >> get each word occurences from train docs divided by total spam docs words no ,so for ham >> mutiply by priors >> calssify by the largest value 

# thl only info i get from test is that word x is in it , ignoring its occurence in test no.

keys_ham = set (ham_Dic.keys())
keys_spam =set(spam_Dic.keys())
#print (keys_spam)

intersection = keys_ham or keys_spam #intersection &

all_train={}

for x in intersection :
	all_train[x]=0

all_test={}

Vocabulary = float(len(intersection)) # all words no in ham and spam 

#														 Testing



file = open(r'Directory to test data' , 'r')# r is the defaullt access mode

total_conditional_P_spam=1.0
total_conditional_P_ham=1.0


hits=0.0
misses=0.0

spam_c=0
ham_c=0

for line in file.readlines():  #test document
	line =line.split(' ')
	spam_or_ham = line[1]
	line = line[2:]

	for x in range(0 ,len(line),2):	
	
		if line[x] in spam_Dic:
			total_conditional_P_spam *= ((spam_Dic[line[x]]+1)/float(total_words_no_spam+Vocabulary))
	
		else:
		 	total_conditional_P_spam *= 1/ float(total_words_no_spam+Vocabulary)

	for y in range(0 ,len(line),2):
		#if line[y] in ham_Dic:
		total_conditional_P_ham *= ((ham_Dic[line[y]]+1)/float(total_words_no_ham+Vocabulary))

		# else: 
		# 	total_conditional_P_ham *= 1/float(total_words_no_ham+Vocabulary)


	P_spam_doc= total_conditional_P_spam*spam_prior
	P_ham_doc= total_conditional_P_ham*ham_prior


	if P_spam_doc > P_ham_doc and spam_or_ham == 'spam':
		hits +=1
		spam_c+=1
	elif P_spam_doc < P_ham_doc and spam_or_ham == 'ham':
		hits +=1
		ham_c+=1
	# elif P_spam_doc == P_ham_doc and spam_or_ham == 'spam':
	#  	hits +=1
	else:
		misses+=1
	
	total_conditional_P_spam =1.0
	total_conditional_P_ham=1.0



#key, value = max(spam_Dic.iteritems(), key=lambda x:x[1])

#print(l)

print (hits*100/(hits+misses))
#print("spam:  %s , ham : %s" )%(spam_c , ham_c)
# dictlist=[(v,k) for k,v in spam_Dic.items()]
# dictlist2 = [(v,k) for k,v in ham_Dic.items()]

# dictlist.sort()
# dictlist2.sort()

#print(dictlist)
#print(dictlist2)

file.close()

