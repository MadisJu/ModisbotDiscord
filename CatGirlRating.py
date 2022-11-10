import json

def AddRating(id, rating):
    f = open("ratings.json", "r")
    a = json.load(f)
    j = 0
    for i in a:
        if int(i["id"]) == int(id):

            print(a[j])
            x = a[j]["ratings"]
            x.append(rating)
            a[j]["ratings"] = x
            with open("ratings.json", "w") as wf:
                json.dump(a, wf, sort_keys=True, indent=4)
                wf.close()
                return
        j+=1

    data = {"id": id, "rating":[rating]}
    a.append(data)
    with open("ratings.json", "w") as wf:
        json.dump(a, wf, sort_keys=True, indent=4)
        wf.close()
        return

def ReadRating(id):
    f = open("ratings.json", "r")
    json_data = json.load(f)
    j = 0
    for i in json_data:
        if int(i["id"]) == int(id):
            return json_data[j]
        j+=1
    return None


def Test(idk):
    f = open("ratings.json", "r")

print(ReadRating(1964))