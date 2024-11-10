from dataclasses import dataclass
from random import random
from knapsack import *

ST = ConstructMethod.SortType # SORT TYPE
SO = ConstructMethod.SortOrder # SORT ORDER

@dataclass
class Construct:
    """Konstruksjonsmetoder for initial knapsack algoritme"""
    def method_1(items, capacity):
        """Konstruerer en knapsack ved å sortere items etter [økende][vekt], og legge til gjenstander i knapsack til kapasiteten er nådd"""
        return ConstructMethod(items=items, capacity=capacity, sort_type=ST.WEIGHT, sort_order=SO.ASCENDING)

    def method_2(items, capacity):
        """Konstruerer en knapsack ved å sortere items etter [synkende][vekt], og legge til gjenstander i knapsack til kapasiteten er nådd"""
        return ConstructMethod(items=items, capacity=capacity, sort_type=ST.WEIGHT, sort_order=SO.DESCENDING)

    def method_3(items, capacity):
        """Konstruerer en knapsack ved å sortere items etter [økende][verdi], og legge til gjenstander i knapsack til kapasiteten er nådd"""
        return ConstructMethod(items=items, capacity=capacity, sort_type=ST.VALUE, sort_order=SO.ASCENDING)

    def method_4(items, capacity):
        """Konstruerer en knapsack ved å sortere items etter [synkende][verdi], og legge til gjenstander i knapsack til kapasiteten er nådd"""
        return ConstructMethod(items=items, capacity=capacity, sort_type=ST.VALUE, sort_order=SO.DESCENDING)


def two_point_crossover(parents:tuple[bytearray,bytearray]) -> list[bytearray]:
    """Utfører to-punkts kryssing mellom to foreldre\n
    parents: Tuple med foreldre, bytearray med binære løsninger\n
    return: Tuple med to barn, bytearray med binære løsninger"""
    assert len(parents[0]) == len(parents[1]), "Foreldre har ulik lengde"
    def tp(parent_1, parent_2):
        """Utfører to-punkts kryssing mellom to foreldre\n"""
        crossover= parent_2[start_val:end_val]
        p1 = parent_1[:start_val]
        p2 = parent_1[end_val:]
        return p1+crossover+p2
    
    start_val = (randint(0, len(parents[0])-2)) 
    end_val = (randint(start_val, len(parents[0])-1)) 
 
    child_1 , child_2= tp(parents[1], parents[0]) ,tp(parents[0], parents[1])

    return [child_1, child_2]
    

def mutate_solution_single(solution:bytearray, mutation_rate:float):
    """Mutere en binær løsning\n
    solution: Løsning som skal muteres\n
    mutation_rate: Sannsynlighet for mutasjon\n
    return: Mutert løsning"""
    if random() <= mutation_rate:
        i = randint(0,len(solution)-1)
        solution[i] = 1 if solution[i] == 0 else 0
   
    return solution

def mutate_solution_multi(solution:bytearray, mutation_rate:float):
    """Mutere en binær løsning\n
    solution: Løsning som skal muteres\n
    mutation_rate: Sannsynlighet for mutasjon\n
    return: Mutert løsning"""
    for i in range(0,len(solution)-1):
        if random() <= mutation_rate:
            solution[i] = 1 if solution[i] == 0 else 0
    return solution

def genetic_algorithm(original_parents:list[tuple[Knapsack,list[Item]]],children_pair_amount:int, original: list[Item], mutation_rate:float, weight_capacity:int) -> list[bytearray]:
    """Genetisk algoritme for å optimalisere knapsack løsninger\n
    original_parents: Liste med foreldre, tuple med knapsack og gjenstander\n
    children_pair_amount: Antall par med barn som skal genereres, dvs, 2 par = 4 barn\n
    original: Liste med gjenstander\n
    mutation_rate: Sannsynlighet for mutasjon\n
    weight_capacity: Kapasitet\n
    return: Liste med binære løsninger"""

    # Fase 1 - Bruke Initial algoritme
    løsninger = original_parents.copy()

    # Fase 2 - Optimering med bruk av Genetisk algoritme
    ## Evaluering av løsninger
    solution_indexes = [0,1]
    for i, val in enumerate(sols:= (evaluate_solutions(evaluate_value_weight, [løsning for løsning in løsninger], weight_capacity))): 
        if sols[solution_indexes[0]] < val : 
            solution_indexes[0] = i
        if sols[solution_indexes[1]] > val : 
            solution_indexes[1] = i
    solution_indexes = solution_indexes+[sol for sol in range(len(sols)) if sol not in solution_indexes]
    løsninger = [løsninger[i] for i in solution_indexes]


    ## Konvertere løsninger til binær form
    bin_løsninger:list[bytearray] = []
    for løsning in løsninger:
        bin_løsninger.append(convert_solution_to_binary(outside=løsning[1], inside=løsning[0], original=original))
    
    ## Gjør løsninger til foreldre
    parents = bin_løsninger.copy()


    ## Genetisk algoritme start
    iterations = 1
    while iterations <= 1000:
        ## Genererer barn
        children : list[bytearray] = []
        children.extend(parents)
        evals: list[tuple[tuple[Knapsack,list[Item]], tuple[float,float]]] = []
        while len(children) < children_pair_amount :
            for i, løsning in enumerate(parents):
                ## Krysning
                if i % 2 == 0:
                    children.extend(two_point_crossover((parents[i], parents[i+1])))
        
            
            ## Mutasjon 
            for child in children:
                children[children.index(child)] = mutate_solution_multi(child,  mutation_rate=mutation_rate)
                solution = convert_binary_to_solution(child, original, weight_capacity, weight_limit_ignore=True)
            ## Evaluering
                evaluation = best_eval(solution[0], weight_capacity) 
                evals.append((solution, evaluation))
       
        ## Sorterer evalueringer
        sorted_evals = []  
        [sorted_evals.append(eval) for eval in evals if eval[1][1] >= 0.0 and eval not in sorted_evals] # Fjerner negative fitness, vekt over maks kapasitet
        sort_weight = sorted(sorted_evals, key=lambda x: x[1][1]) # Sorterer etter vekt
        sort_value = sorted(sorted_evals, key=lambda x: x[1][0], reverse=True) # Sorterer etter verdi
        ## Oppdaterer foreldre og konverterer til binær form
        parents = (
            [convert_solution_to_binary(outside=eval[0][1], inside=eval[0][0], original=original) for eval in sort_weight[:1]] +
            [convert_solution_to_binary(outside=eval[0][1], inside=eval[0][0], original=original) for eval in sort_value[:1]]
            )

        iterations += 1
    return parents





   
 