import random
comp_num = 10
mutation = 0.1
GA_iter = 10
pop_size = 20
pop_select_part = 0.2
survived_percent = 20/100
max = 1000000

graf =[
    [max, 220, 802, 811, 898, 212, 618, 688, 999, 702],
    [220, max, 844, 434, 369, max, 440, 249, 744, 997],
    [802, 844, max, max, 126, 932, 150, 750, 785, 758],
    [811, 434, max, max, 165, max, 725, 449, 345, 707],
    [898, 369, 126, 165, max, 563, 107, 136, 178, 858],
    [212, max, 932, max, 563, max, 839, 814, 792, 649],
    [618, 440, 150, 725, 107, 839, max, 235, 163, 755],
    [688, 249, 750, 449, 136, 814, 235, max, 100, 248],
    [999, 744, 785, 345, 178, 792, 163, 100, max, 951],
    [702, 997, 758, 707, 858, 649, 755, 248, 951, max],
]


def clean_path(arr, last_node):
    for i in range(len(arr)):
        if arr[i] == last_node:
            return arr[: i + 1]


def find_index_value(arr, value):
    for i in range(len(arr)):
        if arr[i] == value:
            return i


def calc_path(arr, last_node):
    path = 0
    for i in range(len(arr) - 1):
        path += graf[arr[i]-1][arr[i + 1]-1]

        if arr[i + 1] == last_node:
            break
    return path

def GA(first_comp,last_comp, mutation, GA_iter):
    pop = []

    def mutate(vec, index_last_node):
        if index_last_node <= 1:
            return vec
        else:
            mut_index = random.randint(1, index_last_node - 1)
            mut_value = random.randint(1, comp_num)
            vec[mut_index] = mut_value
            return vec

    print("\nПервоначальная популяция: ")
    for i in range(20):
        vec = []
        vec.append(first_comp)
        for j in range(6):
            vec.append(random.randint(1, comp_num))
        vec.append(last_comp)
        pop.append(vec)
        print(str(i+1) + " : " + str(vec))

    parents_num = int(survived_percent * pop_size)
    best_path = ( max, max, max)
    for i in range(GA_iter):
        while len(pop) < pop_size:
            if random.random() < mutation:
                # Мутация
                c = random.randint(0, parents_num)
                pop.append(mutate(ranked[c], find_index_value(ranked[c], last_comp)))
            else:
                # Скрещивание
                c1 = random.randint(0, parents_num)
                c2 = random.randint(0, parents_num)
                if (find_index_value(ranked[c1], last_comp)) <= 1:
                    pop.append(ranked[c1])
                else:
                    j = random.randint(1, last_comp - 1)
                    pop.append(ranked[c1][0:j]+ranked[c2][j:])
                    pop.append(ranked[c2][0:j]+ranked[c1][j:])

        sum = 0
        scores = []
        for v in pop:
            i_first_last_node = find_index_value(v, last_comp)
            scores.append((calc_path(v, last_comp), v, i_first_last_node))
            sum += calc_path(v, last_comp)

        scores.sort()

        print("\nИтерация № " + str(i + 1))
        print("Лучший путь : длина - %s, маршрут - %s, количество узлов до цели: %s" %(str(scores[0][0]),str(scores[0][1]),str(scores[0][2])))
        print("Худший путь : длина - %s, маршрут - %s, количество узлов до цели: %s " %(str(scores[-1][0]),str(scores[-1][1]),str(scores[-1][2])))
        print("Средний путь: " + str(sum/len(scores)))

        if best_path[0] > scores[0][0]:
            best_path = [scores[0][0], scores[0][1].copy(), i + 1]
            print("\nНовый лучший путь: " + str(best_path))

        # Сначала включаем только победителей
        ranked = [v for (s, v, i) in scores]
        pop = ranked[0:parents_num]

    return (best_path)

first_comp = (int(input("Введите номер первой вершины: (от 1 до 10) ")))
last_comp = int(input("Введите номер конечной вершины: (от 1 до 10)"))
if (int(input("Для остальных настроек нажмите 1:"))==1):
    mutation=int(input("Введите количество мутаций в процентах (0%-100%):"))/100
    GA_iter = int(input("Введите количество итераций: "))
    print(
        "Номер компьютера-отправителя: %s, номер компьютера-получателя: %s. \n Количество мутаций: %s. Число итераций: %s" % (
        first_comp, last_comp, mutation, GA_iter))
else:
    print("Номер компьютера-отправителя: %s, номер компьютера-получателя: %s" % (first_comp, last_comp))


find_path = GA(first_comp, last_comp,mutation,GA_iter)

print("\n\nОТВЕТ для нач. узла " + str(first_comp) + " и кон. узла " + str(last_comp))
print("Итерация: " + str(find_path[2]))
print("Маршрут: " + str(clean_path(find_path[1], last_comp)))
print("Длина пути  : " + str(find_path[0]) + "\n")

