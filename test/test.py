import multiprocessing


def f(x):
    print(multiprocessing.current_process().name)
    return x * x


if __name__ == "__main__":
    p = multiprocessing.Pool(processes=3)
    print(p.map(f, range(200)))
