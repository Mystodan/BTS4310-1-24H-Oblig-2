# BTS4310-1-24H-Oblig-2
Av Daniel Hao Huynh

Genetisk algoritme for 0/1 Knapsack Problemet.

I denne obligatoriske oppgaven, så har jeg implementert en genetisk algoritme for å løse 0/1 knapsack problemet.

### Knapsack 0/1 Problemet
Knapsack 0/1 problemet handler om å maksimere verdien av gjenstander som kan legges i en ryggsekk med en gitt vektkapasitet. Hver gjenstand har en verdi og en vekt, og man kan enten ta med en gjenstand (1) eller la være (0). Målet er å finne den kombinasjonen av gjenstander som gir maksimal totalverdi uten å overskride ryggsekkens vektkapasitet. Problemet er NP-komplett, så heuristiske metoder som genetiske algoritmer brukes ofte for å finne gode løsninger.

> Dette problemet er NP-komplett, noe som betyr at det ikke finnes noen kjent effektiv algoritme for å løse det for alle mulige tilfeller. Derfor brukes ofte heuristiske eller approksimative metoder, som genetiske algoritmer, for å finne gode løsninger innenfor rimelig tid.

### Min implementasjon
Jeg har valgt å implementere alle Metodene nevnt i Nourredine sine forelesninger for å initialiere foreldrene, basert på dette er dette foreldrene som barna arver fra(se __knapsack_class.py__):
```py
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

```
> Her ser du at Metodene er basert på Stigende/Synkende rekkefølger basert på Verdi/Vekt

### Kjøre filen

For å kjøre dette scriptet er det bare å bruke denne linjen fra root:
```sh
python main.py
```
### Resultater
>Dette er resultatet med bruk av __main.py__, med disse konstantene (merk at ITEMS er ikke egentlig en konstant siden den genererer listen med gjenstander):
```py
# Konstanter
VALUE_LIMITS = (10,20) # [min, max] NOK, verdi grenser for gjenstander
WEIGHT_LIMITS = (1,5) # [min, max] kg, vekt rekkevide generert for gjenstander
WEIGHT_CAPACITY = 25 # Kapasitet, kg for knapsacken
ITEMS = generate_item_list(
    limiter_value=VALUE_LIMITS, 
    limiter_weight=WEIGHT_LIMITS, 
    max_items=50)
MUTATION_RATE = 0.001 # Sannsynlighet for mutasjon
CHILDREN_PAIRS = 50 # Antall barn som skal genereres
```

Terminal output:
```
genererer foreldre:

        Verdi per vekt: 8.333333333333334
        Fitness vekt: 0.040000000000000036
        Vekt: 24
        Verdi: 200
        Gjenstander: 14

        Verdi per vekt: 3.16
        Fitness vekt: 0.0
        Vekt: 25
        Verdi: 79
        Gjenstander: 5

        Verdi per vekt: 4.84
        Fitness vekt: 0.0
        Vekt: 25
        Verdi: 121
        Gjenstander: 11

        Verdi per vekt: 7.4
        Fitness vekt: 0.0
        Vekt: 25
        Verdi: 185
        Gjenstander: 10

genererer barn:
    # barn 1 med sortering etter best verdi:
        Verdi per vekt: 8.4
        Fitness vekt: 0.0
        Vekt: 25
        Verdi: 210
        Gjenstander: 14
    # barn 2 med sortering etter best verdi/vekt:
        Verdi per vekt: 8.4
        Fitness vekt: 0.0
        Vekt: 25
        Verdi: 210
        Gjenstander: 14
```





