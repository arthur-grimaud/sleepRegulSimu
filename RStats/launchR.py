###############
# Launching R #
###############
import os

script= "Rscript RStatsHypno_C.r"

#interface to enter files?
arg1="testdata.txt" #make sure there is a newline at the end
arg2="testdata2.txt" #another text file

#for loop to concatenate as many files as entered?
run = script + " " + arg1 + " " + arg2

#Call command line to run Rscript
os.system(run)

