# CircleFinder

## Description
Bioinspired algorithm to find the maximum radius of a circus which can be placed into a grid with fixed smaller circles.
The problem can be found at the endo of the following tutorial: http://www.ai-junkie.com/ga/intro/gat1.html

## Technique
* The algorithm chosen is a genetic algorithm.
* The individuals are defined based on the binary representation of their coordinates in the grid, generated with Tkinter, a framework for developing interfaces in python.
* The fitness function of an individual is defined as the maximum radius which can be obtained choosing this individual as the center of a circunference (assuming it will at most tangentiate borders or fixed circles).
* The first generations is random and the following ones are defined based on the current, with a probability of choosing an individual being proportional to their fitness.
* Adopted constants:
  1. *Crossover rate:* 0.700
  2. *Mutation rate:* 0.001
  3. *Generation size:* 100

## Usage
* The project was developed using idle3, so this tool is required for running. No other dependencies are needed.
