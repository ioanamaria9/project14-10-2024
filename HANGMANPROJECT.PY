import csv


alfabet_romanesc_eficient = "EARIOTNSULCDPMGHBVĂÎȘȚZQJXFWÂ"


# functie citire fisier csv
def citeste_csv(file_path):
    jocuri = []
    with open(file_path, mode='r', encoding='utf-8') as file: # deschide fisierul pentru a citi impreuna cu caracterele speciale din el
        csv_reader = csv.reader(file, delimiter=';') # creez un reader care citeste fisierul csv (valorile sunt separate de ;)
        for row in csv_reader:
            cod_joc = row[0] # coloana 1
            cuvant_mascat = row[1] # coloana 2
            cuvant_complet = row[2] # coloana 3
            jocuri.append((cod_joc, cuvant_mascat, cuvant_complet)) # returneaza lista de jocuri , fiecare element din lista fiind un tuple
    return jocuri


# functie ghicit cuvinte
def ghiceste_cuvant(cuvant_mascat, cuvant_complet):
    cuvant_curent = list(cuvant_mascat)
    incercari = 0
    litere_folosite = set()

    # parcurg literele din alfabet eficient
    for litera in alfabet_romanesc_eficient:
        if litera in cuvant_complet:  # doar daca litera este în cuvantul complet
            litere_folosite.add(litera) # adaug litera in multimea de litere ghicite
            incercari += 1

            # verific fiecare literă din cuvant
            for i, litera_completa in enumerate(cuvant_complet):
                if cuvant_curent[i] == '*' and litera_completa == litera: # verific pozitia actuala din cuvant este * si litera ghicita corespunde cu litera  din poz resp
                    cuvant_curent[i] = litera  # inlocuiesc '*' cu litera ghicita

            # programul se opreste atunci cand cuvantul este complet
            if ''.join(cuvant_curent) == cuvant_complet:
                break # daca toate literele au fost ghicite , bucla se opreste

    return ''.join(cuvant_curent), incercari # functia returneaza cuvantul completat si numarul de incercari folosite


# functie rulare joc
def joc_hangman(file_path): # file_path = calea catre fisier csv
    jocuri = citeste_csv(file_path) # returneaza o lista de tuple
    rezultate = [] # lista goala care va stoca rezultatele fiecarui joc
    total_incercari = 0

    for cod_joc, cuvant_mascat, cuvant_complet in jocuri:
        cuvant_ghicit, numar_incercari = ghiceste_cuvant(cuvant_mascat, cuvant_complet) # incearca sa ghiceasca cuv mascat folosinf un nr de incercari
        rezultate.append((cod_joc, cuvant_mascat, cuvant_ghicit, numar_incercari)) # adauga rezultatelr in lista rezultate
        total_incercari += numar_incercari

    return rezultate, total_incercari


# functie afisare rezultate
def afiseaza_rezultate(rezultate, total_incercari):
    for cod_joc, cuvant_mascat, cuvant_ghicit, incercari in rezultate:
        print(f"Joc {cod_joc}: -> '{cuvant_mascat}' -> '{cuvant_ghicit}' -> Încercări: {incercari}")

    # numarul total de incercari
    print(f"\nSuma totală a încercărilor: {total_incercari}")



file_path = 'cuvinte_de_verificat.txt'

# rulare joc
rezultate, total_incercari = joc_hangman(file_path)

# verific nr total sa fie sub 1200
if total_incercari <= 1200:
    afiseaza_rezultate(rezultate, total_incercari)
else:
    print(f"\nSuma totală a încercărilor: {total_incercari} depășește 1200.")