class ResultMessage:

    def __init__(self, data, state, message, code):
        self.data = data
        self.state = state
        self.message = message
        self.code = code


    # def get_message(self):
    #     return {"res": self.result, "state": self.state, "message": self.message, "code": self.code}