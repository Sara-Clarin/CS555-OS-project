import random
import argparse

'''
* Test script for AES encryption project for CS555L
* Generates a text file of size (bytes) populated with common english words for testing
*
'''

# List of common English words in varying byte sizes
# Length: 106
words_eightb = ["Academic", "Baseball", "Concrete", "Accepted", "Bathroom", "Conflict", "Accident", "Becoming", "Birthday", "Congress", "Accurate", "Boundary", "Consider", "Achieved", 
"Efficacy", "Envelope", "Distance", "Eighteen,", "Equality", "Distinct", "Election", "Equation", "District", "Governor", "Historic", "Friendly", "Graduate", "Homeless",
"Frontier", "Graphics", "Homepage", "Imperial", "Minimize", "Multiple", "Majority", "Minister", "National", "Marginal", "Ministry", "Negative", "Marriage", "Original", 
"Ninetee", "Preserve", "Overcome", "Northern", "Pressing", "Overhead", "Notebook", "Pressure", "Petition", "Ordinary", "Prospect", "Physical", "Organize", "Protocol",
"Pipeline", "Relation", "Provided", "Platform", "Relative", "Provider", "Pleasant", "Relevant", "Province", "Pleasure", "Reliable", "Simplify", "Sterling", "Swimming", 
"Situated", "Straight", "Symbolic", "Slightly", "Strategy", "Sympathy", "Software", "Strength", "Syndrome", 
"Solution", "Striking", "Tactical", "Terrible", "Training", "Tailored", "Ultimate", "Terminal", "Tracking", "Umbrella", "Universe", "Weakness", "Withdraw", "Unlawful",
"Weighted", "Woodland", "Unlikely", "Whatever", "Workshop", "Valuable", "Volatile", "Vertical", "Wildlife", "Warranty", "Victoria", "Wireless", "Violence"]

#Length: 31
words_fourb = ["Also", "Able", "Acid", "Aged", "Away", "Baby", "Back", "Bank", "Been", "Ball", "Base", "Busy", "Bend", "Bell", "Bird", "Come", "Chat", "Cash", 
               "Cook", "Cool", "Dark", "Each", "Evil", "Even", "Gone", "Gold", "Girl", "Have", "Hair", "Here",
               "Hear", "Into", "Iron", "Ever", "Face", "Kick", "Life", "Like", "Love", "Main", "Move", "Meet", "More", "Nose", "Open", "Pull", "Sell", "Sale"]
#Length: 24
words_twob = ["of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if", "me", "my", "up",  "an", "go", "no", "us", "am"]
words_oneb = ["a", "I"]

def make_choice( vector):
    if vector == "8":
        return random.randint(0,105)
    elif vector == "4":
        return random.randint(0,30)
    elif vector == "2":
        return random.randint(0,23)
    else:
        return random.randint(0,1)
    
# writes bytes less than a full 8-byte word to the end of a file
def write_diff(new_file, diff):
    w1 = words_fourb[make_choice("4")]
    w2 = words_twob[make_choice("2")]
    w3 = words_twob[make_choice("2")]
    w4 = words_oneb[make_choice("1")]
    if diff == 7:
        new_file.write(f'{w1} {w2}')
    elif diff == 6:
        new_file.write(f'{w1}{w2}')
    elif diff == 5:
        new_file.write(f'{w2} {w3}')
    elif diff == 4:
        new_file.write(f'{w1}')
    elif diff == 3:
        new_file.write(f'{w3} ')
    elif diff == 2:
        new_file.write(f'{w3}')
    elif diff == 1:
        new_file.write(f'{w4}')
    return
    
# input: number of eight-byte words, four-byte words, etc. required to meet byte goal
# output: randomized list of words, with the word-lengths interleaved
def choose_words( eights, fours, twos, ones,nbytes, new_file):
    words = []
    sum = eights + fours + twos + ones

    tchars = sum + (eights*8) + (fours*4) + (twos*2) + ones - 1

    i = 0
    while sum > 0:

        if eights > 0:
            words.append(words_eightb[ make_choice("8")])
            eights -= 1
        if fours > 0 and i%2:
            words.append(words_fourb[ make_choice("4")])
            fours -= 1
        if twos > 0:
            words.append(words_twob[ make_choice("2")])
            twos -= 1
        if ones > 0:
            words.append(words_oneb[ make_choice("1")])
            ones -= 1

        sum = eights + fours + twos + ones
        i += 1
        
    total_chars = 0
    for i, word in enumerate(words):
        total_chars += len(word)     # what we would be at if we wrote this

        if total_chars + 1 <= nbytes:
            new_file.write(f'{word} ')
            total_chars += 1        # account for the space
        elif total_chars == nbytes:
            new_file.write(f'{word}')
        else:
            diff = nbytes - (total_chars - len(word)) #how many left to write
            #print(f'Diff is: {diff}')
            if diff > 0:                    # add small number of bytes
                write_diff(new_file, diff)
                break
            if diff == 0:
                break
            elif diff < 0:                     # truncate file
                diff *= -1 
                end = len(word) - diff
                new_file.write(f'{word[0:end]}')
                break

    new_file.close()
    return

'''
Print_diff and print_words together do the same functionality as write_diff and choose_words
These print to the screen without any file I/O
--Note that duplicating the functions is faster than logic blocks within one function for I/O
'''
def print_diff( diff):
    w1 = words_fourb[make_choice("4")]
    w2 = words_twob[make_choice("2")]
    w3 = words_twob[make_choice("2")]
    w4 = words_oneb[make_choice("1")]
    if diff == 7:
        print(f'{w1} {w2}',end='')
    elif diff == 6:
        print(f'{w1}{w2}', end='')
    elif diff == 5:
        print(f'{w2} {w3}', end='')
    elif diff == 4:
        print(f'{w1}', end='')
    elif diff == 3:
        print(f'{w3} ', end='')
    elif diff == 2:
        print(f'{w3}', end='')
    elif diff == 1:
        print(f'{w4}', end='')
    return

def print_words(eights, fours, twos, ones, nbytes):
    words = []
    sum = eights + fours + twos + ones

    tchars = sum + (eights*8) + (fours*4) + (twos*2) + ones - 1
    #print(f'Total chars: {tchars}')

    i = 0
    while sum > 0:

        if eights > 0:
            words.append(words_eightb[ make_choice("8")])
            eights -= 1
        if fours > 0 and i%2:
            words.append(words_fourb[ make_choice("4")])
            fours -= 1
        if twos > 0:
            words.append(words_twob[ make_choice("2")])
            twos -= 1
        if ones > 0:
            words.append(words_oneb[ make_choice("1")])
            ones -= 1

        sum = eights + fours + twos + ones
        i += 1
        
    total_chars = 0
    for i, word in enumerate(words):
        total_chars += len(word)     # what we would be at if we wrote this

        if total_chars + 1 <= nbytes:
            print(f'{word} ', end='')
            total_chars += 1        # account for the space
        elif total_chars == nbytes:
            print(f'{word}',end='')
        else:
            diff = nbytes - (total_chars - len(word)) #how many left to write
            #print(f'Diff is: {diff}')
            if diff > 0:                    # add small number of bytes
                print_diff( diff)
                break
            if diff == 0:
                break
            elif diff < 0:                     # truncate file
                diff *= -1 
                end = len(word) - diff
                print(f'{word[0:end]}', end='')
                break

    return

def generate_new_file( nbytes, to_stdout):
    if not to_stdout:
        print(f"Generating random text file of length {nbytes} bytes\n")

        new_file = open(f'eval_files/{nbytes}.txt', "w+")

    num_eightbs = nbytes  // 8
    remainder = nbytes - (num_eightbs * 8)
    remainder -= num_eightbs   # subtract the number of spaces as words
    num_fours = 0
    num_twos = 0
    num_ones = 0

    tot4s = 0
    tot2s = 0
    tot1s = 0
    i = 0

    while remainder > 0:
        num_fours = remainder // 4
        tot4s += num_fours
        remainder -= (num_fours*4 + num_fours)

        num_twos = remainder // 2
        tot2s += num_twos
        remainder -= (num_twos*2 + num_twos)

        num_ones = 1 if remainder % 2 else 0
        tot1s += num_ones
        remainder -= num_ones + num_ones
        i +=  1
    
    #print(f'Iterations: {i}')
    #print(f'statistics: eights - {num_eightbs} fours- {tot4s}, twos: {tot2s} ones: {tot1s}')

    if not to_stdout:
        to_write = choose_words( num_eightbs, num_fours, num_twos, num_ones, nbytes, new_file)
    else:
        to_write = print_words(num_eightbs, num_fours, num_twos, num_ones, nbytes)
def usage():
    print("Error -- Usage: randfile.py [number of bytes:]")

def main():
  
    parser = argparse.ArgumentParser()
    parser.add_argument("numbytes", help="Number of bytes requested", type=int)
    parser.add_argument("--to_stdout", required=False, default=1, type=int)
    args = parser.parse_args()

    generate_new_file( args.numbytes, args.to_stdout)

if __name__ == "__main__":
    main()