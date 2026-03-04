import streamlit as st
import pandas as pd
import os

st.title("Medical Claim Validation System")

employee_master = pd.read_excel("Final Master ONGC.xlsx", dtype=str)
reference_master = pd.read_excel("Reference No Master.xlsx", dtype=str)

employee_master_clean = employee_master[['CPF Number','Medical Card Number']]

employee_master_clean = employee_master_clean.rename(columns={
    'CPF Number':'CPF NO',
    'Medical Card Number':'MEDICAL CARD NO'
})

reference_master_clean = reference_master[['REFERENCE NO']]

if os.path.exists("history.xlsx"):
    history = pd.read_excel("history.xlsx", dtype=str)
else:
    history = pd.DataFrame(columns=["REFERENCE NO"])

uploaded_file = st.file_uploader("Upload Claim Excel File")

if uploaded_file:

    upload = pd.read_excel(uploaded_file, dtype=str)

    remarks=[]

    duplicate_refs = upload['REFERENCE NO'][upload['REFERENCE NO'].duplicated()].tolist()

    for index,row in upload.iterrows():

        cpf=row['CPF NO']
        card=row['MEDICAL CARD NO']
        ref=row['REFERENCE NO']

        emp_match = employee_master_clean[
            (employee_master_clean['CPF NO']==cpf) &
            (employee_master_clean['MEDICAL CARD NO']==card)
        ]

        ref_match = reference_master_clean[
            reference_master_clean['REFERENCE NO']==ref
        ]

        if emp_match.empty:
            remarks.append("CPF / Medical Card mismatch")

        elif ref_match.empty:
            remarks.append("Reference not in master")

        elif ref in duplicate_refs:
            remarks.append("Duplicate reference in same file")

        elif ref in history["REFERENCE NO"].values:
            remarks.append("Duplicate reference used earlier")

        else:
            remarks.append("OK")

    upload["REMARK"]=remarks

    upload.to_excel("validated_output.xlsx", index=False)

    st.success("Validation Completed")

    st.download_button(
        "Download Checked File",
        data=open("validated_output.xlsx","rb"),
        file_name="validated_output.xlsx"
    )

    history=pd.concat([history,upload[['REFERENCE NO']]])
    history.to_excel("history.xlsx",index=False)