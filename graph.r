library(tidyverse)

data2 <- read_csv("data_2.csv")
names(data2) <- c("Row", "Sample", "Trait", "Value", "Label", "Timestamp")

areas2 <- subset(data2, Trait == "area")
areas2$Timestamp <- as.Date(areas2$Timestamp, format="%Y-%m-%d %H:%M:%S")
areas2$Value <- as.numeric(areas2$Value)
areas2_pure <- filter(areas2, !is.na(Timestamp))
areas2_pp <- filter(areas2, areas2$Value < 5000)

f <- ggplot(areas2_pp, aes(Timestamp, Value, color=factor(Sample), group=factor(Sample))) + geom_point() + geom_smooth() + theme_bw() +
            labs(x = "Day", y = "Area", title = "Trial #1: Leaf Surface Area over Time")

data3a <- read_csv("data_3a.csv")
names(data3a) <- c("Row", "Sample", "Trait", "Value", "Label", "Timestamp")

areas3a <- subset(data3a, Trait == "area")
areas3a$Timestamp <- as.Date(areas3a$Timestamp, format="%Y-%m-%d %H:%M:%S")
areas3a$Value <- as.numeric(areas3a$Value)
areas3a_pure <- filter(areas3a, !is.na(Timestamp))

data3b <- read_csv("data_3b.csv")
names(data3b) <- c("Row", "Sample", "Trait", "Value", "Label", "Timestamp")

areas3b <- subset(data3b, Trait == "area")
areas3b$Timestamp <- as.Date(areas3b$Timestamp, format="%Y-%m-%d %H:%M:%S")
areas3b$Value <- as.numeric(areas3b$Value)
areas3b_pure <- filter(areas3b, !is.na(Timestamp))

areas3 <- rbind(areas3a_pure, areas3b_pure)

g <- ggplot(areas3, aes(Timestamp, Value, color=factor(Sample), group=factor(Sample))) + geom_point() + geom_smooth() + theme_bw() + 
            labs(x = "Day", y = "Area", title = "Trial #2: Leaf Surface Area over Time")