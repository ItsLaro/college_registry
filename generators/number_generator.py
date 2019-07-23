def studnum_gen(num=0):
    while True:
        num += 1
        yield "Student #" + str(num)
