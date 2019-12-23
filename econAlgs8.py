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

    def trueCosts(self, numAgents):
        pass

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

class DictStorage(CostStorage):
    def __init__(self, sets):
        """sets = dict of all costs by the subset"""
        newSets = {}
        for key in sets.keys():
            newSets[tuple(sorted(key))] = sets[key]
        self.sets = newSets
        
    def cost(self, subset):
        return self.sets[tuple(sorted(subset))]

    def trueCosts(self, numAgents):
        agentCosts = [0 for _ in range(numAgents)]
        agents = list(range(numAgents))
        permutations = itertools.permutations(agents)
        permNum = 0
        for permutation in permutations:
            permCosts = permutationCosts(self, permutation)
            for cost in permCosts:
                agentCosts[cost[0]] += cost[1]
            permNum += 1

        return [totalCosts/permNum for totalCosts in agentCosts]

class MaxStorage(CostStorage):
    def __init__(self, costs):
        """sets = a list of all of the costs per agent, the total cost is the maximum of them"""
        self.costs = costs
        self.numAgents = len(costs)
        
    def cost(self, subset):
        return max([self.costs[i] for i in range(self.numAgents) if i in subset])

    def trueCosts(self, numAgents):
        ret = [self.costs[0]/numAgents for _ in range(numAgents)]
        for i in range(1, numAgents):
            trueCost = (self.costs[i]-self.costs[i-1])/(numAgents-i)
            for j in range(i, numAgents):
                ret[j] += trueCost
        return ret
        

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
    trueRes = costs.trueCosts(numAgents)
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

"""copy of already completed print:

testing for three agents
true results:
[3.3333333333333335, 2.8333333333333335, 3.8333333333333335]
average result:
[3.203333333333333, 2.9333333333333336, 3.8633333333333315]
average error:
[0.8433333333333336, 0.64, 0.9133333333333333]
testing for runway of 30
true results:
[0.03333333333333333, 0.07294362143667937, 0.11475824842867435, 0.15906227271524856, 0.20619244810301202, 0.2565484030393221, 0.31060659928907497, 0.3689378650087149, 0.4322295609848516, 0.5013138048021707, 0.5772036921429459, 0.6611401879317953, 0.754653422548653, 0.8596436944868892, 0.9784898345073517, 1.1141962007494188, 1.2705952607477244, 1.4526319104559455, 1.666771014280948, 1.9215961488859299, 2.2287152476121315, 2.6041789898290824, 3.070798101380802, 3.6621321716379525, 4.42982433185622, 5.458300726761026, 6.897887566737307, 9.053189495013141, 12.692527986813195, 20.904833909432405]
average result:
[0.03139999999999997, 0.07712748995739176, 0.11682191025513754, 0.15575837589004435, 0.2061589439843972, 0.26571037331849423, 0.33159375145201475, 0.3554012671338876, 0.4162387716844718, 0.5067310634604401, 0.6060255736729159, 0.6701823868897268, 0.703810518356265, 0.9473118609303143, 0.9414585553921004, 1.2001693897554064, 1.3144083579839179, 1.5223795348401936, 1.749554025137424, 1.8979688208477088, 2.203263570323253, 2.3940717305314494, 2.97467318999606, 3.571896723726299, 4.390809883745856, 5.543745425608913, 6.958182158744936, 9.191378908508128, 12.731906825074386, 20.739096663750406]
average error:
[0.015800000000000012, 0.03334352442065952, 0.04615472623479457, 0.06773190921209307, 0.09142969715196854, 0.09711577238209115, 0.12056023274545502, 0.13138513639366375, 0.15304802070046017, 0.20006317706138974, 0.2238792342535745, 0.2490463318996967, 0.25137847485244497, 0.3493726153628638, 0.3187172606501223, 0.3389301627088234, 0.4672319794489575, 0.4638511497787497, 0.588465337667783, 0.5605564127513811, 0.6099970372944454, 0.7834147729024434, 0.8041090618753479, 0.8842934911319332, 1.0420310065781886, 1.0544800763407003, 1.315547847204918, 1.3387625749555867, 1.4875190345640121, 1.595407173222919]
"""
