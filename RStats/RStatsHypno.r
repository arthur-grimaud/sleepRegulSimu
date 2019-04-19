###################
# Hypnogram Stats #
###################

#Launch from launchR.py

#Saves plots.png, 3 stats.txt


### Importing and formatting data ###

#Get arguments from command line: .txt files to read
args<-commandArgs()
#cat(args,sep="\n")
#length(args)

# testing without passing through python
# data1<-read.delim(file="testdata.txt",header=F, dec=".", sep="\n")
# data2<-read.delim(file="testdata2.txt",header=F, dec=".", sep="\n")
# data<-list()
# data<-append(data,data1)
# data<-append(data,data2)

#open multiple files from command line
data<-list()

for(i in 1:(length(args))){
#retreive first argument from command line (after default args) args[6] and beyond
  if (i>5){ 
    temp<-read.delim(file=args[i],header=F, dec=".", sep="\n")
    data<-append(data,temp)
  }
}
data

#Counting time, bouts, bout duration
#need to consider minutes/count conversion

# %Time spent in each state
total<-0
NREM<-0
wake<-0
REM<-0
totals<-data.frame(matrix(nrow=length(data), ncol=4))
names(totals) <- c("NREM", "REM", "wake","total")

# Number of bouts per state
boutNREM<-0
boutwake<-0
boutREM<-0
bouts<-data.frame(matrix(nrow=length(data),ncol=3))
names(bouts)<- c("NREM", "REM", "wake")

# Time in each bout
timeNREM<-0
timeNREMList<-list()
timewake<-0
timewakeList<-list()
timeREM<-0
timeREMList<-list()

timeInBouts<-list() #to combine NREM,REM,wake

#One big loop counts for each 

for (i in 1:(length(data))){ #for every input file
  for (j in 1:(length(data[[i]]))){ #for every line in a file
    
    #NREM
    if (data[[i]][j] == 0){  #0 corresponds to NREM 
      NREM<-NREM+1 #NREM count
      if (j<length(data[[i]]) && data[[i]][j+1] != data[[i]][j]) { #tests for change in state
        boutNREM<-boutNREM+1 #change in state marks the end of a bout
        timeNREM<-timeNREM+1 #to count first bout occurance
        timeNREMList<-rbind(timeNREMList,timeNREM) #time in bout pushed to list
        timeNREM<-0 #time in bout reset since the state is changed
      }else{
          timeNREM<-timeNREM+1 #no change in state means staying in bout
      }
    #REM
    }else if(data[[i]][j] == 0.5){
      REM<-REM+1
      if (j<length(data[[i]]) && data[[i]][j+1] != data[[i]][j]) { 
        boutREM<-boutREM+1
        timeREM<-timeREM+1 
        timeREMList<-rbind(timeREMList,timeREM)
        timeREM<-0
      }else{
        timeREM<-timeREM+1
      }
    #WAKE  
    }else{
      wake<-wake+1
      if (j<length(data[[i]]) && data[[i]][j+1] != data[[i]][j]) { 
        boutwake<-boutwake+1 
        timewake<-timewake+1 
        timewakeList<-rbind(timewakeList,timewake)
        timewake<-0
      }else{
        timewake<-timewake+1
      }
    }
    total<-total+1
  }
  
  #make df for %time spent and bouts
  totals[i,]<-cbind(NREM,REM,wake,total)
  bouts[i,]<-cbind(boutNREM,boutREM,boutwake)
  
  #reset for next data input
  total<-0
  NREM<-0
  wake<-0
  REM<-0
  
  boutNREM<-0
  boutwake<-0
  boutREM<-0
}

# Since time in bouts are not of equal length, lists are used to first store the data
# The lists are then converted to a dataframe

#Data frames must have columns of the name length
n<-max(length(timeNREMList),length(timeREMList),length(timewakeList),check.names=FALSE)
length(timeNREMList)<-n
length(timeREMList)<-n
length(timewakeList)<-n
#Add all of the data together
timeInBouts<-cbind(timeNREMList,timeREMList,timewakeList)

#Create dataframe from timeInBouts list
boutDurDF<-as.data.frame(timeInBouts)
names(boutDurDF)<-c("NREM","REM","wake")
#Replace "Null" with NA and make data numeric for futher processing
boutDurDF[boutDurDF == "NULL"] <- NA
boutDurDF$NREM = as.numeric(boutDurDF$NREM)
boutDurDF$REM = as.numeric(boutDurDF$REM)
boutDurDF$wake = as.numeric(boutDurDF$wake)


### Statistics ###

# %Time
#ANOVA
ATotals<-totals[,c(1:3)] #Excluding total count
ATotals<-stack(ATotals)
resTotals<-aov( values ~ ind, ATotals)
timeAnova<-summary(resTotals)
#Post-Hoc
timeTukey<-TukeyHSD(resTotals)
#Save
capture.output(timeAnova,timeTukey, file="timeStats.txt")

# Number of bouts
#ANOVA
ABouts<-stack(bouts)
resBouts<-aov( values ~ ind, ABouts)
boutsAnova<-summary(resBouts)
#Post-Hoc
boutsTukey<-TukeyHSD(resBouts)
#Save
capture.output(boutsAnova,boutsTukey, file="boutsStats.txt")

# Time in bouts
#ANOVA
ABoutDur<-stack(boutDurDF)
resBoutDur<-aov( values ~ ind, ABoutDur)
boutDurAnova<-summary(resBoutDur)
#Post-Hoc
boutDurTukey<-TukeyHSD(resBoutDur)
#Save
capture.output(boutDurAnova,boutDurTukey, file="boutDurStats.txt")

### Standard Deviation ###

# % Time
totalMeans<-colMeans(totals)
percent<-totalMeans[1:3]/totalMeans[4]*100
totalMeans<-cbind(totalMeans[1:3],percent)
totalMeans<-data.frame(totalMeans)
totalMeans[,3]<-rbind("NREM","REM","wake")

#Convert means to percentages to calculate SD of %
for(i in 1:3){ #NREM,REM,wake
  for(j in 1:length(totals[[1]]))
    totals[[i]][j]=totals[[i]][j]/totals[[4]][j]*100
}

totalsSD<-sapply(totals[1:3], sd, na.rm = TRUE)
totalsSD<-cbind(totalsSD,totalMeans)
names(totalsSD)<-cbind("SD","mean","percent","state")


# Number of bouts
boutMeans<-colMeans(bouts)
boutMeans<-data.frame(boutMeans)
boutMeans[,2]<-rbind("NREM","REM","wake")
boutsSD<-sapply(bouts, sd, na.rm = TRUE)

boutsSD<-cbind(boutsSD,boutMeans)
names(boutsSD)<-cbind("SD","mean","state")

# Duration of bouts
btMeans<-colMeans(boutDurDF,na.rm=TRUE)
btMeans<-data.frame(btMeans)
btMeans[,2]<-rbind("NREM","REM","wake")
#CONVERSION TO MINUTES

boutDurSD<-sapply(boutDurDF, sd, na.rm = TRUE)
boutDurSD<-cbind(boutDurSD,btMeans)
names(boutDurSD)<-cbind("SD","mean","state")

### Barplots ###

#install.packages("ggplot2")
library(ggplot2)

# %Time

pp<-ggplot(data=totalsSD, aes(x=state, y=percent)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=percent-SD, ymax=percent+SD), width=.2,position=position_dodge(.9)) +
  labs(x="", y="Percent time in each state")

# number of bouts

pp2<-ggplot(data=boutsSD, aes(x=state, y=mean)) +
  geom_bar(stat="identity")+
  geom_errorbar(aes(ymin=mean-SD, ymax=mean+SD), width=.2,position=position_dodge(.9)) +
  labs(x="", y="Number of bouts")

# time in bout

pp3<-ggplot(data=boutDurSD, aes(x=state, y=mean)) +
  geom_bar(stat="identity")+
  geom_errorbar(aes(ymin=mean-SD, ymax=mean+SD), width=.2,position=position_dodge(.9)) +
  labs(x="", y="Mean bout duration (min)")


#Save plots
#install.packages("gridExtra")
require(gridExtra)

plots<-grid.arrange(pp, pp2, pp3, ncol=3)
ggsave("plotStats.png", plot = plots, device = NULL, path = NULL,
       scale = 1)






