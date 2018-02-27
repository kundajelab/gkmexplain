#!/usr/bin/python
from __future__ import division, absolute_import, print_function
import math
import sys
import os
from . import computeLogs_function as cl_f
import math


def monteCarlo(actionToRepeat, timesToRepeat):
    resultsToReturn = [];
    i = 0;
    while (i < timesToRepeat):
        i += 1;
        resultsToReturn.append(actionToRepeat());
    return resultsToReturn;


def mean(arr):
    total = 0;
    for elem in arr:
        total += elem;
    return float(total)/len(arr);


def variance(arr):
    theMean = mean(arr);
    tot = 0;
    for elem in arr:
        tot += (elem-theMean)**2;
    return float(tot)/len(arr);


def sdev(arr):
    return variance(arr)**(0.5);


class TestResult:
    def __init__(self,pval,testType,testStatistic=None,testContext=None):
        self.pval = pval;
        self.testType = testType;
        self.testStatistic=testStatistic;
        self.testContext=testContext;
    def __str__(self):
        toReturn = "pval: "+str(self.pval)+", test: "+self.testType;
        toReturn = self.appendTestInfoToToReturn(toReturn);
        return toReturn;
    def tabDelimString(self):
        toReturn = str(self.pval)+"\t"+"test: "+str(self.testType);
        toReturn = self.appendTestInfoToToReturn(toReturn,tabDelim=True);
        return toReturn;
    @staticmethod
    def tabTitle():
        return "pval\ttestInfo\ttestStatistic\ttestContext";
    def appendTestInfoToToReturn(self,toReturn,tabDelim=False):
        if (tabDelim):
            toReturn += "\t"+(str(self.testStatistic) if self.testStatistic is not None else "");
            toReturn += "\t"+(str(self.testContext) if self.testContext is not None else "");
        else:
            if (self.testStatistic is not None):
                toReturn += ", test statistic: "+str(self.testStatistic);
            if (self.testContext is not None):
                toReturn += ",test context: "+str(self.testContext);
        return toReturn;        


#flips between Z-test and fisher's exact test based on supplied data
def proportionTest(total,special,picked,specialPicked):
    if (special == total or picked == total):
        return TestResult(1,"Common sense");
    if (special == 0):
        return TestResult(1,"Common sense");    

    if (total < len(cl_f.LOG_FACTORIAL_ARRAY)):
        method=hypGeo_cumEqualOrMoreOverlap;
    elif ((specialPicked > 5) and (picked-specialPicked > 5) and (special-specialPicked > 5) and ((total-picked)-(special-specialPicked) > 5)):
        method=twoProportionZtest;
    else:
        method=edgeCase
    return method(total,special,picked,specialPicked);


def edgeCase(total,special,picked,specialPicked):
    hypGeoValueCheck(total,special,picked,specialPicked);
    if (picked == total and specialPicked == special):
        return TestResult(1.0,"Common sense");
    if (specialPicked == 0):
        return TestResult(1.0,"Common sense");
    return twoProportionZtest(total,special,picked,specialPicked);
    #if (picked < cl_f.LOG_FACTORIAL_THRESHOLD):
    #    #do a desperate binomial estimate
    #    return binomialProbability(specialPicked,picked,float(special)/total);
    #raise Exception("No supported test for edge case where "
    #    +"total="+str(total)+", special="+str(special)
    #    +", picked="+str(picked)+" and specialPicked="+str(specialPicked));


def binomialProbability(trials,successes,pSuccess):
    combos = combination(trials,successes);
    return TestResult(combos*(pSuccess**(successes)), "binomial probability");


def multinomialProbability(successesArr,pSuccessesArr,bruteCompute=False):
    assert len(successesArr)==len(pSuccessesArr);
    totalTrials = sum(successesArr);
    if (totalTrials < len(cl_f.LOG_ARRAY)):
        logProb = 0;
        for i in range(0,len(successesArr)):
            logProb += successesArr[i]*math.log(pSuccessesArr[i]);
        #find the multinomial coefficient
        logProb += logMultinomialCombination(successesArr,total=totalTrials,bruteCompute=bruteCompute);
        return TestResult(math.exp(logProb), "multinomial probability");
    else:
        return normalApproxMultinomialProbability(successesArr,pSuccessesArr,totalTrials)


def normalApproxMultinomialProbability(successesArr,pSuccessesArr,totalTrials=None):
    label = "normal approx. multinomial dist";
    for successNum in successesArr:
        if (successNum < 5):
            label += " - inappropriate";
    if (totalTrials is None):
        totalTrails = sum(successesArr);
    meanVector = []
    covarianceMatrix = []
    for i in range(0,len(successesArr)):
        meanVector.append(totalTrials*pSuccessesArr[i]);
        covarianceLine = []
        for j in range(0,len(successesArr)):
            if (j==i):
                covarianceLine.append(totalTrials*pSuccessesArr[i]*(1-pSuccessesArr[i]));
            else:
                covarianceLine.append(-1*totalTrials*pSuccessesArr[i]*pSuccessesArr[j]);
        covarianceMatrix.append(covarianceLine);
    return TestResult(multivariate_normal.pdf(successesArr,meanVector,covarianceMatrix), label);


#for when fisher's exact test doesn't scale
def twoProportionZtest(total,special,picked,specialPicked):
    from scipy.stats import norm;
    hypGeoValueCheck(total,special,picked,specialPicked);
    enOne = float(picked);
    enTwo = float(total-picked);
    pOne = float(specialPicked)/enOne;
    pTwo = float(special-specialPicked)/enTwo;
    pMean = float(special)/total;
    z = float(pOne-pTwo)/((pMean*(1-pMean)*(1/enOne + 1/enTwo))**(0.5))
    if ((specialPicked > 5) and (picked-specialPicked > 5) and (special-specialPicked > 5) and ((total-picked)-(special-specialPicked) > 5)):
        appropriate = True;
    else:
        appropriate = False;
    return TestResult(1-norm.cdf(z),"Two-proportion z-test - "+("appropriate" if appropriate else "inappropriate"), testStatistic=z);


def hypGeo_cumEqualOrMoreOverlap(total,special,picked,specialPicked,bruteCompute=False):
    hypGeoValueCheck(total,special,picked,specialPicked);
    minValSpecialPicked = max(0,(special+picked)-total);
    maxValSpecialPicked = min(special,picked);
    cumProb = 0;
    if (maxValSpecialPicked-specialPicked <= specialPicked-minValSpecialPicked):
        for i in range(specialPicked,maxValSpecialPicked+1):
            cumProb = cumProb + hypGeo_nonCum(total,special,picked,i,bruteCompute);
        toReturn = cumProb;
    else:
        for i in range(minValSpecialPicked,specialPicked): #range goes up till upperval - 1
            cumProb = cumProb + hypGeo_nonCum(total,special,picked,i,bruteCompute);
        toReturn = 1-cumProb;
    return TestResult(toReturn, "hypergeometric test");


def hypGeo_nonCum(total,special,picked,specialPicked,bruteCompute=False):
    hypGeoValueCheck(total,special,picked,specialPicked);
    logCondition = (total > cl_f.LOG_FACTORIAL_THRESHOLD);
    comboFunction = logCombination if logCondition else combination;
    specialChooseSpecialPicked = comboFunction(special,specialPicked,bruteCompute);
    unspecialChooseUnspecialPicked = comboFunction(total-special, picked-specialPicked,bruteCompute);
    totalChoosePicked = comboFunction(total,picked,bruteCompute);
    if (logCondition):
        return math.exp((specialChooseSpecialPicked - totalChoosePicked)+unspecialChooseUnspecialPicked);
    else:
        return (float(specialChooseSpecialPicked)/totalChoosePicked)*unspecialChooseUnspecialPicked;


def hypGeoValueCheck(total,special,picked,specialPicked):
    if (special > total):
        raise ValueError(str(special)+" should not be > "+str(total));
    if (picked > total):
        raise ValueError(str(picked)+" should not be > "+str(total));
    if ((special + picked - specialPicked) > total):
        raise ValueError(str(special)+" + "+str(picked)+" - "+str(specialPicked)+" should not be > "+str(total)+".");
    if (specialPicked > special):
        raise ValueError(str(specialPicked)+" should not be > "+str(special));
    if (specialPicked > picked):
        raise ValueError(str(specialPicked)+" should not be > "+str(picked));
    

def multinomialCombination(items,total=None,bruteCompute=False):
    if (total is None):
        total  = sum(items);
    if (a <= cl_f.LOG_FACTORIAL_THRESHOLD):
        factorialProduct = 1;
        for item in items:
            factorialProduct *= factorial(item);
        return factorial(total)/factorialProduct;
    else:
        return math.exp(logMultinomialCombination(items,total,bruteCompute));


def logMultinomialCombination(items,total=None,bruteCompute=False):
    if (total is None):
        total = sum(items);
    if (a <= cl_f.LOG_FACTORIAL_THRESHOLD):
        return math.log(multinomialCombination(items,total,bruteCompute));
    else:
        factorialSum = 0;
        for item in items:
            factorialSum += logFactorial(item,bruteCompute);
        return logFactorial(total,bruteCompute) - factorialSum;        


def combination(a,b,bruteCompute=False):
    if (b > a):
        bGreaterThanAError(a,b);
    if (a <= cl_f.LOG_FACTORIAL_THRESHOLD):
        return factorial(a)/(factorial(b)*factorial(a-b)); #shouldn't need floats cos integers should divide exactly!
    else:
        return math.exp(logCombination(a,b,bruteCompute));


def logCombination(a,b,bruteCompute=False):
    if (b > a):
        bGreaterThanAError(a,b);
    if (a <= cl_f.LOG_FACTORIAL_THRESHOLD):
        return math.log(combination(a,b));
    else:
        return logFactorial(a,bruteCompute=bruteCompute)-(logFactorial(b,bruteCompute=bruteCompute)+logFactorial(a-b,bruteCompute=bruteCompute));


def bGreaterThanAError(a,b):
    raise ValueError(str(b)+", representing elements picked, should not be larger than "+str(a)+" representing superset to pick from");
    

def factorial(num):
    if (num <= cl_f.LOG_FACTORIAL_THRESHOLD):
        #compute straight up
        toReturn = math.factorial(num);
        if (toReturn < 0):
            raise Exception("Darn, got "+toReturn+" as factorial for "+num+". Probably got some integer overflow. Check value of LOG_FACTORIAL_THRESHOLD?");
    else:
        raise Exception("Wait...are you sure you should be calling factorial and not logFactorial on a number as large as "+str(LOG_FACTORIAL_THRESHOLD)+"?");
    return toReturn


bruteComputationCache = {};


def logFactorial(num,logFactArr=cl_f.LOG_FACTORIAL_ARRAY,bruteCompute=False):
    if (num >= len(logFactArr)):
        if (bruteCompute==False):
            raise Exception("Ooops...can only handle factorials up till "+str(len(logFactArr))+". To handle higher factorials like "+str(num)+", need to generate a longer logFactorial file or set bruteCompute to true");
        else:
            if (num not in bruteComputationCache):
                print("Warning: brute computing logFactorial of "+str(num)+".");
                val = cl_f.computeLogFactorial(num);    
                bruteComputationCache[num] = val;
                return val;
            else:
                return bruteComputationCache[num];
    return logFactArr[num];
