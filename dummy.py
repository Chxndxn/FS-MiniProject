heading = []
search_data = []
animalID_Name = input('Enter Animal ID or Name: ').capitalize()
with open('./files/animalRecord.txt','r') as fRead:
    for line in fRead:
        line = line.rstrip()
        search_animal = line.split('|')
        if search_animal[0] == 'Animal ID':
            string_search_animal = '|'.join(search_animal)
            heading.append(string_search_animal)
            continue
        elif search_animal[0] == animalID_Name or search_animal[1] == animalID_Name:
            string_search_animal = '|'.join(search_animal)
            search_data.append(string_search_animal)

print(heading)
print(search_data)