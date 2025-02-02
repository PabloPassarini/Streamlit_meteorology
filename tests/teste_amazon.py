def findNumber(numbers):
    # Enquanto tivermos mais de dois números, continuamos o processo de redução
    while len(numbers) > 2:
        new_numbers = []
        
        # Percorremos a lista somando pares adjacentes e pegando apenas o último dígito
        for i in range(len(numbers) - 1):
            soma = numbers[i] + numbers[i + 1]
            new_numbers.append(soma % 10)  # Pegamos apenas o último dígito
        
        # Atualizamos a lista com os novos números gerados
        numbers = new_numbers
    
    # Retornamos os dois últimos números como string de dois caracteres
    return str(numbers[0]) + str(numbers[1])

# Exemplo de uso
numbers = [4, 5, 6, 7]
resultado = findNumber(numbers)
print(resultado)  # Saída esperada: "04"
