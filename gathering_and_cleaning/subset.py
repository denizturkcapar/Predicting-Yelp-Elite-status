import pandas
import csv
import json

u = open("../cmsc 12300/user.json")
r = open("../cmsc 12300/review.json")

with open("user_file", mode = "w") as csv_file:
    output = csv.writer(csv_file, delimiter = ",")
    for i in range(1637138):
        line = json.loads(u.readline())
        row = []
        for i, val in line.items():
            if i == "elite":
                if len(val) == 0:
                    row.append(0)
                else:
                    row.append(1)
            elif i == "friends":
                row.append(len(val))
            else:
                row.append(" ".join(str(val).split()))
        output.writerow(row)

with open("review_file", mode = "w") as csv_file:
    output = csv.writer(csv_file, delimiter = ",")
    for i in range(6685900):
        line = json.loads(r.readline())
        row = []
        for i, val in line.items():
            val = " ".join(str(val).split())
            val = " ".join(str(val).split(","))
            row.append(val)
        output.writerow(row)

scores = pandas.read_csv("clean_scores_full.csv", header= None, names = ["user_id", "score"])
use = pandas.read_csv("user_file", header = None, names = ["user_id", "name", "review_count", "yelping_since", "friends", "useful", "funny", "ever_elite", "fans", \
    "cool", "average_stars", "num_hot_compliment", "num_more_compliment", "num_profile_compliment", "num_cute_compliment", "num_list_compliment", \
    "num_note_compliment", "num_plain_compliment", "num_cool_compliment", "num_funny_compliment", "num_writer_compliment", "num_photos_compliment"])
merged = use.merge(scores, how = "inner", on = "user_id") 
merged.to_csv("full_dataset", index = False)



