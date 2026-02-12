# Este arquivo indica que o diretório é um pacote Python.
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time 
import datetime
import plotly.graph_objects as go
from selenium.common.exceptions import NoSuchElementException
from .dadosDI import *
from .capturarDI import *
from .tratarDI import *