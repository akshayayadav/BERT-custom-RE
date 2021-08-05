import re
import spacy
import scispacy
import sys


def get_abstract_dict(abstract_filename):
    abstract_dict={}
    abstract_file = open(abstract_filename, "r")
    for line in abstract_file:
        line = line.rstrip()
        linearr = re.split(r'\t', line)
        abstract_dict[linearr[0]] = {}
        abstract_dict[linearr[0]]["title"] = linearr[1]
        abstract_dict[linearr[0]]["abstract"] = linearr[2]

    abstract_file.close()

    return abstract_dict

def get_entities_dict(entities_filename):
    entities_dict = {}
    entities_file = open(entities_filename, "r")
    for line in entities_file:
        line = line.rstrip()
        linearr = re.split(r'\t', line)
        if linearr[0] in entities_dict:
            entities_dict[linearr[0]][linearr[1]] = {}
            entities_dict[linearr[0]][linearr[1]]["type"] = linearr[2]
            entities_dict[linearr[0]][linearr[1]]["span"] = (int(linearr[3]), int(linearr[4]))
            entities_dict[linearr[0]][linearr[1]]["name"] = linearr[5]
        else:
            entities_dict[linearr[0]] = {}
            entities_dict[linearr[0]][linearr[1]] = {}
            entities_dict[linearr[0]][linearr[1]]["type"] = linearr[2]
            entities_dict[linearr[0]][linearr[1]]["span"] = (int(linearr[3]), int(linearr[4]))
            entities_dict[linearr[0]][linearr[1]]["name"] = linearr[5]

    entities_file.close()
    return entities_dict

def insert_e1_e2_tags(text_str, span1, span2):
    e1_start_tag = '<e1>'
    e1_end_tag = '</e1>'

    e2_start_tag = '<e2>'
    e2_end_tag = '</e2>'

    text_list = list(text_str)

    if(span2[0]>span1[0]):
        text_list.insert(span1[0], e1_start_tag)
        text_list.insert(span1[1] + 1, e1_end_tag)

        text_list.insert(span2[0] + 2, e2_start_tag)
        text_list.insert(span2[1] + 3, e2_end_tag)
        entity_relation_order = "(e1,e2)"

    else:
        text_list.insert(span2[0], e1_start_tag)
        text_list.insert(span2[1] + 1, e1_end_tag)

        text_list.insert(span1[0] + 2, e2_start_tag)
        text_list.insert(span1[1] + 3, e2_end_tag)
        entity_relation_order = "(e2,e1)"

    text_str = ''.join(text_list)

    return [text_str, entity_relation_order]

def get_e1_e2_tagged_sentence(model, text_str):
    text_processed = model(text_str)
    sents = list(text_processed.sents)
    filtered_sentence = [sent for sent in sents if re.search(r'\<e[12]\>.+?\<e[12]\>', str(sent))]
    return filtered_sentence

def map_relations():
    base_path = "../drugprot-training-development-test-background/drugprot-gs-training-development/development/"
    abstract_dict = get_abstract_dict(base_path + "drugprot_development_abstracs.tsv")
    entities_dict = get_entities_dict(base_path + "drugprot_development_entities.tsv")
    relations_filename = base_path + "drugprot_development_relations.tsv"
    relation_triplet_outfile = open(base_path+"drugprot_development_triplets.tsv",
                                    "w")
    skipped_relations_outfile = open(base_path+"drugprot_development_skipped.tsv",
                                    "w")
    scispacy_model = spacy.load("en_core_sci_sm")
    relations_file = open(relations_filename, "r", encoding='utf8')
    for line in relations_file:
        line = line.rstrip()
        linearr = re.split(r'\t', line)
        text = abstract_dict[linearr[0]]['title'] + " " + abstract_dict[linearr[0]]['abstract']
        e1_id = re.split(r':', linearr[2])
        e2_id = re.split(r':', linearr[3])
        relation_class = linearr[1]
        #relation_class = re.sub(r':', "_", relation_class)

        e1_span = entities_dict[linearr[0]][e1_id[1]]['span']
        e2_span = entities_dict[linearr[0]][e2_id[1]]['span']

        e1_name = entities_dict[linearr[0]][e1_id[1]]['name']
        e2_name = entities_dict[linearr[0]][e2_id[1]]['name']

        text, entity_order = insert_e1_e2_tags(text, e1_span, e2_span)
        sentence = get_e1_e2_tagged_sentence(scispacy_model, text)
        if len(sentence) > 0:
            if re.search(r'<e1>', str(sentence[0])) and re.search(r'<e2>', str(sentence[0])):
                relation_triplet_outfile.write(line+"\t"+
                                           e1_name + "\t"+
                                           e2_name + "\t" +
                                           relation_class +
                                           entity_order + "\t" +
                                           str(sentence[0]) + "\n")
            else:
                skipped_relations_outfile.write(line+"\t"+
                                           e1_name + "\t"+
                                           e2_name + "\t" +
                                           relation_class +
                                           entity_order + "\t" +
                                           str(sentence[0]) + "\n")

        else:
            skipped_relations_outfile.write(line+"\n")

    relation_triplet_outfile.close()
    skipped_relations_outfile.close()

map_relations()