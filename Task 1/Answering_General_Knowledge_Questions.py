import wolframalpha

def ask_wolframalpha(query):
        app_id = "your_app_id"
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        return answer