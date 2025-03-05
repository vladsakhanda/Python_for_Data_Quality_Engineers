text = '''homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

text = text.lower().replace(' iz ', ' is ') # Case normalization and replacing iz to is

new_text = ''
number_of_whitespace_characters = 0

# Calculating number of whitespaces, define first words of the sentence and making them in upper case
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

print(f'Number of whitespace characters: {number_of_whitespace_characters}\n')

# Forming additional sentence
additional_sentence = ''
last_sentence_word = ''
for word in new_text.split():
    if any(char in ('.', ';', ':') for char in word):
        for char in ('.', ';', ':'):
            word = word.replace(char, '')

        additional_sentence += word + ' '

# Inserting additional sentence into me specified paragraph
new_text_with_added_sentence = new_text[: new_text.index('ph.')] + 'ph. ' + additional_sentence + new_text[new_text.index('ph.') :]
print(new_text_with_added_sentence)


