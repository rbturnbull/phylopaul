#!/bin/bash

# To give your job a name, replace "MyJob" with an appropriate name
#SBATCH --job-name=1co-lewismk-lognormal-homogeneous

#SBATCH --ntasks=1

#SBATCH -p physical

# set your minimum acceptable walltime=days-hours:minutes:seconds
#SBATCH -t 25:00:00

# Specify your email address to be notified of progress.
#SBATCH --mail-user=robert.turnbull@unimelb.edu.au
#SBATCH --mail-type=ALL

# Load the environment variables
module purge
module load java/11.0.2
# module load foss/2019b
# module load beast/2.6.3

/data/gpfs/projects/punim1224/rob/paul/beast/bin/beast $(ls *.xml)