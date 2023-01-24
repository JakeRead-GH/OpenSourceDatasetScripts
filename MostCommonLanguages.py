# languages.txt contains the comma separated language column from the dataset
lang_file = open("languages.txt")
languages = []
lang_count = []

for line in lang_file:
    lang_list = line.split(", ")

    for lang in lang_list:
        lang = lang.strip()
        
        if lang not in languages:
            languages.append(lang)
            lang_count.append(1)
        else:
            pos = languages.index(lang)
            lang_count[pos] += 1

lang_file.close()

lang_data = zip(lang_count, languages)
lang_data_sorted = sorted(lang_data, reverse = True)
lang_count_sorted, languages_sorted = zip(*lang_data_sorted)

print("\nLanguage\tCount\n")

for i in range (len(languages)):
    print(languages_sorted[i] + "\t\t" + str(lang_count_sorted[i]))


