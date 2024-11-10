# Beskrivelse: Hovedprogram for knapsack problemet, med genetisk algoritme
from knapsack_class import generate_item_list, print_evaluation_values
from knapsack_logic import Construct, convert_binary_to_solution, genetic_algorithm

# Konstanter
VALUE_LIMITS = (10,20) # [min, max] NOK, verdi grenser for gjenstander
WEIGHT_LIMITS = (1,5) # [min, max] kg, vekt rekkevide generert for gjenstander
WEIGHT_CAPACITY = 25 # Kapasitet, kg for knapsacken
ITEMS = generate_item_list(limiter_value=VALUE_LIMITS, limiter_weight=WEIGHT_LIMITS, max_items=50)
MUTATION_RATE = 0.001 # Sannsynlighet for mutasjon
CHILDREN_PAIRS = 50 # Antall barn som skal genereres





if __name__ == "__main__":
    # Genererer foreldre / initielle løsninger
    parents = [ 
        ## Metode 1 - Sorter gjenstander etter økende vekt
        Construct.method_1(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
        ## Metode 2 - Sorter gjenstander etter synkende verkt
        Construct.method_2(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
        ## Metode 3 - Sorter gjenstander etter økende verdi
        Construct.method_3(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
        ## Metode 4 - Sorter gjenstander etter synkende verdi
        Construct.method_4(items=ITEMS, capacity=WEIGHT_CAPACITY).construct(),
    ]
    # Evaluering av første generasjons foreldre
    print("genererer foreldre:\n")
    for parent in parents:
        print_evaluation_values(parent, WEIGHT_CAPACITY) #

   
    # Genetisk algoritme optimering, med two-point crossover og mutasjon av barn basert på sannsynlighet
    last_gen_children = genetic_algorithm(
        original_parents=parents, # Foreldre
        children_pair_amount=CHILDREN_PAIRS, # Antall barn
        original=ITEMS, # Gjenstander som skal sorteres i knapsacken
        mutation_rate=MUTATION_RATE, # Sannsynlighet for mutasjon
        weight_capacity=WEIGHT_CAPACITY) # Kapasitet for knapsacken
    
    # Evaluering av genererte barn
    print("genererer barn:\n")
    for child in last_gen_children:
        print_evaluation_values(
            convert_binary_to_solution(child, ITEMS, WEIGHT_CAPACITY, weight_limit_ignore=True), 
            WEIGHT_CAPACITY) # Skriver ut evaluering av løsning
        