'''
Naomi Havelaar
'''
# Takes a DNA sequence string and adds the desired number of dashes to the end of the sequence.
# Returns the new string with the dash at the end. 
def pad_with_indels(sequence, num):
    return sequence + ('-' * num)

# Inserts a dash into a DNA sequence string at the desired index.
# Returns the new string with the dash inserted.
def insert_indel(sequence, index):
    beginning = sequence[:index]
    end = sequence[index:]
    with_indel = beginning + '-' + end
    return with_indel

# Counts the number of matches between Sequence 1 and Sequence 2.
# Returns the number of matches. 
def count_matches(sequence1, sequence2):
    match_iterator = 0
    for i in range(len(sequence1)): 
        if sequence1[i] == sequence2[i]:
            if (sequence1[i] != '-') and (sequence2[i] != '-'):
                match_iterator += 1
    return match_iterator

# Prints a menu in the program.
def print_menu():
    menu = print('Main Menu\n1. Insert an indel\n2. Remove an indel\n3. Score similarity\n4. Suggest indel\n5. Quit\n')
    return menu

# Asks the user to choose an option from the menu.
# Returns the menu option. 
def get_menu_choice():
    menu_option = int(input('Please choose an option: '))
    while menu_option <= 0 or menu_option > 5:
        menu_option = int(input('Please choose an option: '))
    return menu_option

# Asks the user which DNA sequence to use in the program.
# Returns the sequence number.
def get_sequence_number():
    sequence = int(input('\nSequence 1 or 2? '))
    while sequence <= 0 or sequence >=3:
            sequence = int(input('\nSequence 1 or 2? '))
    return sequence

# Asks the user to input a position where an indel can be inserted within the given DNA sequence.
# Returns the validated position number. 
def get_insert_position(sequence):
    position = int(input('Please choose a position: '))
    while position <= 0 or position > len(sequence):
        position = int(input('Please choose a position: '))
    return position

# Asks the user to input a position within the given DNA sequence where an indel can be found.
# Validates that input until it is correct.
# Returns the validated position number.
def get_remove_position(sequence):
    position = int(input('Please choose a position: '))
    index_indel = 0
    while index_indel < len(sequence):
        index_indel = sequence.find('-', index_indel)
        if position == index_indel + 1:
            return position
        else:
            position = int(input('Please choose a position: '))

# Given a sequence and an index of an indel in that sequence, removes the indel at the given index.
# Returns the new string.    
def remove_indel(sequence, index):
    init_seq = sequence[:index - 1]
    new_seq_removed = sequence[index:]
    return init_seq + new_seq_removed   

# Takes two DNA sequences and prints matching positions in lowercase.
# Mismatching positions are printed in uppercase.
def get_lower_upper(sequence1, sequence2):    
    newsequence1 = ''
    newsequence2 = ''
    for i in range(len(sequence1)): 
        if sequence1[i].lower() == sequence2[i].lower(): 
            newsequence1 += str(sequence1[i].lower())
            newsequence2 += str(sequence2[i].lower())
        else:
            newsequence1 += str(sequence1[i].upper())
            newsequence2 += str(sequence2[i].upper())
    return newsequence1, newsequence2    

# Compares the two DNA sequences and determines which length of the sequences is smaller. 
# Returns one given sequence and a new sequence with indels inserted at the end. 
def get_append_indel(sequence1, sequence2):
    if len(sequence1) < len(sequence2):
        sequence1 = pad_with_indels(sequence1, len(sequence2) - len(sequence1))
    elif len(sequence2) < len(sequence1):
        sequence2 = pad_with_indels(sequence2, len(sequence1) - len(sequence2))
    return sequence1, sequence2

# Takes two sequences and adds an indel to each position within the shorter sequence.
# Counts the matches between the sequence with the inserted indel and the other sequence.
# Calculates the suggested position in the first DNA sequence where an indel should be added
# to maximize the similarity between the two sequences.
# Returns the suggested position.
def find_optimal_indel_position(sequence, othersequence):
    suggested_position = 1
    max_match = 0
    for i in range(len(sequence)):
        newsequence = insert_indel(sequence, i)
        newsequence, othersequence = get_append_indel(newsequence, othersequence)
        newsequence, othersequence = get_lower_upper(newsequence, othersequence)
        num_match = count_matches(newsequence, othersequence)
        if num_match > max_match:
            max_match = num_match
            suggested_position = i + 1
    return suggested_position
    
if __name__ == "__main__":
    sequence1 = input('Please enter DNA Sequence 1: ')
    sequence2 = input('Please enter DNA Sequence 2: ')
    print()

    sequence1, sequence2 = get_append_indel(sequence1, sequence2) 
    
    newsequence1, newsequence2 = get_lower_upper(sequence1, sequence2)
            
    print('Sequence 1:', newsequence1)
    print('Sequence 2:', newsequence2) 
    print()

    #MILESTONE 2
    print_menu()
    menu_option = get_menu_choice()
    while menu_option <= 5:
        if menu_option == 1:
            sequence_number = get_sequence_number()
            if sequence_number == 1:
                seq1_position = get_insert_position(newsequence1) - 1 
                prelim_s1_upper = insert_indel(newsequence1, seq1_position) 
                prelim_s1_upper, sequence2 = get_append_indel(prelim_s1_upper, sequence2) 
                newsequence1, newsequence2 = get_lower_upper(prelim_s1_upper, sequence2)
            elif sequence_number == 2:
                seq2_position = get_insert_position(newsequence2) - 1 
                prelim_s2_upper = insert_indel(newsequence2, seq2_position) 
                prelim_s2_upper, sequence1 = get_append_indel(prelim_s2_upper, sequence1) 
                newsequence1, newsequence2 = get_lower_upper(prelim_s2_upper, sequence1)
            
        elif menu_option == 2:
            sequence_number = get_sequence_number()
            if sequence_number == 1:
                seq1_with_indel = get_remove_position(newsequence1)
                newsequence1 = remove_indel(newsequence1, seq1_with_indel)
                newsequence2 = remove_indel(newsequence2, len(newsequence2))
            elif sequence_number == 2:
                seq2_with_indel = get_remove_position(newsequence2)
                newsequence1 = remove_indel(newsequence1, len(newsequence1))
                newsequence2 = remove_indel(newsequence2, seq2_with_indel)
            
        elif menu_option == 3:
            matches = count_matches(newsequence1, newsequence2)
            mismatches = len(newsequence1) - matches
            match_rate = (matches / len(newsequence1) * 100)
            print(f"\nSimilarity: {matches} matches, {mismatches} mismatches. {match_rate:.1f}% match rate.\n") 
            
        elif menu_option == 4:
            sequence_number = get_sequence_number()
            if sequence_number == 1:
                suggested_position = find_optimal_indel_position(newsequence1, newsequence2)
                newsequence1_pos = insert_indel(newsequence1, suggested_position)
                newsequence1_pos, newsequence2_pos = get_append_indel(newsequence1_pos, newsequence2)
                newsequence1_pos, newsequence2_pos = get_lower_upper(newsequence1_pos, newsequence2_pos)
                matches = count_matches(newsequence1_pos, newsequence2_pos)
                mismatches = len(newsequence1_pos) - matches
                match_rate = (matches / len(newsequence1_pos) * 100)
                print(f"Insert an indel into Sequence 1 at position {suggested_position}.")
                print(f"\nSimilarity: {matches} matches, {mismatches} mismatches. {match_rate:.1f}% match rate.\n") 
                
            elif sequence_number == 2:
                suggested_position = find_optimal_indel_position(newsequence2, newsequence1)
                newsequence2_pos = insert_indel(newsequence2, suggested_position)
                newsequence1_pos, newsequence2_pos = get_append_indel(newsequence1, newsequence2_pos)
                newsequence1_pos, newsequence2_pos = get_lower_upper(newsequence1_pos, newsequence2_pos)
                matches = count_matches(newsequence1_pos, newsequence2_pos)
                mismatches = len(newsequence2_pos) - matches
                match_rate = (matches / len(newsequence2_pos) * 100)
                print(f"Insert an indel into Sequence 2 at position {suggested_position}.")
                print(f"\nSimilarity: {matches} matches, {mismatches} mismatches. {match_rate:.1f}% match rate.\n") 
                

        elif menu_option == 5:
            exit()
                
        print('\nSequence 1:', newsequence1)
        print('Sequence 2:', newsequence2)
        print()
        print_menu()
        menu_option = get_menu_choice()
    
