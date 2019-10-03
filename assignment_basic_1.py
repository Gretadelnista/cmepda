import argparse
import time
import string
import logging
import re
import numpy as np
from matplotlib import pyplot as plt


_DESCRIPTION = 'Measure the releative frequencies of letters in a text file'

def process(file_path):
    logging.info('Opening file %s...', file_path)
    with open(file_path, 'r') as file_input:
        text = file_input.read()
        text = text.lower()
    logging.info('Done.')

    # Optional skip of preamble and licence
    if args.skip == True:
        logging.info('Skipping the preamble...')
        id_ = re.compile('\*\*\*')
        logging.debug('id_ preamble-end: %s', \
                      text[id_.search(text).start():id_.search(text, id_.search(text).end()).end()])
        preamble_end = id_.search(text, id_.search(text).end()).end()
        text = text[preamble_end:]              # skip preamble
        logging.info('Done.')
        logging.info('Skipping the licence...')
        logging.debug('Skip licence: %s', text[id_.search(text, preamble_end).start():])
        text = text[:id_.search(text, preamble_end).start()]                 # skip licence
        logging.info('Done.')

    # Prepare a dictionary to hold the letter frequencies, and initialize
    # all the counts to zero.
    alphabet = string.ascii_lowercase
    letter = {str(i) : 0 for i in alphabet}
    logging.debug('Dict letter: %s', letter)
    # Loop over the input data
    for i in text:
        if i in letter:
            letter[i] += 1

    # Prepare the arrays for the printing
    x = np.arange(0, len(letter))
    y = np.array([*letter.values()])
    y = y/y.sum()
    x_tick = [*letter.keys()]  # keys-array in the correct order

    # Print the final output
    print('Relative frequence of each letter of the alphabet: \n')
    for i, j in zip(x_tick, y):
        print(f'{i}: {j}')



    # Optional display of the frequences' histogram
    if args.histogram == True:
        logging.info('Displaying the frequences\' histogram')
        plt.title('Bar plot of the frequences')
        plt.bar(x, y, tick_label=x_tick)
        plt.ylabel('Relative frequences')
        plt.show()
        logging.info('Done.')

    # Optional print of the statistic
    if args.statistic == True:
        logging.info('Printing the basic statistic...')
        n_chars = len(text)
        n_words = len(text.split())
        end_line = re.compile('\\n')
        n_lines = len(end_line.findall(text))
        print('Number of characters: {}, Number of words: {}, Number of lines:{} ' \
              .format(n_chars, n_words, n_lines))
        logging.info('Done')

    logging.info('Process function terminated.')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    parser.add_argument('input', help='path to the input file')
    parser.add_argument('-H', '--histogram', action='store_true', \
                        help='Optional histogram of the frequencies')
    parser.add_argument('-s', '--skip', action='store_true', \
                        help='Optional skip preamble and licence')
    parser.add_argument('-S', '--statistic', action='store_true',  \
                        help='Optional basic statistic')
    parser.add_argument('-l', '--logging_level', default='INFO', \
                        help='You can change the logging severity level')
    args = parser.parse_args()
    logging.basicConfig(level=args.logging_level.upper())
    logging.info('The severity level requested for the logging is set...')
    start = time.process_time()
    process(args.input)
    print('Total elapsed time: {} s'.format(time.process_time()-start))
