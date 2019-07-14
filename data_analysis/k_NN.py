from mrjob.job import MRJob
import queue

K = 15

def compute_similarity(user_data, other_user_data):
    '''
    A formula for computing the similarity of two users in a dataset. Does a
    root transform for variables with large ranges, and weights each variable
    based on statistical significance.

    Inputs:
        user_data: (list) A list containing column values for a row of data in the
          dataset corresponding to a Yelp user.
        other_user_data: (list) A list containing column values for a row of data 
          in the dataset, for another Yelp user.
    '''

    indices = [3, 5, 9, 11, 23, 24, 25, 26]

    user = [float(user_data[i]) for i in indices]
    other_user = [float(other_user_data[i]) for i in indices]

    review_count = 1 - ((abs(user[0] - other_user[0]) ** (1/2)) / 116)
    friends = 1 - ((abs(user[1] - other_user[1]) ** (1/3)) / 53.65)
    fans = 1 - ((abs(user[2] - other_user[2]) ** (1/4)) / 24.50)
    avg_stars = 1 - (abs(user[3] - other_user[3]) / 4)
    score = 1 - (abs(user[4] - other_user[4]) / 120.78)
    yrs_yelping = 1 - (abs(user[5] - other_user[5]) / 14.10)
    tot_comps_given = 1 - ((abs(user[6] - other_user[6]) ** (1/3)) / 65.40)
    tot_comps_recvd = 1 - ((abs(user[7] - other_user[7]) ** (1/3)) / 65.20)

    similarity = 0.35 * review_count + 0.125 * friends + 0.125 * fans + \
    0.125 * avg_stars + 0.125 * score + 0.05 * yrs_yelping + \
    0.07 * tot_comps_given + 0.03 * tot_comps_recvd

    return similarity


class K_NN(MRJob):
    '''
    A MapReduce class finding the k nearest-neighbors of a datapoint, and
    using those nearest negihbors to predict if the datapoint should be an 
    elite user or not.
    '''

    def mapper_init(self):
        copy = open("full_dataset_final.csv")
        self.lines = copy.readlines()



    def mapper(self, _, line):
        '''
        Splits a CSV by line/user and calculates the similarity between the 
        current user and every other user in the CSV.
        
        Inputs:
            _: arbitrary
            line: a line of a CSV file corresponding to a user

        Yields:
            key: user id + elite status, value: tuple of (similarity score, 
              other user id + elite status)
        '''

        row = line.split(",")
        user_id = row[1]
        user_elite = row[7]   
        user = user_id + " " + user_elite

        for other_row in self.lines:
            other_row = other_row.split(",")
            other_user_id = other_row[1]
            if (user_id != other_user_id) & (user_id != '4ehyeebKp5S8ANk2RTV_AQ'):
                other_elite = other_row[7]
                other_user = other_user_id + " " + other_elite
                similarity = compute_similarity(row, other_row)
                comparison = (similarity, other_user)
                yield user, comparison


    def reducer_init(self):
        '''
        Initializes a PriorityQueue for the reducer.
        '''

        self.queue = queue.PriorityQueue(maxsize=K)


    def reducer(self, user, others):
        '''
        Predicts if a user is elite or not, based off of the elite status of
          the k nearest-neighbors of the user.

        Inputs:
            user: (str) user_id + elite status
            others: a generator containing tuples of (similarity score, other 
              user id + elite status)"

        Yields:
            key: user, value: user's actual vs. predicted elite status, as str
        '''
        
        # Uses a priorityQueue to determine the k nearest neighbors
        other_users = list(others)
        for other in other_users:
            if self.queue.full():
                least_similar_user = self.queue.get()
                if other[0] > least_similar_user[0]:
                    self.queue.put(other)
                else:
                    self.queue.put(least_similar_user)
            else:
                self.queue.put(other)

        # Determines the proportion of elite users among nearest neighbors
        user_elite_actual = user[-1]   # assuming user is a string, get elite number
        other_elite_count = 0
        for other in self.queue.queue:
            other_elite = other[1][-1] # assuming user is a string, get elite number
            other_elite = int(other_elite)
            other_elite_count += other_elite
        elite_avg = other_elite_count / K

        # Determines elite status of the user based off of nearest neighbors
        if elite_avg >= 0.5:       # play around with this? 0.5 is a 1, 0, or coin flip?
            user_elite_predicted = "1"
        else:
            user_elite_predicted = "0"
        if user_elite_actual == user_elite_predicted:
            yield user_elite_actual * 2, 1
        else:
            if user_elite_actual == "0":
                yield user_elite_actual + str(abs(int(user_elite_actual) - 1)), 1

    

if __name__ == '__main__':
    K_NN.run()