from typing import List

def flattened_list_of_lists(list_of_lists: List[List], unique: bool = False) -> List:
    flat = [item for sublist in list_of_lists for item in sublist]

    if unique:
        flat = list(set(flat))

    return flat

if __name__ == "__main__":
    import random as rnd
    l_o_l = [[x for x in range(rnd.randint(5, 10))] for y in range(rnd.randint(5, 10))]

    print(l_o_l)
    print(flattened_list_of_lists(l_o_l))
    print(flattened_list_of_lists(l_o_l, unique=True))
