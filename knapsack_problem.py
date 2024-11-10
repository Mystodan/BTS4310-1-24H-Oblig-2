from dataclasses import dataclass
from random import random
from knapsack import *

# Konstanter
ST = ConstructMethod.SortType # SORT TYPE
SO = ConstructMethod.SortOrder # SORT ORDER
VALUE_LIMITS = (10,20) # [min, max] NOK, verdi grenser for gjenstander
WEIGHT_LIMITS = (1,5) # [min, max] kg, vekt rekkevide generert for gjenstander
WEIGHT_CAPACITY = 25 # Kapasitet, kg for knapsacken
ITEMS = generate_item_list(limiter_value=VALUE_LIMITS, limiter_weight=WEIGHT_LIMITS, max_items=50)
MUTATION_RATE = 0.5 # Sannsynlighet for mutasjon
CHILDREN_PAIRS = 50 # Antall barn som skal genereres

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

def genetic_algorithm(parents:list[tuple[Knapsack,list[Item]]]):
    """Genetisk algoritme for å løse knapsack problemet"""
    mut_rat = MUTATION_RATE

    # Fase 1 - Bruke Initial algoritme
    løsninger = parents

    # Fase 2 - Optimering med bruk av Genetisk algoritme
    ## Evaluering av løsninger
    solution_indexes = [0,1]
    for i, val in enumerate(sols:= (evaluate_solutions(evaluate_value_weight, [løsning for løsning in løsninger], WEIGHT_CAPACITY))): 
        if sols[solution_indexes[0]] < val : 
            solution_indexes[0] = i
        if sols[solution_indexes[1]] > val : 
            solution_indexes[1] = i
    solution_indexes = solution_indexes+[sol for sol in range(len(sols)) if sol not in solution_indexes]
    løsninger = [løsninger[i] for i in solution_indexes]


    ## Konvertere løsninger til binær form
    bin_løsninger:list[bytearray] = []
    for løsning in løsninger:
        bin_løsninger.append(convert_solution_to_binary(outside=løsning[1], inside=løsning[0], original=ITEMS))
    
    ## Gjør løsninger til foreldre
    parents = bin_løsninger.copy()


    ## Genetisk algoritme start
    iterations = 1
    while iterations <= 1000:
        ## Genererer barn
        children : list[bytearray] = []
        children.extend(parents)
        evals: list[tuple[tuple[Knapsack,list[Item]], tuple[float,float]]] = []
        while len(children) < 100 :
            for i, løsning in enumerate(parents):
                ## Krysning
                if i % 2 == 0:
                    children.extend(two_point_crossover((parents[i], parents[i+1])))
        
            
            ## Mutasjon 
            for child in children:
                children[children.index(child)] = mutate_solution_multi(child,  mutation_rate=mut_rat)
                solution = convert_binary_to_solution(child, ITEMS, WEIGHT_CAPACITY, weight_limit_ignore=True)
            ## Evaluering
                evaluation = best_eval(solution[0], WEIGHT_CAPACITY) 
                evals.append((solution, evaluation))
       
        ## Sorterer evalueringer
        sorted_evals = []  
        [sorted_evals.append(eval) for eval in evals if eval[1][1] >= 0.0 and eval not in sorted_evals] # Fjerner negative fitness, vekt over maks kapasitet
        sort_weight = sorted(sorted_evals, key=lambda x: x[1][1]) # Sorterer etter vekt
        sort_value = sorted(sorted_evals, key=lambda x: x[1][0], reverse=True) # Sorterer etter verdi
        ## Oppdaterer foreldre og konverterer til binær form
        parents = (
            [convert_solution_to_binary(outside=eval[0][1], inside=eval[0][0], original=ITEMS) for eval in sort_weight[:1]] +
            [convert_solution_to_binary(outside=eval[0][1], inside=eval[0][0], original=ITEMS) for eval in sort_value[:1]]
            )
        ## Oppdaterer mutasjonsrate ved å oppdatere iterasjoner
        if iterations % 100 == 0:
            mut_rat = max(MUTATION_RATE * 0.5, 0.001)
        iterations += 1
    return parents




if __name__ == "__main__":
    parents = [ # Genererer foreldre
        Construct.method_1(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
        Construct.method_2(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
        Construct.method_3(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
        Construct.method_4(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
    ]
    # Evaluering av foreldre
    print("genererer foreldre:\n")
    for parent in parents:
        solution = parent
        print(f"\tVerdi per vekt: {best_eval(solution[0], WEIGHT_CAPACITY)[0]/sum([item.weight for item in solution[0].items])}")
        print(f"\tFitness vekt: {best_eval(solution[0], WEIGHT_CAPACITY)[1]}")
        print(f"\tVekt: {sum([item.weight for item in solution[0].items])}")
        print(f"\tVerdi: {sum([item.value for item in solution[0].items])}")
        print(f"\tGjenstander: {len(solution[0].items)}\n")

   
    # Genetisk algoritme
    last_gen_children = genetic_algorithm(parents)
    
    # Evaluering av barn
    print("genererer barn:\n")
    for child in last_gen_children:
        solution = convert_binary_to_solution(child, ITEMS, WEIGHT_CAPACITY, weight_limit_ignore=True)
        print(f"\tVerdi per vekt: {best_eval(solution[0], WEIGHT_CAPACITY)[0]/sum([item.weight for item in solution[0].items])}")
        print(f"\tFitness vekt: {best_eval(solution[0], WEIGHT_CAPACITY)[1]}")
        print(f"\tVekt: {sum([item.weight for item in solution[0].items])}")
        print(f"\tVerdi: {sum([item.value for item in solution[0].items])}")
        print(f"\tGjenstander: {len(solution[0].items)}\n")
   
 