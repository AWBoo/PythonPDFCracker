def process_text(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            text = infile.read()
    except FileNotFoundError:
        print(f"The file {input_file} does not exist.")
        return

    words = text.split()
    processed_words = []

    for word in words:
        if len(word) <= 5:
            number = 17  # Reset number for each new word
            for i in range(8):
                processed_words.append(f"{word}{number}")
                number += 1  # Increment number for the next variant

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(processed_words))

    print(f"Processing complete. Results written to {output_file}")

# Example usage
input_file = 'dictionary.txt'
output_file = 'ScrubbedDict.txt'
process_text(input_file, output_file)
