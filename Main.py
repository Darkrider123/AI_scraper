from UrlMakers import *
from IA import *
from Scraper import *

def scrape_weidmueller():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    #options.add_argument("--headless")
    nr_of_processes = 5

    o_t = []
    a_k = []
    er = []
    path = "Weidmueller"
    excel_input_filename = "Pricelist_Weidmueller_edit.xlsx"
    result_path = path + "/results"
    title_xpath = "/html/body/div[3]/div[2]/div[1]/div[3]/ul/li/div[2]/a/span[1]"
    description_xpath = "/html/body/div[3]/div[2]/div[1]/div[3]/ul/li/div[2]/a/p"
    urlMaker = UrlMakerWeidmueller()
    scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker, options = options, nr_of_processes = nr_of_processes)
    return a_k, o_t, er


def scrape_pheonix():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    #options.add_argument("--headless")
    nr_of_processes = 6

    o_t = []
    a_k = []
    er = []
    path = "Phoenix"
    excel_input_filename = "Pricelist_Phoenix_Contact_edit.xlsx"
    result_path = path + "/results"
    title_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div/h1"
    description_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div/div[9]/div[1]/div[2]/div[1]/p"
    urlMaker = UrlMakerPhoenix()
    scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker, True, options = options ,nr_of_processes = nr_of_processes)
    return a_k, o_t, er


def scrape_eaton():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    #options.add_argument("--headless")
    nr_of_processes = 3

    o_t = []
    a_k = []
    er = []
    path = "Eaton"
    excel_input_filename = "Pricelist_Phoenix_Contact_edit.xlsx"
    result_path = path + "/results"
    title_xpath = "/html/body/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[5]/div[1]/div[1]/div/div[1]/div/div/div[2]/h1"
    description_xpath = "/html/body/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[5]/div[1]/div[1]/div/div[1]/div/div/div[2]/div[1]"
    urlMaker = UrlMakerEaton()
    scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker, False, True, options, nr_of_processes = nr_of_processes)



def main():
    scrape_pheonix()

if __name__ == '__main__':
    main()