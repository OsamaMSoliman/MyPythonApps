def first_path():
    pass


def second_path():
    pass


def run():
    first_path()
    second_path()


if __name__ == "__main__":
    run()

    list = []

    for i in range(10):
        list.append(i)

    count = 0
    for i in list:
        if i % 2 == 0:
            list[count] = None
        count += 1

    for i in range(10):
        list.append(i)

    for o in list:
        print(o)
