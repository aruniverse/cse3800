#!/usr/bin/python

# Author: Arun George
# Class: UConn, CSE 3800, Fall 2017
# Instructor: Yufeng Wu
# Description: HW 2, Problem 4

import time
import random
import numpy as np
import pandas as pd

def main() :
	type = input("Enter type ( 'basic' or 'random' ) : ")
	if(type == 'basic') :
		basic()
	elif(type == 'random') :
		randomize()
	else :
		main()

def basic() :
	s1 = input("Enter string s1: ")
	s2 = input("Enter string s2: ")
	score = LocalAlignment(s1, s2)
	#	score = SmithWaterman(s1, s2)
	print("The max score for s1:{} and s2:{} is {}".format(s1, s2, score))

def randomize() :
	dnaSeq = ['A', 'T', 'C', 'G']
	lengths = [10, 100, 1000, 10000]#, 100000]
	for l in range(len(lengths)) :
		s1 = "".join(random.choice(dnaSeq) for i in range(lengths[l]))
		s2 = "".join(random.choice(dnaSeq) for j in range(lengths[l]))
		print("String 1: {} \n".format(s1))
		print("String 2: {} \n".format(s2))
		score = SmithWaterman(s1, s2)
		print("The max score for s1:{} and s2:{} is {}".format(s1, s2, score))

#	Basic Local Alignment alg
#	v(i,0) = -i , v(0,j) = -j, for all i<m, and j<n
#	v(i,j) = argmax { v(i-1,j)-1 , v(i,j-1)-1, v(i-1,j-1)+-1 }
def LocalAlignment(s1, s2) :
	startTime = time.time()
	s1 = " " + s1 ;	s2 = " " + s2	
	l1 = len(s1) ; l2 = len(s2)
	m = np.zeros(shape=(l1, l2), dtype=int)
	rows = m.shape[0] ;	cols = m.shape[1]
	for i in range(0, rows) :
		m[i, 0] = -i
	for j in range(0, cols) :
		m[0, j] = -j
	for i in range(1, rows) :
		for j in range(1, cols) :
			L = m[i-1, j] - 1
			U = m[i, j-1] - 1
			D = m[i-1, j-1] + 1 if s1[i] == s2[j] else m[i-1, j-1] - 1	# python's way of doing ternary conditionals, could've called Score()
			m[i, j] = max(L, U, D, 0)
			m[i, j] = max(L, U, D)
	mat = pd.DataFrame(m, columns=list(s2), index=list(s1))
	output(mat)
	print(time.time() - startTime)
	return m[l1-1, l2-1]

#	Smith-Waterman alg
#	v(i,0) = 0 , v(0,j) = 0, for all i<m, and j<n
#	v(i,j) = argmax { v(i-1,j)-1 , v(i,j-1)-1, v(i-1,j-1)+-1 , 0}
def SmithWaterman(s1, s2) :
	startTime = time.time()
	s1 = " " + s1 ;	s2 = " " + s2	
	l1 = len(s1) ; l2 = len(s2)
	m = np.zeros(shape=(l1, l2),dtype=int)
	maxScore = 0
	rows = m.shape[0] ;	cols = m.shape[1]
	for i in range(1, rows) :
		for j in range(1, cols) :
			L = m[i-1, j] - 1
			U = m[i, j-1] - 1
			D = m[i-1, j-1] + 1 if s1[i] == s2[j] else m[i-1, j-1] - 1	# python's way of doing ternary conditionals, could've called Score()
			m[i, j] = max(L, U, D, 0)
			if (m[i, j] > maxScore) :
				maxScore = m[i, j]
	mat = pd.DataFrame(m, columns=list(s2), index=list(s1))
	output(mat)
	print(time.time() - startTime)
	return maxScore

def output(mat) :
	print(mat)
	rows = mat.shape[0] 
	cols = mat.shape[1]
	logFile = 'log'+str(rows-1)+'x'+str(cols-1)+'.txt'
	with open(logFile, 'w') as lf :
		pass
		mat.to_string(lf)

if __name__ == '__main__':
	main()