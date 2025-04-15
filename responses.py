
def Ok202(status, content):
    return {
        "statusCode": 102,
        "status": status,
        "content" : content
    }, 202

def Ok200(status, content):
    return {
        "statusCode": 200,
        "status": status,
        "content" : content
    }, 200

def Error400(status, content):
    print(status, content)
    return {
        "statusCode": 400,
        "status": status,
        "content" : content,
    }, 400

def Error401(content):
    return {
        "statusCode": 401,
        "status": "error 401",
        "content" : content
    }, 401


def Error500(content, debugError):
    return {
        "statusCode": 500,
        "status": "erro 500",
        "content" : content,
        "debugError": debugError
    }, 500

