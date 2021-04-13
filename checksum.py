def get_checksum(items_list):
    seed = 113
    limit = 10000007
    result = 0

    for item in items_list:
        result += id(item)
        result *= seed
        result %= limit

    return result

