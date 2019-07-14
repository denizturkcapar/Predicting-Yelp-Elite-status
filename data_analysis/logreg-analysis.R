data <- read.csv("training.csv", header = T)
names(data)[names(data) == "fans"] <- "e"
names(data)[names(data) == "ever_elite"] <- "fans"
names(data)[names(data) == "e"] <- "ever_elite"
data$fans <- as.numeric(as.character(data$fans))
data$yelping_since <- as.Date(data$yelping_since)
data$years_yelping <- (Sys.Date() - data$yelping_since) / 365

data$total_compliments_received <- data$num_hot_compliment + data$num_cool_compliment + data$num_cute_compliment + 
  data$num_funny_compliment + data$num_list_compliment + data$num_note_compliment + data$num_photos_compliment + 
  data$num_profile_compliment + data$num_plain_compliment + data$num_writer_compliment + data$num_more_compliment
data$total_compliments_given <- data$useful + data$funny + data$cool

everything <- glm(ever_elite ~ score + review_count + fans + average_stars + years_yelping + num_hot_compliment + num_more_compliment + 
    num_profile_compliment + num_cute_compliment + num_list_compliment + num_note_compliment + num_plain_compliment + 
    num_cool_compliment + num_funny_compliment + num_writer_compliment + num_photos_compliment + funny + useful + cool,
    family = "binomial", data = data)
kable(tidy(everything))

smaller <- glm(ever_elite ~ score + review_count + fans + average_stars + years_yelping + total_compliments_given +
    total_compliments_received, family = "binomial", data = data)
kable(tidy(smaller))

reduced <- glm(ever_elite ~ review_count + fans + average_stars + total_compliments_given +
                 total_compliments_received, family = "binomial", data = data)



