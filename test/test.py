import multiprocessing


def f(x):
    print(multiprocessing.current_process().name)
    return x * x


def f1(i, map, v):
    map[i] = i
    v += 1


if __name__ == "__main__":
    # p = multiprocessing.Pool(processes=3)
    # print(p.map(f, range(200)))
    # for i in range(30):
    #     if i % 2 == 0:
    #         print("testing r", i, "\r")
    #     if i % 7 == 0:
    #         print(i)
    map = dict()
    v = 0
    for i in range(10):
        f1(i, map, v)
    print(map)
    print(v)

