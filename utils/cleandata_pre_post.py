import json


def list_dumps(post_req):
    for field in list(post_req):
        if type(post_req[field]) == list:
            post_req[field] = json.dumps(post_req[field])
    return post_req
