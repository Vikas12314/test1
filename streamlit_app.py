import streamlit as st
import subprocess
import sys
import os
import io
import shlex
import pandas as pd
import snowflake.connector
import pandas as pd
from pathlib import Path
# Gets the version
ctx = snowflake.connector.connect(
    user='EAI20071',
    password='Student@1234',
    account='epson.east-us-2.azure',
	warehouse='TRANSFORMING',
    database='CATALINA',
    schema='RAW',
	role='CATALINA_DEVELOPER'
    )
 


st.title("Motherboard Process")
st.markdown('_This program takes the Files with Printer Serial Number as Input and generates file for each serial number with Ink Shots_')

st.markdown('### Click below to validate Input File ###')

if st.button('Validate Input File'):
	path = './printer_serial_number.txt'
	obj = Path(path)
	if obj.exists():
	    st.write('**File Exists Having Below Serial Numbers**')
	    df = pd.read_csv("./printer_serial_number.txt",header=None)
	    st.write(df)
	    
	else:
	    st.write('**File Does Not Exists.Please Provide The Input File**')
if st.button('Generate Motherboard Files'):
    st.write('The files with the below data is generated for Printer Serial Numbers')
    df = pd.read_csv("./printer_serial_number.txt",header=None)
 
    for i, j in df.iterrows():
        x = df.iloc[[i]].to_string(header=False,index=False,index_names=False)		
        st.write(x)
        d_black = pd.read_sql("""SELECT DISTINCT  PRINTER_SERIAL_NBR,BLACK_SHOTS FROM 
		CMOWNER.PRINTER_MASTER WHERE PRINTER_SERIAL_NBR =""" + "'" +  x + "'" +";", con = ctx)
        d_param = float(d_black.iloc[:, [1]].to_string(header=False,index=False,index_names=False))
        d_sr = d_black.iloc[:, [0]].to_string(header=False,index=False,index_names=False)
 		
        if d_param != 0:
            st.write(d_sr + " have black shots")
            df_nb = pd.read_sql("""SELECT  DISTINCT 
	        RPAD(PRINTER_SERIAL_NBR,18,' ') C1,
	        LPAD(CYAN_SHOTS,20,'0') C2,LPAD(MAGENTA_SHOTS,20,'0') C3,
	        LPAD(YELLOW_SHOTS,20,'0') C4,LPAD(BLACK_SHOTS,20,'0') C5,
	        '00000000000000'  C6 ,'00000000000000'  C7,'00000000000000'  C8 ,'00000000000000'  C9,
            '00000000000000'  C10 ,'00000000000000'  C11,'00000000000000'  C12 ,'00000000000000'  C13,
	        '00000000000000'  C14 ,'00000000000000'  C15,'00000000000000'  C16 ,'00000000000000'  C17,
	        '00000000000000'  C19 ,'00000000000000'  C20,'00000000000000'  C21 ,'00000000000000'  C22,
	        '00000000000000'  C23 ,'00000000000000'  C24,'00000000000000'  C25 ,'00000000000000'  C26,'0000' C27
	        FROM CMOWNER.PRINTER_MASTER
            WHERE PRINTER_SERIAL_NBR = """ + "'" +  d_sr + "'" +";", con = ctx)
            st.write(df_nb)
            df_nb.to_csv("./temp/" + x + ".txt",sep='~', index = False, header = False)
            subprocess.run(["./chksumgencmc7.exe", "./temp/" + d_sr + ".txt","./"])
            os.rename('./chksumgen.txt', './' + x +'.txt')
            os.replace("./genreport.txt", "./genreport/genreport.txt")
        else:
            st.write(d_sr + " does not have shots")
            df_b = pd.read_sql("""SELECT  DISTINCT 
	        RPAD(PRINTER_SERIAL_NBR,18,' ') C1,
	        LPAD(CYAN_SHOTS,20,'0') C2,LPAD(MAGENTA_SHOTS,20,'0') C3,
	        LPAD(YELLOW_SHOTS,20,'0') C4,
	        '00000000000000'  C6 ,'00000000000000'  C7,'00000000000000'  C8 ,'00000000000000'  C9,
            '00000000000000'  C10 ,'00000000000000'  C11,'00000000000000'  C12 ,'00000000000000'  C13,
	        '00000000000000'  C14 ,'00000000000000'  C15,'00000000000000'  C16 ,'00000000000000'  C17,
	        '00000000000000'  C19 ,'00000000000000'  C20,'00000000000000'  C21 ,'00000000000000'  C22,
	        '00000000000000'  C23 ,'00000000000000'  C24,'00000000000000'  C25 ,'00000000000000'  C26,'0000' C27
	        FROM CMOWNER.PRINTER_MASTER
            WHERE PRINTER_SERIAL_NBR = """ + "'" +  d_sr + "'" +";", con = ctx)
            st.write(df_b)
            df_nb.to_csv("./temp/" + x + ".txt",sep='~', index = False, header = False)
            subprocess.run(["./chksumgencmc7.exe", "./temp/" + d_sr + ".txt","./"])
            os.rename('./chksumgen.txt', './' + x +'.txt')
            os.replace("./genreport.txt", "./genreport/genreport.txt")


			