def consolidate_summaries(dict1, dict2):
    """
    Merges two dictionaries by appending values based on their data types,
    only if the values are not None or empty strings.
    """
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                consolidate_summaries(dict1[key], dict2[key])
            elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                dict1[key].extend(
                    [item for item in dict2[key] if item is not None and item != ""]
                )
            elif isinstance(dict1[key], str) and isinstance(dict2[key], str):
                if dict2[key] is not None and dict2[key] != "":
                    dict1[key] = f"{dict1[key]}|{dict2[key]}"
            else:
                if dict2[key] is not None and dict2[key] != "":
                    dict1[key] = dict2[key]
        else:
            if dict2[key] is not None and dict2[key] != "":
                dict1[key] = dict2[key]
    return dict1
