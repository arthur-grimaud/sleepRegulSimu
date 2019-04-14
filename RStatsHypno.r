###################
# Hypnogram Stats #
###################

#Get arguments from command line
args<-commandArgs()
cat(args,sep="\n") #shows args
typeof(args)
length(args)

#retreive first argument from command line (after default args)
inFile<-args[6]
data1<-read.delim(file=inFile,header=F, dec=".", sep=" ")
head(data1)


#open multiple files
#for(i in 1:(length(args)-5)){
#    data[i,]<-read.delim(file=args[i],header=F, dec=".", sep=" ")
#}


#maybe useful for multiple input files
#idea would be to make a new dataframe to create histograms of means
#and to run ANOVA/posthoc stats on
#need to consider minutes/count conversion
total<-0
NREM<-0
wake<-0
REM<-0

#for (i in 1:(length(args)-5))
for (i in data1){ #data1[i,]
  if (i==0){
    NREM<-NREM+1
  }else if(i==0.5){
    REM<-REM+1
  }else if(i==1){
    wake<-wake+1
  }
  total<-total+1
}

#just to check
cat("New NREM ",NREM,"\n")
cat("New REM ",REM,"\n")
cat("New wake ",wake,"\n")
cat("New total ",total,"\n")

#install.packages("ggplot2")
library(ggplot2)

#list to vector
typeof(data1)
data1Unlist<-unlist(data1, use.names=FALSE)

#plot histogram
pp<-ggplot() + 
  aes(data1Unlist)+ 
  geom_histogram(binwidth=0.5, colour="black", fill="white")

#save plot as png in current working directory
ggsave("test.png", plot = pp, device = NULL, path = NULL,
       scale = 1)