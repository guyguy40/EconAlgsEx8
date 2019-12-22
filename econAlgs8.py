import itertools, random

"""
this is a submission for question 1. Submittor info:
name - Guy Wolf
id - 212055966
"""

#each agent is an int from 0 to the number of agents-1. Each subset is a list of agents.

class CostStorage:
    def cost(self, subset):
        pass

class DictStorage(CostStorage):
    def __init__(self, sets):
        """sets = dict of all costs by the subset"""
        newSets = {}
        for key in sets.keys():
            newSets[tuple(sorted(key))] = sets[key]
        self.sets = newSets
        
    def cost(self, subset):
        return self.sets[tuple(sorted(subset))]

class MaxStorage(CostStorage):
    def __init__(self, costs):
        """sets = a list of all of the costs per agent, the total cost is the maximum of them"""
        self.costs = costs
        self.numAgents = len(costs)
        
    def cost(self, subset):
        return max([self.costs[i] for i in range(self.numAgents) if i in subset])

def permutationCosts(costs, perm):
    ret = []
    subset = []
    prevCost = 0
    for agent in perm:
        subset.append(agent)
        cost = costs.cost(subset)
        ret.append((agent, cost-prevCost))
        prevCost = cost
    return ret

def fullShapley(costs, numAgents):
    agentCosts = [0 for _ in range(numAgents)]
    agents = list(range(numAgents))
    permutations = itertools.permutations(agents)
    permNum = 0
    for permutation in permutations:
        permCosts = permutationCosts(costs, permutation)
        for cost in permCosts:
            agentCosts[cost[0]] += cost[1]
        permNum += 1

    return [totalCosts/permNum for totalCosts in agentCosts]
        

def approxShapley(costs, numAgents, permNum):
    agentCosts = [0 for _ in range(numAgents)]
    
    for _ in range(permNum):
        permutation = list(range(numAgents))
        random.shuffle(permutation)
        permCosts = permutationCosts(costs, permutation)
        for cost in permCosts:
            agentCosts[cost[0]] += cost[1]
    
    return [totalCosts/permNum for totalCosts in agentCosts]

def test(exampleName, costs, numAgents, testPerms, numTests):
    testSum = [0 for _ in range(numAgents)]
    testDiffSum = [0 for _ in range(numAgents)]
    trueRes = fullShapley(costs, numAgents)
    print("testing for " + exampleName)
    print("true results:")
    print(str(trueRes))

    for _ in range(numTests):
        testRes = approxShapley(costs, numAgents, testPerms)
        for i in range(len(testRes)):
            testSum[i] += testRes[i]
            testDiffSum[i] += abs(testRes[i]-trueRes[i])

    print("average result:")
    print(str([val / numTests for val in testSum]))

    print("average error:")
    print(str([val / numTests for val in testDiffSum]))

three = {}

three[(0,)] = 0
three[(1,)] = 0
three[(2,)] = 0

three[(0,1)] = 4
three[(1,2)] = 5
three[(0,2)] = 6

three[(0,1,2)] = 10

threeCosts = DictStorage(three)

test("three agents", threeCosts, 3, 6, 100)

runway = [(2**(i/5))+i for i in range(30)]
runwayCosts = MaxStorage(runway)

test("runway of 30", runwayCosts, 30, 100, 100)
