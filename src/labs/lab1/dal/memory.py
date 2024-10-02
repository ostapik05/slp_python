def memory_set(memory, calculation):
    memory = calculation["result"]
    print("Значення збережено в пам'яті.")
    return memory


def memory_save(memory, calculation):
    memory += calculation["result"]
    print("Значення збережено в пам'яті.")
    return memory


def memory_retrieve(memory):
    if memory:
        print(f"Значення з пам'яті: {memory}")
        return memory
    else:
        print("Пам'ять порожня.")
        return 0


def memory_clean():
    print("Пам'ять очищена.")
    return 0
