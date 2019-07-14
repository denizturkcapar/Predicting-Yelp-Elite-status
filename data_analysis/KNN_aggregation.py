from mrjob.job import MRJob
import math
import re

class KNN_aggregator(MRJob):

    def mapper(self, _, line):

        line = line.split("\t")
        score = line[1]
        score = re.search(r"(\d{2})", score).group(0)
        yield score, 1


    def combiner(self, name, counts):

        yield name, sum(counts)


    def reducer(self, name, counts):

        yield name, sum(counts)


if __name__ == "__main__":
    KNN_aggregator.run()