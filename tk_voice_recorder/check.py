import os

sentences_folder = os.listdir("/Users/tomer/test")
for sen in sentences_folder:
    if not sen.endswith('.txt'):
        sentences_folder.remove(sen)
#print(sentences_folder)

sentence_file = sentences_folder[0]
sentences_folder.remove(sentence_file)
sentence = open(os.path.join('/Users/tomer/test', sentence_file)).read()
filename = sentence_file.replace('.txt', '.wav')

print(sentences_folder)
print(sentence)
print(filename)