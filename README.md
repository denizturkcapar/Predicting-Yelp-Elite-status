# Roadmap to our Programs

## Data Gathering & Cleaning:

* mapreduced_rdg_level.py – iterates through the reviews dataset and assigns each review a Flesch Reading Ease score, 
which is used in building our logistic regression and KNN programs
* subset.py – a utility program that was used to work first with subsets of our data to merge them (users and reviews)
and at one point was adapted to also merge the full sized datasets
* process_rawdata.py – a final tweaking of our full dataset that aggregates certain columns that describe users

## Data Analysis:

* correct_guesses.py – a MapReduce program that aggregates the results of the logistic regression model by comparing 
incorrect and correct predictions of the model in relation to the actual elite status of each user
* distance_calc.py – a program that was used to help us develop the distance formula that we use in our K-Nearest 
Neighbor program
* k_NN.py – a MapReduce program that finds the K-Nearest Neighbor of each user
* test.py – a tentative program that will aggregate the results of KNN
* logreg-analysis.R/Rmd/pdf - R code that builds the logistic regression model 

## Data Used

* training_dataset150000.csv: 150,000k subset of data used to train the logistic regression model
* testing_dataset_for_mapreduce: the non-150,000k users used to test the logistic regression model used in correctguesses.py
* Other files used for analysis were too large for git and were kept on our machines
