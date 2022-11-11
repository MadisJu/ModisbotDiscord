import CatGirlRating


class CatGirl:
    id
    ratings = []
    comments = []

    def __init__(self, id, comments, ratings):
        self.id = id
        self.ratings = ratings
        self.comments = comments

    def __init__(self, id):
        self.id = id
        data = CatGirlRating.ReadRating(self.id)
        if not(data == None):
            if "ratings" in data.keys():
                self.ratings = data["ratings"]
            if "comments" in data.keys():
                self.comments = data["comments"]


    def AvgRating(self):
        if len(self.ratings) == 0:
            return 0
        return sum(self.ratings)/len(self.ratings)

