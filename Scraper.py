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



def scraper_logic(o_t, a_k, er, urlMaker, close_reopen_driver= False):
    pass


def scraper(o_t, a_k, er, path, result_path, excel_input_filename, title_xpath, description_xpath, urlMaker, close_reopen_driver= False):

    filename_path = path + "/" + excel_input_filename
    ids = read_ids(filename_path)
    
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

    
    only_title_write_file(o_t, result_path)
    all_okay_write_file(a_k, result_path)
    error_write_file(er, result_path)