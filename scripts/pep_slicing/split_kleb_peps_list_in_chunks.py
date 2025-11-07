def split_peptides_file(input_file, chunk_size=1000):
    with open(input_file, 'r') as infile:
        peptides = infile.readlines()
    
    for i in range(0, len(peptides), chunk_size):
        chunk = peptides[i:i+chunk_size]
        with open(f'kleb_peps_chunk_{i//chunk_size + 1}.txt', 'w') as outfile:
            outfile.writelines(chunk)

# Usage
split_peptides_file("filtered_peptides_9-12mer_kp.txt", chunk_size=1000)




