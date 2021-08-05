import re
import random
from biobert_embedding.embedding import BiobertEmbedding

def convert_chemprot_triplet_to_semeval_format():
    base_path = "../DrugProt_Corpus/training/"
    chemprot_triplet_file = open(base_path + "drugprot_training_triplets.tsv", "r")
    chemprot_semeval_outfile = open(base_path + "drugprot_training_triplets_semeval.txt", "w")
    biobert = BiobertEmbedding()
    line_list = list()
    for line in chemprot_triplet_file:
        line = line.rstrip()
        line_list.append(line)

    line_list = random.sample(line_list, len(line_list))

    counter = 1
    for line in line_list:
        linearr = re.split(r'\t', line)
        rel = linearr[6]
        sent = linearr[7]
        seq_length = len(biobert.process_text(sent))

        if(seq_length>512):
            continue

        chemprot_semeval_outfile.write(str(counter) + "\t" +
                                       "\"" + sent + "\"" + "\n" +
                                       rel + "\n" +
                                       "Comment:" + "\n" +
                                       "\n")
        counter += 1

    chemprot_triplet_file.close()
    chemprot_semeval_outfile.close()


convert_chemprot_triplet_to_semeval_format()