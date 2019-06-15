def hello():
    i = 1
    def hello_2():
        print(i)

    def hello_3():
        i = 3
        hello_2()

    hello_2()
    hello_3()
hello()