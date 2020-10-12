import pdfplumber
import re

words_to_remove = [
"la","el","los", "las","un","una","y","o","al","a",
"de","que","en","se","con","lo","por","le","del","su","es",
"si","me","era","sus","él","ha","te"
]

class PDFCounter:
    def __init__(self, path, exclude_words=[]):
        self._path = path
        self._words = {}
        self._characters_to_remove = "—!'?¿¡()-.»«•:1234567890"
        self._pattern = "[" + self._characters_to_remove + "]"
        self._words_to_remove = exclude_words


    def initialize(self): 
        with pdfplumber.open(self._path) as pdf: 
            print("\n\n\n\nLoading file and parsing it...")
            print("\nThis will take long\n\n\n\n")
            for page in pdf.pages: 
                self._get_words_by_page(page) 
        return self._words
                       
    def _get_words_by_page(self, page):
        words = page.extract_words()
        for word in words:
            sub_word = re.sub(self._pattern, "", word['text']).lower()
            if sub_word in self._words_to_remove or sub_word == '':
                continue
            if sub_word in self._words:
                self._words[sub_word] += 1
            else:
                self._words[sub_word] = 1

file_path = input("Enter path to file: ") or "C:/Users/Sergio/Downloads/file.pdf"

try:

    pdf_counter = PDFCounter(file_path, exclude_words=words_to_remove) 


    words = pdf_counter.initialize()

    sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)

    while True:
        batch = input("How many words? (Default 50): ") or "50"
        if int(batch) <= len(sorted_words):
            break;
        else:
            print('Index out of range, the list of word is of length {}'.format(len(sorted_words)))


    for i in range(0, int(batch)):
        print("{}: {}".format(sorted_words[i][0], sorted_words[i][1]))


except FileNotFoundError:
    print("\n-----------------------ERROR------------------------\n")
    print("Could not find file. Make sure the path is correct")
    print("It should look something like this: C:/Users/yourusername/file.pdf")
    print("If you placed you file on the same directory as this file you can use: file.pdf\n")
    print("Try again...\n")
    print("------------------------------------------------------")
except:
    print("\nERROR: Something went wrong...\n")