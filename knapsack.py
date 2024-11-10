from enum import Enum
from random import randint


class Item():
    def __init__(self, weight, value):
        """Initialiserer en gjenstand\n
        weight: Vekt\n
        value: Verdi"""
        self.weight :int= weight
        self.value :int= value

class Knapsack():
    def __init__(self, capacity):
        """Initialiserer en knapsack\n
        capacity: Kapasitet"""
        self.capacity = capacity
        self.items = []
        self.value = 0
        self.weight = 0

    def add_item(self, item:Item):
        """Legger til en gjenstand i knapsacken\n
        item: Gjenstand som skal legges til"""
        assert self.weight + item.weight <= self.capacity,"Item exceeds capacity"
        self.items.append(item)
        self.value += item.value
        self.weight += item.weight

    def add_items(self, items:list[Item], assert_ignore = False):
        """Legger til flere gjenstander i knapsacken\n
        items: Liste med gjenstander som skal legges til\n
        assert_ignore: Ignorerer assert"""

        if not assert_ignore: assert self.weight + sum([item.weight for item in items]) <= self.capacity, "Items exceeds capacity"
        self.items.extend(items)
        self.value += sum([item.value for item in items])
        self.weight += sum([item.weight for item in items])

    def get_items_not_in_knapsack(self, items:list[Item]):
        """Henter gjenstander som ikke er i knapsacken\n
        items: Liste med gjenstander\n
        return: Liste med gjenstander som ikke er i knapsacken"""
        return [element for element in items if element not in self.items]
    
    def get_item_values(self):
        """Henter verdier for gjenstander i knapsacken\n"""
        return [element.value for element in self.items]
    def get_item_value_sum(self):
        """Henter summen av verdier for gjenstander i knapsacken\n"""
        return sum([element.value for element in self.items])
    def get_item_weights(self):
        """Henter vektene for gjenstander i knapsacken\n"""
        return [element.weight for element in self.items]
    def get_item_value_per_weight(self):
        """Henter verdi per vekt for gjenstander i knapsacken\n"""
        return sum([element.value for element in self.items])/sum([element.weight for element in self.items])


class ConstructMethod():
    class SortType(Enum):
        """Sorterings type"""
        VALUE = 1
        WEIGHT = 2
        VALUE_WEIGHT = 3
    class SortOrder(Enum):
        """Sorterings rekkefølge"""
        ASCENDING = 1
        DESCENDING = 2
    
    def sort_items(self, items:list[Item], sort_type, sort_order):
        """Sorterer gjenstander basert på type og rekkefølge\n
        items: Liste med gjenstander\n
        sort_type: Type sortering\n
        sort_order: Rekkefølge\n
        return: Sortert liste"""
        return sorted(items, key=lambda item: item.value if sort_type == self.SortType.VALUE else item.weight, reverse=True if sort_order == self.SortOrder.DESCENDING else False) 
   
    def __init__(self, items:list[Item], capacity, sort_type, sort_order):
        """Initialiserer konstruktør\n
        items: Liste med gjenstander\n
        capacity: Kapasitet\n
        sort_type: Type sortering\n
        sort_order: Rekkefølge"""
        self.items = self.sort_items(items, sort_type, sort_order)
        self.capacity = capacity
        
   
    def construct(self) -> tuple[Knapsack, list[Item]]:
        """Konstruerer en løsning\n
        return: Tuple med gjenstander i knapsack og gjenstander som ikke er i knapsacken"""
        knapsack = Knapsack(capacity=self.capacity)
        for item in self.items:
            if knapsack.weight + item.weight <= knapsack.capacity:
                knapsack.add_item(item)
        return knapsack, [element for element in self.items if element not in knapsack.items]

def generate_item_list(max_items, limiter_weight:tuple[int,int], limiter_value:tuple[int,int]) -> list[Item]:
    """Genererer en liste med gjenstander\n
    max_items: Antall gjenstander som skal genereres\n
    limiter_weight: Tuple med [min, max] vekt for gjenstander\n
    limiter_value: Tuple med [min, max] verdi for gjenstander\n
    return: Liste med gjenstander"""
    return [Item(weight=randint(limiter_weight[0], limiter_weight[1]), value=randint(limiter_value[0], limiter_value[1])) for _ in range(max_items)]

def convert_solution_to_binary(outside:list[Item], inside:Knapsack, original:list[Item]) -> bytearray:
    """Konverterer en løsning til binær form\n
    outside: Gjenstander som ikke er i knapsacken\n
    inside: Knapsacken\n
    original: Liste med gjenstander\n
    return: Binær liste"""
   
    assert len(original) == (len(outside)+len(inside.items))
    bin_list:bytearray = bytearray(len(original))
    for item in original:
        bin_list[original.index(item)] = 1 if item in inside.items else 0
    return bin_list

def convert_binary_to_solution(binary:bytearray, original:list[Item], capacity:int, weight_limit_ignore = False) -> tuple[Knapsack, list[Item]]:
    """Konverterer en binær løsning til en liste med gjenstander\n
    binary: Løsning i binær, 0 = utenfor, 1 = innenfor knapsacken\n
    original: Liste med gjenstander\n
    return: Lister med gjenstander"""

    assert len(binary) == len(original), "Binary and original list have different lengths"
    new_knapsack = Knapsack(capacity=capacity)
    new_knapsack.add_items([original[i] for i in range(len(binary)) if binary[i] == 1], assert_ignore=weight_limit_ignore)
    return new_knapsack, [original[i] for i in range(len(binary)) if binary[i] == 0]

def evaluate_weight_fitness(solution:Knapsack, capacity:int) -> tuple[float,float]:
    """Evaluerer fitnessen til en løsning basert på vekt\n
    solution: Liste med gjenstander\n
    capacity: Vekt kapasitet\n
    return: Fitness, lavere er bedre"""
    fitness = 1-sum([item.weight for item in solution.items])/capacity 
    return fitness, fitness

def evaluate_value_weight(solution:Knapsack, capacity:int) -> tuple[float,float]:
    """Evaluerer fitnessen til en løsning basert på verdi/vekt\n
    solution: Liste med gjenstander\n
    return: verdi per gjenstand, høyere er bedre"""
    value_per_weight = solution.get_item_value_sum()/sum(solution.get_item_weights())
    return value_per_weight, value_per_weight

def best_eval(solution:Knapsack, capacity:int) -> tuple[float,float]:
    """Evaluerer fitnessen til en løsning basert på verdi/vekt og vekt\n
    solution: Liste med gjenstander\n
    return: Tuple med verdi per gjenstand, høyere er bedre og fitness vekt, lavere er bedre, utenom negative tall"""
    weight_sum = sum(solution.get_item_weights())  
    if weight_sum > capacity:
        return 0.0, -1.0 # Returnerer 0.0 for verdi per vekt og -1.0 for fitness vekt, hvis verdien er over kapasitet
    fitness = 1-sum([item.weight for item in solution.items])/capacity 
    return solution.get_item_value_sum(), fitness 

def evaluate_solutions(evaluation_function,solution:list[tuple[Knapsack, list[Item]]], capacity:int) -> list[float]:
    """Evaluerer en liste med løsninger\n
    evaluation_function: Funksjon for evaluering av løsning\n
    solution: Liste med løsninger\n
    capacity: Kapasitet\n
    return: Liste med evalueringer"""
    return [evaluation_function(sol[0], capacity) for sol in solution] # Evaluering av flere løsninger