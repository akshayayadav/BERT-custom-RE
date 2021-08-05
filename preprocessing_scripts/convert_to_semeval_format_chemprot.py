import re
import random
def convert_chemprot_triplet_to_semeval_format():
    base_path = "../ChemProt_Corpus/chemprot_development/chemprot_development/"
    chemprot_triplet_file = open(base_path + "chemprot_development_gold_standard_withNOT_triplets.tsv", "r")
    chemprot_semeval_outfile = open(base_path + "chemprot_development_gold_standard_withNOT_triplets_semeval.txt", "w")
    line_list = list()
    for line in chemprot_triplet_file:
        line = line.rstrip()
        line_list.append(line)

    line_list = random.sample(line_list, len(line_list))

    counter = 1
    for line in line_list:
        linearr = re.split(r'\t', line)
        rel = linearr[1]
        sent = linearr[8]

        chemprot_semeval_outfile.write(str(counter) + "\t" +
                                       "\"" + sent + "\"" + "\n" +
                                       rel + "\n" +
                                       "Comment:" + "\n" +
                                       "\n")
        counter += 1

    chemprot_triplet_file.close()
    chemprot_semeval_outfile.close()


convert_chemprot_triplet_to_semeval_format()