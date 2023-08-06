from .TestProperties import TestProperty
from .TestCaseGeneration import TestCaseGenerator
from .TestExecutionEngine import TestExecutor
from math import sqrt, acos, asin, sin, degrees, degrees, isclose
from scipy import stats
import numpy as np

class StatAnalyser:

    #use 2-sample t-test
    #null hypothesis is that the two states are equal
    def testAssertEqual(self,
                        p_value,
                        data):
        testResults = []
        for testIndex in range(len(data)):
            if np.array_equal(data[testIndex][0], data[testIndex][1]):
                testResults.append(True)
                continue

            t, stat_p = stats.ttest_ind(data[testIndex][0], data[testIndex][1])
            testResults.append(p_value <= stat_p)

        return testResults


    #use chi-square test for independence
    #null hypothesis is that they are not entangled
    def testAssertEntangled(self,
                            p_value,
                            data):
        #print(testResults)
        testResults = []
        for testIndex in range(len(data)):
            print(data[testIndex])
            #TODO currently doesn't work properly?
            t, stat_p, x, y = stats.contingency.chi2_contingency(data[testIndex])
            print(stat_p)
            #trialResults = []
            #for trialData in testData:
            #    nb0sQubit0 = trialData[0][0]
            #    nb1sQubit0 = trialData[0][1]

            #    nb0sQubit1 = trialData[1][0]
            #    nb1sQubit1 = trialData[1][1]

            #    totalQubit0 = nb0sQubit0 + nb1sQubit0
            #    totalQubit1 = nb0sQubit1 + nb1sQubit1

            #    total0s = nb0sQubit0 + nb0sQubit1
            #    total1s = nb1sQubit0 + nb1sQubit1

            #    grandTotal = total0s + total1s

            #    expected0sQubit0 = totalQubit0 * total0s / grandTotal #Assuming no dependence
            #    expected1sQubit0 = totalQubit0 * total1s / grandTotal #Assuming no dependence
            #    expected0sQubit1 = totalQubit1 * total0s / grandTotal #Assuming no dependence
            #    expected1sQubit1 = totalQubit1 * total1s / grandTotal #Assuming no dependence

            #    diffExpectedActual0sQubit0 = nb0sQubit0 - expected0sQubit0
            #    diffExpectedActual1sQubit0 = nb1sQubit0 - expected1sQubit0
            #    diffExpectedActual0sQubit1 = nb0sQubit0 - expected0sQubit1
            #    diffExpectedActual1sQubit1 = nb1sQubit1 - expected1sQubit1

            #    dividedSquaredDiff0_0 = (diffExpectedActual0sQubit0 ** 2) / expected0sQubit0
            #    dividedSquaredDiff1_0 = (diffExpectedActual1sQubit0 ** 2) / expected1sQubit0
            #    dividedSquaredDiff0_1 = (diffExpectedActual0sQubit1 ** 2) / expected0sQubit1
            #    dividedSquaredDiff1_1 = (diffExpectedActual1sQubit1 ** 2) / expected1sQubit1

            #    testStat = dividedSquaredDiff0_0 + dividedSquaredDiff1_0 + dividedSquaredDiff0_1 + dividedSquaredDiff1_1

            #    dof = 1 #degree of freedom is (rows - 1) * (cols - 1) or 1 * 1 or 1

            #    criticalT = stats.t.ppf(q=p_value, df=dof)

            #    trialResults.append(abs(testStat) <= abs(criticalT))

            #finalTestResults.append({"Passed trials": trialResults.count(True), "Failed trials": trialResults.count(False)})

        return testResults



    #Using one-sample t-test
    #The Null hypothesis is that the sample was taken with the same probability as the argument
    #TestResults is a tuple of tuple of bool
    def testAssertProbability(self,
                            p_value: float,
                            expectedProbas,
                            data):

        testResults = []

        for trialIndex in range(len(data)):
            if np.all(data[trialIndex] == data[trialIndex][0]):
                testResults.append(isclose(data[trialIndex][0], expectedProbas[trialIndex], abs_tol=0.01))
                continue

            t, stat_p = stats.ttest_1samp(data[trialIndex], expectedProbas[trialIndex])

            testResults.append(p_value <= stat_p)

            #print(stat_p)

        return testResults



    def testAssertTransformed(self, thetaMin, thetaMax, phiMin, phiMax, testStatevectors):

        results = []
        for statevector in testStatevectors:

            realPart0 = float(statevector[0].real)

            thetaRad = acos(realPart0) * 2

            #print(f"thata degrees from statevector: {degrees(thetaRad)}")

            if sin(thetaRad / 2) == 0:
                raise Exception("Division by 0")

            phiRad1 = acos(float(statevector[1].real) / sin(thetaRad / 2))
            #phiRad2 = asin(float(testStatevector[1].imag) / sin(thetaRad / 2))

            #print(f"values from statevectors: {degrees(thetaRad)}, {degrees(phiRad1)}")

            results.append(degrees(thetaRad) >= thetaMin - 0.001 and degrees(thetaRad) <= thetaMax + 0.001 and \
                           degrees(phiRad1) >= phiMin - 0.001 and degrees(phiRad1) <= phiMax + 0.001)

        return results
