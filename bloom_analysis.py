import numpy as np
import matplotlib.pyplot as plt

# Function to determine the false positive probability based on the variables P, B and h
# Here, P is the number of passwords, B is the size of the bloom filter and h is the number of hash functions
def false_positive_probability(P, B, h):
    return 1 - np.exp((-h*P)/B)

# Function to determine the optimal amount of hash functions based on the number of passwords and the size of the bloom filter. 
# This optimal amount of hash funtions leads to the lowest probability for false positive results.
def optimal_h(P, B):
    return((P/B)*np.log(2))

# The number of hash funtions to use
h = [1,2,3,4,5]

# The sizes of the bloom filters
B = [100000, 200000, 300000, 500000, 1000000]

# The fixed amount of passwords
P = 669879

# Default values used in the plotting
default_B = B[3]
default_h = h[2]

def plot_variable_h(P, default_B, h):
    # List to store the probability of false positives
    fp = []

    for hash in h: 
        fp.append(false_positive_probability(P, default_B, hash))

    # The optimal number of hash functions
    oh = (optimal_h(P, default_B))

    plt.plot(h, fp, label='False positive probability')
    plt.xlabel('Hash functions')
    plt.ylabel('False positive probability')
    plt.title(f'Analys of the Bloom filter with P = {P} and B = {default_B}. \nThe optimal number of hash functions is {np.round(oh, 3)}, which gives a false positive probability of {np.round((false_positive_probability(P, default_B, oh)), 3)}')
    plt.plot([oh], [false_positive_probability(P, default_B, oh)], 'ro', label='Optimal number of hash functions')
    plt.text(oh, (false_positive_probability(P, default_B, oh))+0.01, np.round((false_positive_probability(P, default_B, oh)), 3), ha="center")
    # plt.text(oh*1.05, (false_positive_probability(P, default_B, oh))*1.01, f'Optimal number \nof hash functions')
    plt.legend()
    plt.show()
    return 0

def plot_variable_B(P, B, default_h):
    # List to store the probability of false positives
    fp = []

    # List to store the optimal number of hash functions
    oh = []

    for bits in B:
        # Adding the  
        fp.append(false_positive_probability(P, bits, default_h))

        # Calculating the optimal number of hash functions
        oh.append(optimal_h(P, bits))

    plt.plot(B, fp, label='False positive probability')
    plt.xlabel('Bloom filter size')
    plt.title(f'Analys of the Bloom filter with P = {P} and h = {default_h}. \nAnalyzing the false positive probability with the different bloom filter sizes')
    plt.legend()
    plt.show()
    
    plt.plot(B, oh, 'ro', label='Optimal number of hash funtions')
    plt.xlabel('Bloom filter size')
    plt.title(f'Analys of the Bloom filter with P = {P} and a variable bloom filter size B. \nAnalyzing what the optimal number of hash functions are, based on the bloom filter size B')
    for i, h in enumerate(oh):
      plt.text(B[i], h+0.1, np.round(h,2), ha="center")
    plt.ylim(0,5.5)
    plt.legend()
    plt.show()
    return 0

plot_variable_h(P, default_B, h)
plot_variable_B(P, B, default_h)