def findMaximumScore(stockPrices, k):
    # Encontra o valor mais frequente no vetor
    freq = {}
    for num in stockPrices:
        if num in freq:
            freq[num] += 1
        else:
            freq[num] = 1
    
    max_count = 0
    number_max = 0
    for num, count in freq.items():
        if count > max_count:
            max_count = count
            number_max = num

    # Função para verificar a maior sequência contígua de um número específico
    

    # Varredura da esquerda para a direita
    lst_esq = []
    k_stop = 0
    for i in stockPrices:
        if i != number_max and k_stop < k:
            k_stop += 1
        else:
            lst_esq.append(i)

    # Varredura da direita para a esquerda
    lst_dir = []
    k_stop = 0
    for i in reversed(stockPrices):
        if i != number_max and k_stop < k:
            k_stop += 1
        else:
            lst_dir.append(i)
    lst_dir = lst_dir[::-1]

    # Verifica a maior sequência contígua em ambas as listas
    max_esq = verificar_maior(lst_esq, number_max)
    max_dir = verificar_maior(lst_dir, number_max)

    # Retorna o maior valor entre as duas verificações
    return max(max_esq, max_dir)

def verificar_maior(lst, max_num):
        max_seq = 0
        seq = 0
        for i in lst:
            if i == max_num:
                seq += 1
                if seq > max_seq:
                    max_seq = seq
            else:
                seq = 0
        return max_seq
# Exemplo de uso
stockPrices = [7, 5, 7, 7, 1, 1, 7, 7]
k = 3
print(findMaximumScore(stockPrices, k))  # Saída esperada: 5