from mrjob.job import MRJob
import math
import datetime
from dateutil.parser import parse

TODAY = datetime.datetime(2019, 5, 30)

class Predictions(MRJob):

    def mapper(self, _, line):

        line = line.split("|")

        rvw_count, friends, ever_elite = float(line[0]), float(line[2]), str(line[5])
        fans, avg_stars, score = float(line[6]), float(line[8]), float(line[20])

        tot_received = 0
        for i in range(9,20):
            tot_received += float(line[i])

        tot_given = 0
        for i in [3, 4, 7]:
            tot_given += float(line[i])

        yrs_yelping = ((TODAY - parse(line[1])).days) / 365

        coefs = {"score": -0.0185642, "intercept": -4.1184859, \
        "review_count": 0.0236431, "fans": 0.0000776, \
        "average_stars": 0.4126102, "years_yelping": -0.0171222, \
        "total_compliments_given": -0.0019019, \
        "total_compliments_received": 0.0005216, "friends": 0.0056643}

        if score != "score":
            pred = coefs["intercept"] + coefs["score"] * score + \
            coefs["review_count"] * rvw_count + coefs["fans"] * fans + \
            coefs["average_stars"] * avg_stars + coefs["years_yelping"] * yrs_yelping + \
            coefs["total_compliments_received"] * tot_received + \
            coefs["total_compliments_given"] * tot_given + coefs["friends"] * friends

            pred = (math.exp(pred))/(1 + math.exp(pred))

            if pred >= 0.50:
                estimated = "1"
            else:
                estimated = "0"

            yield ever_elite + estimated, 1


    def combiner(self, name, counts):

        yield name, sum(counts)


    def reducer(self, name, counts):

        yield name, sum(counts)


if __name__ == "__main__":
    Predictions.run()

