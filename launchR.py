###############
# Launching R #
###############
import os

script= "Rscript rstats_hypno.r"

#interface to enter files?
arg1="testdata.txt" #make sure there is a newline at the end
arg2="arg2" #another text file

#for loop to concatenate as many files as entered?
run = script + " " + arg1 + " " + arg2

#Call command line to run Rscript
os.system(run)

