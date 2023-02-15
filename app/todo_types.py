import json


class Todo(str):
    """ Todo object in json format
    """
    
    def __new__(cls, title: str, is_done=False):
        todo = json.dumps({
            'title': title,
            'is_done': is_done
        })
        instance = super().__new__(cls, todo)
        return instance