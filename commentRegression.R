#Important Libraries
library(plyr)

#Read in the data
data <- read.csv("data.csv");

#Create indicator variables for boolean expressions
topics = c("TrumpTalk", "Russia", "Emails", "China", "Abortion", "Trump", "Hillary", 
           "Obama", "Wall", "Mexico", "Immigration", "Bernie", "Guns", "Healthcare", "Taxes");

for(i in 1:length(topics)){
  data[[topics[i]]] = revalue(data[[topics[i]]], c("false" = 0, "true" = 1));
}

#Let us run some logistic regression models to see if we find any interesting relationships
##Basic regression for comment_length
commentBasic <- lm(data$comment_length ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                      + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                      + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes);
summary(commentBasic);

matplot(coef(summary(commentBasic))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Basic regression for score
scoreBasic <- lm(data$score ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                 + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                 + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes);
summary(scoreBasic);

matplot(coef(summary(scoreBasic))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Basic regression for neu
neuBasic <- lm(data$neu ~ data$TrumpTalk + data$Russia + data$Emails + data$China
               + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
               + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes);
summary(neuBasic);

matplot(coef(summary(neuBasic))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Basic regression for neg
negBasic <- lm(data$neg ~ data$TrumpTalk + data$Russia + data$Emails + data$China
               + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
               + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes);
summary(negBasic);

matplot(coef(summary(negBasic))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Basic regression for pos
posBasic <- lm(data$pos ~ data$TrumpTalk + data$Russia + data$Emails + data$China
               + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
               + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes);
summary(posBasic);

matplot(coef(summary(posBasic))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Basic regression for compound
compBasic <- lm(data$compound ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes);
summary(compBasic);

matplot(coef(summary(compBasic))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

#Run some logistic models with interaction between names

##Interaction regression for comment_length
commentInteract <- lm(data$comment_length ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                      + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                      + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                      + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie);
summary(commentInteract);

matplot(coef(summary(commentInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Interaction regression for score
scoreInteract <- lm(data$score ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                 + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                 + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                 + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie);
summary(scoreInteract);

matplot(coef(summary(scoreInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Interaction regression for neu
neuInteract <- lm(data$neu ~ data$TrumpTalk + data$Russia + data$Emails + data$China
               + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
               + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
               + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie);
summary(neuInteract);

matplot(coef(summary(neuInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Interaction regression for neg
negInteract <- lm(data$neg ~ data$TrumpTalk + data$Russia + data$Emails + data$China
               + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
               + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
               + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie);
summary(negInteract);

matplot(coef(summary(negInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Interaction regression for pos
posInteract <- lm(data$pos ~ data$TrumpTalk + data$Russia + data$Emails + data$China
               + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
               + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
               + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie);
summary(posInteract);

matplot(coef(summary(posInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Interaction regression for compound
compInteract <- lm(data$compound ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie);
summary(compInteract);

matplot(coef(summary(compInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

#Run a final, advanced interaction regression model

##Advanced interaction regression for comment_length
commentAdvInteract <- lm(data$comment_length ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                         + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                         + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                         + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie
                         + data$Russia * data$China + data$TrumpTalk * data$Emails * data$Hillary);
summary(commentAdvInteract);

matplot(coef(summary(commentAdvInteract))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Advanced interaction regression for score
commentAdvScore <- lm(data$score ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                      + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                      + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                      + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie
                      + data$Russia * data$China + data$TrumpTalk * data$Emails * data$Hillary);
summary(commentAdvScore);

matplot(coef(summary(commentAdvScore))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Advanced interaction regression for neu
commentAdvNeu <- lm(data$neu ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                    + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                    + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                    + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie
                    + data$Russia * data$China + data$TrumpTalk * data$Emails * data$Hillary);
summary(commentAdvNeu);

matplot(coef(summary(commentAdvNeu))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Advanced interaction regression for pos
commentAdvPos <- lm(data$pos ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                    + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                    + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                    + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie
                    + data$Russia * data$China + data$TrumpTalk * data$Emails * data$Hillary);
summary(commentAdvPos);

matplot(coef(summary(commentAdvPos))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Advanced interaction regression for neg
commentAdvNeg <- lm(data$neg ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                    + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                    + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                    + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie
                    + data$Russia * data$China + data$TrumpTalk * data$Emails * data$Hillary);
summary(commentAdvNeg);

matplot(coef(summary(commentAdvNeg))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");

##Advanced interaction regression for compound
commentAdvComp <- lm(data$compound ~ data$TrumpTalk + data$Russia + data$Emails + data$China
                    + data$Abortion + data$Hillary + data$Obama + data$Wall + data$Mexico
                    + data$Immigration + data$Bernie + data$Guns + data$Healthcare + data$Taxes
                    + data$TrumpTalk * data$Hillary * data$Obama * data$Bernie
                    + data$Russia * data$China + data$TrumpTalk * data$Emails * data$Hillary);
summary(commentAdvComp);

matplot(coef(summary(commentAdvComp))[,1], type = c("b"), pch = 1, ylab = "Coefficent",
        xlab = "Which Coefficent", main = "Coefficents Visualized", col = "blue");
