import json

def AddRating(id, rating):
    f = open("ratings.json", "r")
    a = json.load(f)
    j = 0
    for i in a:
        if int(i["id"]) == int(id):
            x = a[j]["ratings"]
            x.append(rating)
            a[j]["ratings"] = x
            with open("ratings.json", "w") as wf:
                json.dump(a, wf, sort_keys=True, indent=4)
                wf.close()
                return
        j+=1

    data = {"id": id, "ratings":[rating]}
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

def AddComment(id, comment):
    file = open("ratings.json", "r")
    json_data = json.load(file)
    i = 0
    for object in json_data:
        if(int(object["id"])) == id:
            tcomments = object[i]["comments"]
            tcomments.append(comment)
            json_data[i]["comments"] = tcomments
            with open("ratings.json", "w") as wf:
                json.dump(json_data, wf, sort_keys=True, indent= 4)
                wf.close()
                return


def Test(idk):
    f = open("ratings.json", "r")

print(ReadRating(1964))