import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, matthews_corrcoef, balanced_accuracy_score, \
    confusion_matrix, f1_score, accuracy_score, precision_score


pred_tsv = pd.read_csv("../DrugProt_Corpus/development/"
                       "drugprot_development_triplets_withPreds.tsv", sep = "\t",
                       names=["pmid", "relation_type", "entity1", "entity2",
                              "entity1_name", "entity2_name", "true_relation_label", "sentence",
                              "pred_relation_label"])
'''
class_labels = ["CPR_3(e1,e2)", "CPR_3(e2,e1)",
                "CPR_4(e1,e2)", "CPR_4(e2,e1)",
                "CPR_5(e1,e2)", "CPR_5(e2,e1)",
                "CPR_6(e1,e2)", "CPR_6(e2,e1)",
                "CPR_9(e1,e2)", "CPR_9(e2,e1)",
                "CPR_10(e1,e2)", "CPR_10(e2,e1)"]

'''

results = precision_recall_fscore_support(pred_tsv["true_relation_label"], pred_tsv["pred_relation_label"],
                                          average='weighted')
acc = accuracy_score(pred_tsv["true_relation_label"], pred_tsv["pred_relation_label"])

#conf_matrix = confusion_matrix(pred_tsv["true_relation_label"], pred_tsv["pred_relation_label"], labels=class_labels)

results_mcc = matthews_corrcoef(pred_tsv["true_relation_label"], pred_tsv["pred_relation_label"])
results_ba = balanced_accuracy_score(pred_tsv["true_relation_label"], pred_tsv["pred_relation_label"])


print(results)
print(acc)
print(results_mcc)
print(results_ba)
#print(conf_matrix)