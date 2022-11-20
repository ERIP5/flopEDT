import json

def execute_query(client_query, query, type):
    response = client_query(query)
    content = json.loads(response.content)
    """ print(content)
    assert False """
    assert 'errors' not in content
    res = content["data"][type]["edges"]
    return res

def append_data(data, key, val):
    if type(val) in (str, int, float, bool):
        data.setdefault(key, [])
        data[key].append(val)
    else:
        for k, v in val.items():
            append_data(data, k, v)

def get_data(res):
    data = {}
    for r in res:
        for key, val in r["node"].items():
            append_data(data, key, val)
    return data
