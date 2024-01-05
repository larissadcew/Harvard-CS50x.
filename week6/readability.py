from cs50 import get_string

text = get_string("Text: ")

letter = 0
sentence = 0
word = 1

for i in range(len(text)):
    if text[i].isalpha():
        letter += 1
    elif text[i].isspace():
        word += 1
    elif text[i] in ['!', '.', '?']:
        sentence += 1

L = float(letter / word) * 100
S = float(sentence / word) * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

if index <= 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")