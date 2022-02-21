import math
import random

def function1(x):
    '''
    First objective funtion

    Parameters
    ----------
    x : list
        We take vector as list of values.

    Returns
    -------
    float
        We return first value of vector.

    '''
    return x[0]
    
def function2(x):
    '''
    Second objective function.

    Parameters
    ----------
    x : list
        We take vector as list of values.

    Returns
    -------
    float
        We return the value of funtion f2 for value x.

    '''
    g = 1 + 9/(len(x)-1)*math.fsum(x[1:])
    return g*(1-math.sqrt(x[0]/g))

def non_dominated_sorting(population, values1, values2):
    '''
    Function for non dominate sorting.

    Parameters
    ----------
    population : list
        Set of vectors (vectors given as list).
    values1 : list
        Values of f1 for given vectors.
    values2 : list
        Values of f2 for given vectors.

    Returns
    -------
    fronts : list
        This is list of fronts, fronts are given as list, elements of fronts
        are given as list of 3 elements: index of vector from population,
        vector and number of its front.

    '''
    dominates = [[]for x in range(len(values1))]
    fronts = []
    domination_count = [0 for x in range(len(values1))]
    for p_index in range(len(values1)):
        for q_index in range(len(values1)):
            # =================================================================
            #comparing two vectors p and q to see if one dominates the other or 
            #vice versa
            # =================================================================
            if p_index == q_index:
                continue
            elif ((values1[p_index] <= values1[q_index] and values2[p_index] <= values2[q_index]) and
                (values1[p_index] < values1[q_index] or values2[p_index] < values2[q_index])):
                dominates[p_index].append(q_index)
            elif ((values1[q_index] <= values1[p_index] and values2[q_index] <= values2[p_index]) and
                (values1[q_index] < values1[p_index] or values2[q_index] < values2[p_index])):
                domination_count[p_index] += 1
    front_index = 0
    tresh = []
    while(domination_count != [0 for i in range(len(domination_count))]):
        fronts.append([[x, population[x], front_index] for x in range(len(domination_count)) if (domination_count[x]==0 and x not in tresh)])
        # =====================================================================
        #we put y and z so we can ignore them in this loop
        # =====================================================================
        for front_elem, y, z in fronts[front_index]:
            for x in range(len(domination_count)):
                if x in dominates[front_elem]:
                    domination_count[x] -= 1
        for x, y, z in fronts[front_index]:
            tresh.append(x)
        front_index += 1
    
    
    return fronts

def sorting_values_in_front(front, values):
    '''
    Sorting population front

    Parameters
    ----------
    front : list
        List of front where each element is list of 3, index of vector from 
        population, vector and number of its front.
    values : list
        List of values of objective function for elements from this front.

    Returns
    -------
    list_to_sort : list
        Sorted list of 2 elements, index of element in population, and value.

    '''
    list_to_sort = [(x, values[x]) for x, y, z in front]
    list_to_sort.sort(key=lambda x: x[1])
    return list_to_sort

def crowding_distance(front, values1, values2):
    '''
    Function that append crowding distance value to element of front.

    Parameters
    ----------
    front : list
        List of front where each element is list of 3, index of vector from 
        population, vector and number of its front.
    values1 : list
        Values of f1 for given vectors.
    values2 : list
        Values of f2 for given vectors.

    Returns
    -------
    front : list
        List of front where each element is list of 4, index of vector from 
        population, vector, number of its front and crowding distance value.

    '''
    #calculating crowding distance for front and sorting it by cd
    distances = [0 for x in range(len(front))]
    sorted1 = sorting_values_in_front(front, values1)
    sorted2 = sorting_values_in_front(front,values2)
    values1_of_front = [x[1] for x in sorted1]
    values2_of_front = [x[1] for x in sorted2]
    front[0].append(distances[0])
    distances[len(front)-1] = math.inf
    front[len(front)-1].append(distances[len(front)-1])
    for k in range(len(front)):
        #used formula for calculating crowding distance
        i1 = sorted1.index((front[k][0],values1[front[k][0]]))
        i2 = sorted2.index((front[k][0],values2[front[k][0]]))
        if (i1 == 0 or i2 == 0):
            distances[k] = math.inf
        elif (i1 == len(front)-1 or i2 == len(front)-1):
            distances[k] = math.inf
        else:
            if (max(values1_of_front)-min(values1_of_front)) == 0:
                distances[k] = distances[k]
            else:
                distances[k] = distances[k] + (sorted1[i1+1][1] - sorted1[i1-1][1])/(max(values1_of_front)-min(values1_of_front))
                distances[k] = distances[k] + (sorted2[i2+1][1] - sorted2[i2-1][1])/(max(values2_of_front)-min(values2_of_front))
        front[k].append(distances[k])
    return front

def crossover(parent1, parent2):
    '''
    Function for crossover.

    Parameters
    ----------
    parent1 : list
        Vector of parent1 given as list.
    parent2 : list
        Vector of parent2 given as list.

    Returns
    -------
    child1 : list
        Vector of child1 given as list.
    child2 : list
        Vector of child2 given as list.

    '''
    child1 = []
    child2 = []
    for gen in range(len(parent1)):
        r = random.random()
        if r > 0.5:
            child1.append(parent1[gen])
            child2.append(parent2[gen])
        else:
            child1.append(parent2[gen])
            child2.append(parent1[gen])
    return child1, child2

def mutation (child):
    '''
    We will mutate radnomly picked gene with prob 10%.

    Parameters
    ----------
    child : list
        Vector of child given as list.

    Returns
    -------
    child : list
        Vector of mutated child given as list.

    '''
    mutation_prob = random.random()
    if mutation_prob > 0.90:
        mutated_gene = random.randint(0, len(child)-1)
        child[mutated_gene] = random.uniform(0, 1)
    return child

def dividing_population(fronts, values1, values2):
    '''
    Survival of 50% fittest.

    Parameters
    ----------
    fronts : list
        This is a list of fronts, fronts are given as list of list of 4 
        elements, index of vector from  population, vector, number of its front
        and crowding distance value.
    values1 : list
        Values of f1 for given vectors.
    values2 : list
        Values of f2 for given vectors.

    Returns
    -------
    population : list
        List of vectors, top 50%.

    '''
    population = []
    for front in fronts:
        if (len(population)==50):
            break
        elif ((len(population) + len(front)) <=50):
            population.extend(front)
        elif ((len(population) + len(front)) > 50):
            new_list = sorted(front, key=lambda x: x[3], reverse=True)
            population.extend(new_list[:50-(len(population))])
    return population
            
def making_children(divided_population):
    '''
    Making new population of 50% fittest and it's offspring.

    Parameters
    ----------
    divided_population : list
        List of vectors, top 50%.

    Returns
    -------
    new_population : list
        New population that contain parents and childrens.

    '''
    parent1 = []
    parent2 = []
    new_population = []
    while(len(divided_population)>0):
        parent1_1, parent1_2 = random.sample(divided_population, 2)
        if parent1_1[2] < parent1_2[2]:
            parent1 = parent1_1
        elif parent1_1[2] > parent1_2[2]:
            parent1 = parent1_2
        else:
            if parent1_1[3] <= parent1_2[3]:
                parent1 = parent1_2
            else:
                parent1 = parent1_1
        divided_population.remove(parent1)
        if len(divided_population) == 1:
            parent2 = divided_population[0]
        else:    
            parent2_1, parent2_2 = random.sample(divided_population, 2)
            if parent2_1[2] < parent2_2[2]:
                parent2 = parent2_1
            elif parent2_1[2] > parent2_2[2]:
                parent2 = parent2_2
            else:
                if parent2_1[3] <= parent2_2[3]:
                    parent2 = parent2_2
                else:
                    parent2 = parent2_1
        divided_population.remove(parent2)
        child1, child2 = crossover(parent1[1], parent2[1])
        child1 = mutation(child1)
        child2 = mutation(child2)
        new_population.extend([parent1[1], parent2[1], child1, child2])
    return new_population