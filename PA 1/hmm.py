#!/usr/bin/python

# Author: Arun George
# Class: UConn, CSE 3800, Fall 2017
# Instructor: Yufeng Wu
# Description: Programming Assignment 1

import time
import numpy as np
import random

def main():
	lengths  = [300, 3000, 30000, 300000] 
	for lIndex, lVal in enumerate(lengths):	#test for each sequence length
		startTime = time.time()
		vit_totalDifferences	= 0
		post_totalDifferences	= 0
		totalSeqLength			= 10 * lVal

		logFile = 'log'+str(lVal)+'.txt'
		with open(logFile, 'w') as lf :
			pass	# flush the file everytime we run the tests
		lf.close()

		mleTot = np.zeros((2,6))

		for i in range(0, 10):				# run ten tests for each length and report the average
			print("running trial {}".format(i))
			states 				= ['F', 'L']
			symbols 			= ['1', '2', '3', '4', '5', '6']
			statePath			= ""
			symbolPath			= ""
			startMatrix 		= np.array([0.5, 0.5])	
			transitionMatrix 	= np.array([[0.95, 0.05], 
										 	[0.10, 0.90]])
			emissionMatrix		= np.array([[1/6, 1/6, 1/6, 1/6, 1/6, 1/6], 
											[1/10, 1/10, 1/10, 1/10, 1/10, 1/2]])
			
			curState = str(np.random.choice(states, p = startMatrix)) # Pick the die to initially start with, Fair or Loaded

			for sz in range(lVal):
				if curState == 'F' :
					curState = str(np.random.choice(states, p = list(transitionMatrix[0])))
				elif curState == 'L' :
					curState = str(np.random.choice(states, p = list(transitionMatrix[1])))
				statePath 	+= curState
				if curState == 'F' :
					symbol 	= str(np.random.choice(symbols, p = list(emissionMatrix[0])))
				elif curState == 'L' :
					symbol 	= str(np.random.choice(symbols, p = list(emissionMatrix[1])))
				symbolPath 	+= symbol

			v 		= viterbi(symbolPath, startMatrix, transitionMatrix, emissionMatrix)
			vPath 	= convertToStr(v)

			fwd 	= forward(symbolPath, startMatrix, transitionMatrix, emissionMatrix)
			f 		= np.argmax(fwd, axis=1)
			fPath 	= convertToStr(f)

			bwd 	= backward(symbolPath, startMatrix, transitionMatrix, emissionMatrix)
			b 		= np.argmax(bwd, axis=1)
			bPath 	= convertToStr(b)

			post 	= posterior(fwd, bwd)
			p 		= np.argmax(post, axis=1)
			pPath 	= convertToStr(p)

			diffViterbi 	= sum(1 for a, b in zip(statePath, vPath) if a != b)
			diffPosterrior	= sum(1 for a, b in zip(statePath, pPath) if a != b)

			mleMat = MLE(statePath, symbolPath)
			mleTot = np.add(mleTot, mleMat)

			# the following print statements were used for testing
			# print("Trial number {} for sequence of length {}".format(i+1, lVal))
			# print("Rolls: \t\t{}".format(symbolPath))
			# print("Die:   \t\t{}".format(statePath))
			# print("Viterbi: \t{}".format(vPath))	
			# print("Forward: \t{}".format(fPath))
			# print("Backward:\t{}".format(bPath))
			# print("Posterrior: \t{}".format(pPath))
			# print("Num of differences between Actual and Viterbi:\t\t{}".format(diffViterbi))
			# print("Num of differences between Actual and Posterrior:\t{}".format(diffPosterrior))
			# print("MLE for the Fair die:\t{}".format(mleMat[0]))
			# print("MLE for the Loaded die:\t{}".format(mleMat[1]))

			with open(logFile, 'a+') as lf :	# append to the log file test data 10 times for each length
				lf.write("\nTrial number {} for sequence of length {}".format(i+1, lVal))
				lf.write("\nDie:   \t\t{}".format(statePath))
				lf.write("\nViterbi: \t{}".format(vPath))
				lf.write("\n\t\t\t Num of differences: {}".format(diffViterbi))
				lf.write("\nPosterrior: {}".format(pPath))
				lf.write("\n\t\t\t Num of differences: {}".format(diffPosterrior))
				# lf.write("\nMLE for the Fair die:\t{}".format(mleMat[0]))
				# lf.write("\nMLE for the Loaded die:\t{}".format(mleMat[1]))
				lf.write("\n")
			lf.close()
			vit_totalDifferences	+= diffViterbi
			post_totalDifferences	+= diffPosterrior

		mleFin = np.divide(mleTot, 10)

		with open(logFile, 'a+') as lf :
			lf.write("\nSummary for length {}".format(lVal))
			lf.write("\nPercentage viterbi was wrong: {}".format(vit_totalDifferences/totalSeqLength))
			lf.write("\nPercentage posterrior was wrong: {}".format(post_totalDifferences/totalSeqLength))
			lf.write("\nMLE for the Fair die:\t{}".format(mleFin[0]))
			lf.write("\nMLE for the Loaded die:\t{}".format(mleFin[1]))
		lf.close()
		endTime = time.time()
		print("Simulation for length {}  done and can find test data in {}. \nSimulation took {}s".format(lVal, logFile, endTime-startTime))

def viterbi(seq, initMat, transitionMat, emissionMat):
	numStates  = emissionMat.shape[0]
	numSymbols = emissionMat.shape[1]
	dTable  = np.zeros((len(seq), numStates))					
	pTable 	= np.zeros((len(seq), numStates), dtype = np.int)	
	#initialization
	for i in range(numStates):
	    dTable[0,i]  = initMat[i] * emissionMat[i, int(seq[0])-1]
	    pTable[0,i] 	= 0
	#recursion
	for t in range(1,len(seq)):
	    for j in range(numStates):
	        m = np.zeros(numStates)
	        for i in range(numStates):
	            m[i] = dTable[t-1, i] * transitionMat[i,j]
	        pTable[t,j] = m.argmax()
	        dTable[t,j]  = m.max() * emissionMat[j, int(seq[t])-1]
	#termination
	m = np.zeros(numStates)
	for i in range(numStates):
	    m[i] = dTable[len(seq)-1, i]
	#traceback
	V = np.zeros(len(seq), dtype=np.int)
	V[len(seq)-1] = m.argmax()
	for t in reversed(range(len(seq)-1)):
		V[t] = pTable[t+1, V[t+1]]
	return V

def forward(seq, initMat, transitionMat, emissionMat):
	numStates  = emissionMat.shape[0]
	numSymbols = emissionMat.shape[1]
	fwd = np.zeros((len(seq), numStates))
	#initiazliation
	for i in range(numStates):
	    fwd[0, i] = initMat[i] * emissionMat[i, int(seq[0])-1]
	#induction
	for t in range(len(seq)-1):
	    for j in range(numStates):
	        s = 0
	        for i in range(numStates):
	            s += fwd[t,i] * transitionMat[i,j]
	        fwd[t+1,j] = s * emissionMat[j, int(seq[t+1])-1]
	return fwd

def backward(seq, initMat, transitionMat, emissionMat):
	numStates  = emissionMat.shape[0]
	numSymbols = emissionMat.shape[1]
	bwd = np.zeros((len(seq), numStates))
	#initialization
	for i in range(numStates):
	    bwd[len(seq)-1, i] = 1
	#induction:
	for t in reversed(range(len(seq)-1)):
	    for i in range(numStates):
	        s = 0
	        for j in range(numStates):
	            s += transitionMat[i,j] * emissionMat[j, int(seq[t+1])-1] * bwd[t+1, j]            
	        bwd[t,i] = s
	return bwd

def posterior(fwd, bwd):
	numStates	= fwd.shape[1]
	numSymbols	= fwd.shape[0]
	post = np.zeros((numSymbols, numStates))
	fp = fwd[-1].sum()
	for t in range(numSymbols):
		for i in range(numStates):
			post[t,i] = (fwd[t,i] * bwd[t,i]) / fp
	return post

def MLE(statePath, symbolPath):
	fTotal = statePath.count('F')
	lTotal = statePath.count('L')
	FF, FL, LL, LF = 0, 0, 0, 0

	# used to test
	# for i in range(len(statePath)-1):
	# 	if statePath[i] == str(statePath[i+1]) == 'F':
	# 		FF += 1
	# 	elif statePath[i] == statePath[i+1] == 'L':
	# 		LL += 1
	# 	elif statePath[i] == 'F' and statePath[i+1] == 'L':
	# 		FL += 1
	# 	elif statePath[i] == 'L' and statePath[i+1] == 'F':
	# 		LF += 1

	# mleFF = FF / fTotal ; mleFL = FL / fTotal
	# mleLL = LL / lTotal ; mleLF = LF / lTotal

	F1, F2, F3, F4, F5, F6 = 0, 0, 0, 0, 0, 0
	L1, L2, L3, L4, L5, L6 = 0, 0, 0, 0, 0, 0

	for i in range(len(statePath)):
		if statePath[i] == 'F' and symbolPath[i] == '1':
			F1 += 1
		elif statePath[i] == 'F' and symbolPath[i] == '2':
			F2 += 1
		elif statePath[i] == 'F' and symbolPath[i] == '3':
			F3 += 1
		elif statePath[i] == 'F' and symbolPath[i] == '4':
			F4 += 1
		elif statePath[i] == 'F' and symbolPath[i] == '5':
			F5 += 1
		elif statePath[i] == 'F' and symbolPath[i] == '6':
			F6 += 1
		if statePath[i] == 'L' and symbolPath[i] == '1':
			L1 += 1
		elif statePath[i] == 'L' and symbolPath[i] == '2':
			L2 += 1
		elif statePath[i] == 'L' and symbolPath[i] == '3':
			L3 += 1
		elif statePath[i] == 'L' and symbolPath[i] == '4':
			L4 += 1
		elif statePath[i] == 'L' and symbolPath[i] == '5':
			L5 += 1
		elif statePath[i] == 'L' and symbolPath[i] == '6':
			L6 += 1

	mleF1 = F1 / fTotal ; mleF2 = F2 / fTotal ; mleF3 = F3 / fTotal ; mleF4 = F4 / fTotal ; mleF5 = F5 / fTotal ; mleF6 = F6 / fTotal
	mleL1 = L1 / lTotal ; mleL2 = L2 / lTotal ;	mleL3 = L3 / lTotal ; mleL4 = L4 / lTotal ;	mleL5 = L5 / lTotal ; mleL6 = L6 / lTotal

	mleMatrix	= np.array([[mleF1, mleF2, mleF3, mleF4, mleF5, mleF6], 
							[mleL1, mleL2, mleL3, mleL4, mleL5, mleL6]])

	return mleMatrix

def convertToStr(mat):
	mPath = ''.join(map(str, mat))
	for c in mPath:
		if c == '0':
			mPath = mPath.replace(c,'F')
		if c == '1':
			mPath = mPath.replace(c,'L')
	return mPath

if __name__ == '__main__':
	main()