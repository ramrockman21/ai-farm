import json

def search_dataset(crop, question):
    try:
        with open('data/agri_data.json') as f:
            data = json.load(f)

        for item in data:
            if item["crop"].lower() in crop.lower() and item["problem"] in question.lower():
                return item["solution"]

    except:
        return None

    return None