def normalize_and_replace(text):
    """Lowercase text and replace ' iz ' with ' is '."""
    return text.lower().replace(' iz ', ' is ')


def count_whitespaces_and_capitalize(text):
    """Count whitespaces and capitalize the first letter of each sentence."""
    new_text = ''
    number_of_whitespace_characters = 0
    make_upper_case_next_word = True

    for symbol in text:
        if symbol.isspace():
            number_of_whitespace_characters += 1

        if make_upper_case_next_word and symbol.isalpha():
            symbol = symbol.upper()
            make_upper_case_next_word = False
        if symbol in ('.', ';', ':'):
            make_upper_case_next_word = True

        new_text += symbol

    return new_text, number_of_whitespace_characters


def extract_last_words_and_form_sentence(text):
    """Extract the last word of each sentence and form a new sentence."""
    additional_sentence = ''
    words = text.split()

    for word in words:
        if any(char in ('.', ';', ':') for char in word):
            word = word.strip('.;:')
            additional_sentence += word + ' '

    return additional_sentence.strip()


def insert_additional_sentence(text, additional_sentence):
    """Insert the additional sentence into the text at a specified location."""
    index = text.index('ph.')
    return text[:index] + 'ph. ' + additional_sentence + ' ' + text[index:]


def process_text(text):
    """Process text by normalizing, counting whitespaces, extracting last words, and updating text."""
    normalized_text = normalize_and_replace(text)
    new_text, whitespace_count = count_whitespaces_and_capitalize(normalized_text)
    additional_sentence = extract_last_words_and_form_sentence(new_text)
    new_text_with_added_sentence = insert_additional_sentence(new_text, additional_sentence)

    return new_text_with_added_sentence, whitespace_count

text = '''homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

final_text, total_whitespaces = process_text(text)

print(f'Number of whitespace characters: {total_whitespaces}\n')
print(final_text)
