import pandas
from pandas.io import excel
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import io
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import multiprocessing


NR_OF_PROCESSES = 5



def read_ids(filename):
    df = pandas.read_excel(filename, sheet_name= "Sheet1")
    ids = df["Part Number"]
    return ids


def only_title_add(id , title, o_t):
    o_t.append([str(id), title.text])

def all_okay_add(id , title, description, a_k):
    a_k.append([str(id), title.text, description.text])

def error_add(id, er):
    er.append([id])


def only_title_write_file(o_t, result_path):
    data_frame_only_title = pandas.DataFrame(o_t)
    data_frame_only_title.to_excel(result_path + "/only_title.xlsx")

def all_okay_write_file(a_k, result_path):
    data_frame_ok = pandas.DataFrame(a_k)
    data_frame_ok.to_excel(result_path + "/all_ok.xlsx")

def error_write_file(er, result_path):
    data_frame_er = pandas.DataFrame(er)
    data_frame_er.to_excel(result_path + "/error.xlsx")



def scraper_logic(id_curent_process, d, title_xpath , description_xpath , urlMaker, ids ,close_reopen_driver= False):
    o_t = []
    a_k = []
    er = []

    driver = None
    if close_reopen_driver == False:
        driver = webdriver.Chrome(executable_path= 'chromedriver.exe')

    for id in ids:

        if close_reopen_driver == True:
            driver = webdriver.Chrome(executable_path= 'chromedriver.exe')
        urlMaker.make_url(id)
        formated_url = urlMaker.url 
        driver.get(formated_url)

        try:

            title = driver.find_element_by_xpath(title_xpath)

            try:
                description = driver.find_element_by_xpath(description_xpath)
                if description.text == "":
                    only_title_add(id, title, o_t)
                else:
                    all_okay_add(id, title, description, a_k)


            except selenium.common.exceptions.NoSuchElementException:
                only_title_add(id, title, o_t)

        except selenium.common.exceptions.NoSuchElementException:
            error_add(id, er)
        
        if close_reopen_driver == True:
            driver.close()

    if close_reopen_driver == False:
        driver.close()


    d[id_curent_process] = [o_t, a_k, er]


def scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker, close_reopen_driver= False):

    filename_path = path + "/" + excel_input_filename
    ids = read_ids(filename_path)

    with multiprocessing.Manager() as manager:
        d = manager.dict()

        i = 0
        j = unitate = len(ids)/ NR_OF_PROCESSES
        jobs = []
        j = int(j)
        unitate = int(unitate)
        id_curent_process = 0

        while j <= len(ids) + 1:
            ids_curent_process = ids[i:j]
            p = multiprocessing.Process(target = scraper_logic, args=(id_curent_process, d, title_xpath, description_xpath, urlMaker, ids_curent_process, close_reopen_driver))
            id_curent_process += 1
            jobs.append(p)

            i += unitate
            j += unitate

        if i < len(ids) and j != len(ids) + 1:
            j = len(ids) + 1
            ids_curent_process = ids[i:j]
            p = multiprocessing.Process(target = scraper_logic, args=(id_curent_process, d, title_xpath, description_xpath, urlMaker, ids_curent_process, close_reopen_driver))
            id_curent_process += 1
            jobs.append(p)

        for job in jobs:
            job.start()

        for job in jobs:
            job.join()
        
        
        id_curent_process -= 1

        for id_process in range(id_curent_process):
            o_t.append(d[id_process][0])
            a_k.append(d[id_process][1])
            er.append(d[id_process][2])
        
        o_t = [item for sublist in o_t for item in sublist]
        a_k = [item for sublist in a_k for item in sublist]
        er = [item for sublist in er for item in sublist]

    
    only_title_write_file(o_t, result_path)
    all_okay_write_file(a_k, result_path)
    error_write_file(er, result_path)