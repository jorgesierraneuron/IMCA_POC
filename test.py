from concurrent.futures import ThreadPoolExecutor, as_completed


lista = list(range(1, 22))

sub_lista = []
for i in range(0, len(lista), 5):
    
    sub_lista.append(lista[i:i+5])

print(sub_lista)  


def multiply(numbers):
    
    for i in range(0,len(numbers)):

        numbers[i] = numbers[i]*2

    return numbers

    

results = []
       
with ThreadPoolExecutor(max_workers=5) as executor:

    futue_process ={executor.submit(multiply,numbers): numbers for numbers in sub_lista}
    for future in as_completed(futue_process):
        result = future.result()
        results.append(result)


print(results)


