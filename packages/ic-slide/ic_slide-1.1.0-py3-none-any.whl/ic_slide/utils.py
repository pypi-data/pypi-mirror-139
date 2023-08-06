
def capitalize(test_dict):
    res = dict()
    for key in test_dict.keys():
        if isinstance(test_dict[key], dict):
            res[key[0].upper() + key[1:]] = capitalize(test_dict[key])
        else:
            res[key[0].upper() + key[1:]] = test_dict[key]
    return res
