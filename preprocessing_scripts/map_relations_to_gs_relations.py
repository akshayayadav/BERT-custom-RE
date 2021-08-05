import re


def get_training_relations_dict(training_relations_filename):
    training_relations_dict = {}
    training_relations_file = open(training_relations_filename, "r", encoding='utf8')
    for line in training_relations_file:
        line = line.rstrip()
        linearr = re.split(r'\t', line)
        key = linearr[0] + "-" + linearr[1] + "-" + linearr[4] + "-" + linearr[5]
        value = linearr[3]
        training_relations_dict[key] = value

    return training_relations_dict

def map_relation_names():
    base_path = "../ChemProt_Corpus/chemprot_test/chemprot_test/"
    training_relations_dict = get_training_relations_dict(base_path + "chemprot_test_relations.tsv")
    gs_training_relations_file = open(base_path + "chemprot_test_gold_standard_withNOT.tsv", "r")
    mapped_gs_training_relations_file = open(base_path + "chemprot_test_gold_standard_withNOT_mapped.tsv", "w")
    for line in gs_training_relations_file:
        line = line.rstrip()
        linearr = re.split(r'\t', line)
        key = linearr[0] + "-" + linearr[1] + "-" + linearr[2] + "-" + linearr[3]
        mapped_gs_training_relations_file.write(line + "\t" + training_relations_dict[key] + "\n")

    gs_training_relations_file.close()
    mapped_gs_training_relations_file.close()

map_relation_names()




