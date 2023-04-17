# This is the code for the Bloom Filter project of TDT4305

import configparser  # for reading the parameters file
from pathlib import Path  # for paths of files
import time  # for timing
import numpy as np
import random

# Global parameters
parameter_file = 'default_parameters.ini'  # the main parameters file
# the main path were all the data directories are
data_main_directory = Path('data')
# dictionary that holds the input parameters, key = parameter name, value = value
parameters_dictionary = dict()


# DO NOT CHANGE THIS METHOD
# Reads the parameters of the project from the parameter file 'file'
# and stores them to the parameter dictionary 'parameters_dictionary'
def read_parameters():
    config = configparser.ConfigParser()
    config.read(parameter_file)
    for section in config.sections():
        for key in config[section]:
            if key == 'data':
                parameters_dictionary[key] = config[section][key]
            else:
                parameters_dictionary[key] = int(config[section][key])


# TASK 2
def bloom_filter(new_pass):

    # The indices from the hash functions of the password
    hash_indices = hash_functions(new_pass)

    # Updating the global bit-array B of size N, so that the indices from the hash functions
    # of the password are 1
    for elem in hash_indices:
        global B
        B[elem] = 1

    return 0


# DO NOT CHANGE THIS METHOD
# Reads all the passwords one by one simulating a stream and calls the method bloom_filter(new_password)
# for each password read
def read_data(file):
    time_sum = 0
    pass_read = 0
    with file.open() as f:
        for line in f:
            pass_read += 1
            new_password = line[:-3]
            ts = time.time()
            bloom_filter(new_password)
            te = time.time()
            time_sum += te - ts

    return pass_read, time_sum


# Helper task to select a list of p unique prime numbers. Limited to 14 prime numbers.
def list_of_primes(p):

    # Setting the seed, as to have consistency in the hash funtions
    random.seed(12)

    # The number of which i collect the prime numbers. So the highest possible prime number is n
    n = 100

    # Method for finding an array of prime numbers.
    # Sourced online, but verified the results as consistent and correct.
    s = np.arange(3, n, 2)
    for m in range(3, int(n ** 0.5)+1, 2):
        if s[(m-3)//2]:
            s[(m*m-3)//2::m] = 0
            np.r_[2, s[s > 0]]

    # Returning a radom sample containg p prime numbers from the first 14 prime numbers
    return random.sample(list(s[s != 0]), p)

# TASK 1
# Created h number of hash functions


def hash_functions(password):

    # The number of hash functions
    h = parameters_dictionary['h']

    # The indices for the bit-array B selected by the hash functions of the passwords
    hash_indices = []

    # The size of the bloom filter
    N = parameters_dictionary['n']

    # The list of prime numbers used for the hash funtions
    p = list_of_primes(h)

    # ord() returns the Unicode code point for a one-character string (e.g. "a" -> 97)
    s = [ord(c) for c in password]  # Convert the password to a list of numbers

    # Calculating the indices for the password, that is used in the bit-array B
    for i in range(h):
        sums = 0
        for j in range(0, len(s)):
            sums += (s[j] * (p[i] ** j))
        hash_indices.append(sums % N)

    # Returning the list of hash indices
    return hash_indices


if __name__ == '__main__':

    # Reading the parameters
    read_parameters()

    # Creating the hash functions
    # hash_functions()

    # The size of the bloom filter
    size = parameters_dictionary['n']

    # Creating the bit-array B
    B = np.zeros(size)

    # Reading the data
    print("Stream reading...")
    data_file = (data_main_directory /
                 parameters_dictionary['data']).with_suffix('.csv')
    passwords_read, times_sum = read_data(data_file)
    print(passwords_read, "passwords were read and processed in average", times_sum / passwords_read,
          "sec per password\n")
    # print("Number of zeros in bit-array is", len(B[B == 0]))
    # print("Number of ones in bit-array is", len(B[B == 1]))

    passwords_not_in_passwords_csv_file = ['07886819', '0EDABE59B', '0BFE0815B', '01058686E', '09DFB6D3F', '0F493202C', '0CA5E8F91', '0C13EC1D9', '05EF96537', '03948BA8F', '0D19FB394', '0BF3BD96C', '0D3665974', '0BBDF91E9', '0A6083B64', '0D76EF8EC', '096CD1830', '04000DE73', '025C442BA', '0FD6CAA0A', '06CC18905', '0998DDE00', '02BAACDC4', '0D58264FC', '0CB8911AA', '0CF9E0BDC', '007B7F82F', '0948FD17A', '058BB08DB', '02EDBE8CA', '0D6F02EFD', '09C9797FB', '0F8CB3DA5', '0C2825430', '038BE7E61', '03F69C0F5', '07EB08903', '0917C741D', '0D01FEE8F', '01B09A600', '0BD197525', '06B6A2E60', '0B72DEF61', '095B17373', '0B6E0EEB1', '0078B3053', '08BD9D53F', '01995361F', '0F0B50CAE',
                                           '0B5D2887E', '004EB658C', '0D2C77EDB', '07221E24D', '0E8A4CC90', '00E947367', '0DBE190BB', '0D8726592', '06C02D59D', '0462B8BC6', '0F85122F8', '0FA1961EB', '035230553', '04CDFB216', '0356DB0AD', '0FD947DA3', '053BB206F', '0D1772CC1', '00DB759F5', '072FB4E7A', '0B47CB62D', '0616B627F', '0F3E153BC', '0F3AC7DEE', '01286192B', '009F3C478', '07D89E83E', '007CAFDE6', '0ABC9E80B', '091D1CDA5', '0BFC208A1', '0957D4C84', '00AAF260A', '09CF00D7C', '0D1C66C72', '0EA20CA23', '07D6BE324', '05B264527', '0D48C41F6', '081E31BF5', '0A1DC7455', '07BB493D8', '050036F1B', '00E73A1EC', '0C2D93CC0', '0FF47B30C', '0313062DE', '0E1BEFA3F', '0A24D069F', '02A984386', '0367F7405']

    false_positives = 0

    for pw in passwords_not_in_passwords_csv_file:
        pw_in_set = True
        test_indices = hash_functions(pw)
        for i in test_indices:
            if B[i] == 0:
                pw_in_set = False
        if pw_in_set:
            false_positives += 1

    print('There are', false_positives, 'false positives')
