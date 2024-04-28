import sys
import os 
import argparse 

parser=argparse.ArgumentParser()
parser.add_argument("-generate", action="store_true" , help="Generate random graph")
parser.add_argument("-user-provided", action="store_true" , help="Generate graph from user input")

