from UrlMakers import *
from Scraper import *
from BagOfWords import *
from DataNormalization import *
from sklearn.cluster import MeanShift


def scrape_weidmueller():
    o_t = []
    a_k = []
    er = []
    path = "Weidmueller"
    excel_input_filename = "Pricelist_Weidmueller_edit.xlsx"
    result_path = path + "/results"
    title_xpath = "/html/body/div[3]/div[2]/div[1]/div[3]/ul/li/div[2]/a/span[1]"
    description_xpath = "/html/body/div[3]/div[2]/div[1]/div[3]/ul/li/div[2]/a/p"
    urlMaker = UrlMakerWeidmueller()
    scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker)
    return a_k, o_t, er


def scrape_pheonix():
    o_t = []
    a_k = []
    er = []
    path = "Phoenix"
    excel_input_filename = "Pricelist_Phoenix_Contact_edit.xlsx"
    result_path = path + "/results"
    title_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div/h1"
    description_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div/div[9]/div[1]/div[2]/div[1]/p"
    urlMaker = UrlMakerPhoenix()
    scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker, True)
    return a_k, o_t, er



def some_ai_try():
    df = pandas.read_excel("Weidmueller/results/all_ok.xlsx", sheet_name = "Sheet1")
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


    ms = MeanShift(bandwidth= 0.06, n_jobs= 5)
    ms.fit(train_features)

    labels = ms.labels_
    n_clusters = len(np.unique(labels))

    print("Number of estimated clusters: ",n_clusters)


    rez = []

    for id, description, company, label in zip (ids, descriptions, companies, labels):
        rez.append([id, description, company ,label])

    df = pandas.DataFrame(rez)
    df.to_excel("Crossref_AI.xlsx")



if __name__ == '__main__':
    some_ai_try()