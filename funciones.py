import streamlit as st
import psycopg2
import pandas as pd
import sqlite3
# despues vemos de aca si algo no se usa o si falta alguna mas


def get_db_conection():
     user = "postgres.atwgqupcjrxxxxzmlkdm"
     password = "Pbk3ofO6Ife6oI0A"
     host = "aws-0-us-east-1.pooler.supabase.com"
     port = "5432"
     dbname = "postgres" ## aca estaba lo mismo que en user
     conn = psycopg2.connect(
          dbname = dbname,
          user = user,
          password = password,
          host = host,
          port = port
     )
     return conn


