from mrjob.job import MRJob
import re
import textstat

data = open('temporary.csv', 'w')


class Flesch_Reading_Analysis(MRJob):

    def mapper(self, _, line):

        cols = line.split(',')
        user = cols[1]
        text = cols[7]
        yield user, text

    def reducer(self, user, reviews):

        OUTPUT_PROTOCOL = CsvProtocol

        reviews = ' '.join(reviews)
        metric = textstat.flesch_reading_ease(reviews)
        writed = user + ', ' + str(metric) + '\n'
        data.write(writed)
        yield user, metric

def csv_cleaner(csv_file):

    file = open(csv_file, 'r')
    lines = file.readlines()
    file.close()
    really_new = open('clean_scores_full.csv', 'w')
     
    for line in lines:
        user_id = re.search(r'[-?]*([\d|\w|_|-]+)', line).groups(0)[0]
        score = re.search(r'(-?[\d]+[.][\d]+)', line).groups(0)[0]
        new_line = user_id + ', ' + score + '\n'
        really_new.write(new_line)
        

if __name__ == '__main__':
  Flesch_Reading_Analysis.run()
  data = data.close()
  data = '/home/student/CS-123-Final/temporary.csv'
  csv_cleaner(test)
