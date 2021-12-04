import pandas

from BagOfWords import *
from DataNormalization import *
from sklearn.cluster import MeanShift




def classify_data():
    df = pandas.read_excel("appended_results/results.xlsx", sheet_name = "Sheet1")
    ids = df[0]
    descriptions = df[2]
    companies = df[3]

    aux = list()

    colors = list()
    with open("colors.txt", "r") as f:
        input = f.read()
        colors = input.split("\n")
    
    for color in colors:
        aux.append(color.upper())

    colors = aux

    aux = list()

    for description in descriptions:
        description = str(description).upper()
        description = description.replace(",", "")

        for color in colors:
            description = description.replace(color, "")
        aux.append(description)
    
    descriptions = aux

    aux = list()
    for id in ids:
        aux.append(id)
    ids = aux

    aux = list()
    for company in companies:
        aux.append(company)
    companies = aux



    bow = Bag_of_words()
    bow.build_vocabulary(descriptions)
    train_features = bow.get_features(descriptions)
    train_features, _ = normalize_data(train_features, train_features, "l1")


    ms = MeanShift(bandwidth= 0.06, n_jobs= -1)
    ms.fit(train_features)

    labels = ms.labels_
    n_clusters = len(np.unique(labels))

    print("Number of estimated clusters: ",n_clusters)


    rez = []

    for id, description, company, label in zip (ids, descriptions, companies, labels):
        rez.append([id, description, company ,label])

    df = pandas.DataFrame(rez)
    df.to_excel("Crossref_AI.xlsx")
