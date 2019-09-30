import os
import argparse
import time
import string
import numpy as np
import re
import logging
from matplotlib import pyplot as plt


_description = 'Measure the releative frequencies of letters in a text file'

def process(file_path):
    logging.info('Opening file %s...',args.input)
    with open(args.input,'r') as file_input:
        f = file_input.read()
        f = f.lower()
    logging.info('Done.')

    # Optional skip of preamble and licence
    if args.skip != None:
        logging.info('Skipping the preamble...')
        id = re.compile('\*\*\*')
        logging.debug('ID preamble-end: %s',f[id.search(f).start():id.search(f,id.search(f).end()).end()])
        preamble_end = id.search(f,id.search(f).end()).end()
        f = f[preamble_end:]              # skip preamble
        logging.info('Done.')
        logging.info('Skipping the licence...')
        logging.debug('Skip licence: %s',f[id.search(f,preamble_end).start():])
        f = f[:id.search(f,preamble_end).start()]                 # skip licence
        logging.info('Done.')

    # Prepare a dictionary to hold the letter frequencies, and initialize
    # all the counts to zero.
    alphabet = string.ascii_lowercase
    letter = {str(i) : 0 for i in alphabet}
    logging.debug('Dict letter: %s',letter)
   
    # Loop over the input data
    for i in f:
        if i in letter:
            letter[i] += 1

    # Prepare the arrays for the printing
    x = np.arange(0,len(letter))
    y = np.array([*letter.values()])
    y = y/y.sum()
    x_tick= [*letter.keys()]  # keys-array in the correct order

    # Print the final output
    print('Relative frequence of each letter of the alphabet: \n')
    for i,j in zip (x_tick,y):
        print(f'{i}: {j}')



    # Optional display of the frequences' histogram
    if args.histogram != None:
        logging.info('Displaying the frequences\' histogram')
        plt.title('Bar plot of the frequences')
        plt.bar(x,y,tick_label=x_tick)
        plt.ylabel('Relative frequences')
        plt.show()
        logging.info('Done.')

    # Optional print of the statistic
    if args.statistic != None:
        logging.info('Printing the basic statistic...')
        n_chars = len(f)
        n_words = len(f.split())
        end_line = re.compile('\\n')
        n_lines = len(end_line.findall(f))
        print('Number of characters: {}, Number of words: {}, Number of lines:{} '.format(n_chars,n_words,n_lines))
        logging.info('Done')

    logging.info('Process function terminated.')



if __name__ == '__main__':
    start = time.process_time()
    
    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument('-i', '--input', required=True, help= 'path to the input file')
    parser.add_argument('-hist','--histogram',help= 'Optional histogram of the frequencies: digit yes   if you want')
    parser.add_argument('-s','--skip',help='Digit skip if you want to skip preamble and licence')
    parser.add_argument('-stat','--statistic',help='Digit yes if you want basic statistic')
    parser.add_argument('-log','--logging_level', default='INFO',help='You can change the logging severity level')
    args=parser.parse_args()
    
    logging.basicConfig(level=args.logging_level.upper())
    logging.info('The severity level requested for the logging is set...')
    
    process(args.input)
    
    print('Total elapsed time: {} s'.format(time.process_time()-start))

