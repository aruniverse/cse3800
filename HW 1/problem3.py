#!/usr/bin/python

# Author: Arun George
# Class: UConn, CSE 3800, Fall 2017
# Instructor: Yufeng Wu
# Description: HW 1, Problem 3

import random

def main():
	n = int(input("Enter initial amount: "))
	N = int(input("Enter goal: "))
	strategy = input("Enter strategy: ('timid' or 'bold') ")
	probabilities = [ 0.45, 0.48, 0.5, 0.52, 0.55 ]
	with open('logFile.txt', 'w'):	#open the log file and delete its content
		pass
	for p in probabilities:
		success = 0
		for i in range(0, 100):
			if(strategy == 'timid'):
				val = timid(n, N, p)
			else:
				val = bold(n, N, p)
			if (val == N) :
				success+=1
		#print("Num success: ", success, strategy, p)
		s = "Strategy: " + strategy + " Probability: " + str(p) + " Num Success: " + str(success) + "\n"
		print(s)
		with open('logFile.txt', 'a') as logFile:
			logFile.write(s)

def timid(n, N, p):
	while(0<n and n<N) : 
		r = random.random()
		if(r<p) :
			n+=1
		else :
			n-=1
	return n

def bold(n, N, p):
	while(0<n and n<N) :
		if(2*n<=N):
			bet = n
		else:
			bet = N-n
		r = random.random()
		if(r<p) :
			n+=bet
		else :
			n-=bet
	return n

if __name__ == '__main__':
	main()