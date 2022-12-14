import streamlit as st
import pandas as pd
import numpy as np
import csv
from io import StringIO
import datetime
import re

tomorrow_date= datetime.date.today() + datetime.timedelta(days = 1)
tomorrow = datetime.date.strftime(tomorrow_date, "%m/%d/%Y")

sdc_columns = [  'SHIPMENT_PACKAGE_IDENTIFIER*', 'SHIPPER_ADDRESS_CONTACT_NAME*'\
               , 'SHIPMENT_READY_DATE_MM_DD_YYYY*', 'SHIPMENT_READY_TIME_HH_MM*'\
               , 'SHIPPER_TIME_ZONE*', 'SHIPPER_ADDRESS_COMPANY_NAME'\
               , 'SHIPPER_ADDRESS*', 'SHIPPER_ADDRESS_APT_FLOOR_SUITE'\
               , 'SHIPPER_ADDRESS_CITY*', 'SHIPPER_ADDRESS_STATE*'\
               , 'SHIPPER_ADDRESS_ZIP*', 'SHIPPER_ADDRESS_PHONE*'\
               , 'SHIPPER_ADDRESS_SPECIAL_INSTRUCTIONS', 'SHIPPER_ADDRESS_NOTIFICATION_EMAIL'\
               , 'SHIPPER_ADDRESS_EMAIL_NOTIFICATION_OPT_IN', 'SHIPPER_ADDRESS_PHONE_NOTIFICATION_OPT_IN'\
               , 'SHIPPER_THIS_IS_RESIDENTIAL_ADDRESS', 'SHIPPER_ADDRESS_OPEN_TIME'\
               , 'SHIPPER_ADDRESS_CLOSE_TIME', 'RECIPIENT_ADDRESS_CONTACT_NAME*'\
               , 'RECIPIENT_ADDRESS_COMPANY', 'RECIPIENT_ADDRESS*', 'RECIPIENT_ADDRESS_APT_FLOOR_SUITE'\
               , 'RECIPIENT_ADDRESS_CITY*', 'RECIPIENT_ADDRESS_STATE*', 'RECIPIENT_ADDRESS_ZIP*'\
               , 'RECIPIENT_ADDRESS_PHONE*', 'RECIPIENT_ADDRESS_SPECIAL_INSTRUCTIONS'\
               , 'RECIPIENT_ADDRESS_NOTIFICATION_EMAIL', 'RECIPIENT_ADDRESS_EMAIL_NOTIFICATION_OPT_IN'\
               , 'RECIPIENT_ADDRESS_PHONE_NOTIFICATION_OPT_IN', 'RECIPIENT_THIS_IS_RESIDENTIAL_ADDRESS'\
               , 'RECIPIENT_ADDRESS_OPEN_TIME', 'RECIPIENT_ADDRESS_CLOSE_TIME', 'SHIPMENT_DECLARED_VALUE*'\
               , 'SIGNATURE_SERVICE*', 'SHIPMENT_SPECIAL_SERVICES', 'SHIPMENT_SERVICE_TYPE*'\
               , 'SHIPMENT_REFERENCE_PO_NUMBER', 'SHIPMENT_REFERENCE_DEPT_NUMBER'\
               , 'SHIPMENT_REFERENCE_RMA_NUMBER', 'SHIPMENT_REFERENCE_INVOICE_NUMBER'\
               , 'SHIPMENT_REFERENCE_OTHER', 'IDENTICAL_PACKAGE_COUNT*', 'PACKAGE_LENGTH*'\
               , 'PACKAGE_WIDTH*', 'PACKAGE_HEIGHT*', 'PACKAGE_WEIGHT*', 'HAZMAT_PACKAGE_TYPE**'\
               , 'HAZMAT_COMMODITIES_ID_TYPE**', 'HAZMAT_COMMODITIES_ID_NUMBER**'\
               , 'HAZMAT_COMMODITIES_DOT_SHIPPING_NM**', 'HAZMAT_COMMODITIES_TECHNICAL_NAME'\
               , 'HAZMAT_COMMODITIES_PACKAGING_GROUP', 'HAZMAT_COMMODITIES_TYPE_DOT_LABELS'\
               , 'HAZMAT_COMMODITIES_WEIGHT_LBS**', 'HAZMAT_COMMODITIES_PRIMARY_CLASS**'\
               , 'HAZMAT_COMMODITIES_SUBSIDIARY_CLASSES', 'HAZMAT_RADIOACTIVE_TRANSPORT_INDEX'\
               , 'HAZMAT_RADIOACTIVE_SURFACE_READING', 'HAZMAT_RADIOACTIVE_CRITICALITY_SAFETY_INDEX'\
               , 'HAZMAT_RADIOACTIVE_LABEL_TYPE', 'HAZMAT_RADIOACTIVE_RADIONUCLIDES'\
               , 'HAZMAT_RADIOACTIVE_ACTIVITY_VALUE', 'HAZMAT_RADIOACTIVE_ACTIVITY_UNITOFMEASURE'\
               , 'HAZMAT_RADIOACTIVE_PHYSCIAL_FORM', 'HAZMAT_RADIOACTIVE_CHEMICAL_FORM'\
               , 'OFFEROR_NAME**', 'NAME_OF_SIGNATORY', 'EMERGENCY_CONTACT_NUMBER**'
               ]
    
sdc_zip_codes = ['38002', '38004', '38011', '38014', '38015', '38016', '38017', '38018', '38023', '38027',\
                 '38028', '38029', '38053', '38054', '38058', '38060', '38066', '38071', '38083', '38088',\
                 '38101', '38103', '38104', '38105', '38106', '38107', '38108', '38109', '38111', '38112',\
                 '38113', '38114', '38115', '38116', '38117', '38118', '38119', '38120', '38122', '38124',\
                 '38125', '38126', '38127', '38128', '38130', '38131', '38132', '38133', '38134', '38135',\
                 '38136', '38137', '38138', '38139', '38141', '38145', '38147', '38148', '38150', '38151',\
                 '38152', '38157', '38159', '38163', '38166', '38167', '38168', '38173', '38174', '38175',\
                 '38177', '38181', '38182', '38183', '38184', '38186', '38187', '38188', '38190', '38193',\
                 '38194', '38197', '38611', '38632', '38637', '38641', '38651', '38654', '38664', '38671',\
                 '38672', '38680', '38686', '72301', '72303', '72313', '72320', '72325', '72327', '72329',\
                 '72331', '72332', '72338', '72339', '72346', '72348', '72350', '72364', '72373', '72376',\
                 '72384', '72386']
    
default_sdc_columns = {'SHIPMENT_PACKAGE_IDENTIFIER*': 'S',
        'SHIPPER_ADDRESS_CONTACT_NAME*': 'HOME PLACE PASTURES',
        'SHIPMENT_READY_DATE_MM_DD_YYYY*': tomorrow,
        'SHIPMENT_READY_TIME_HH_MM*': '10:00',
        'SHIPPER_TIME_ZONE*': 'US/Central',
        'SHIPPER_ADDRESS_COMPANY_NAME': 'FEDEX CPC',
        'SHIPPER_ADDRESS*': '3041 Millbranch Rd',
        'SHIPPER_ADDRESS_APT_FLOOR_SUITE': np.nan,
        'SHIPPER_ADDRESS_CITY*': 'MEMPHIS',
        'SHIPPER_ADDRESS_STATE*': 'TN',
        'SHIPPER_ADDRESS_ZIP*': 38116,
        'SHIPPER_ADDRESS_PHONE*': 8289896049,
        'SHIPPER_ADDRESS_SPECIAL_INSTRUCTIONS': np.nan,
        'SHIPPER_ADDRESS_NOTIFICATION_EMAIL': 'info@homeplacepastures.com',
        'SHIPPER_ADDRESS_EMAIL_NOTIFICATION_OPT_IN': 'N',
        'SHIPPER_ADDRESS_PHONE_NOTIFICATION_OPT_IN': 'N',
        'SHIPPER_THIS_IS_RESIDENTIAL_ADDRESS': 'N',
        'SHIPPER_ADDRESS_OPEN_TIME': '7:00',
        'SHIPPER_ADDRESS_CLOSE_TIME': '20:00',
        'RECIPIENT_ADDRESS_COMPANY': np.nan,
        'RECIPIENT_ADDRESS_SPECIAL_INSTRUCTIONS': np.nan,
        'RECIPIENT_ADDRESS_EMAIL_NOTIFICATION_OPT_IN': 'Y',
        'RECIPIENT_ADDRESS_PHONE_NOTIFICATION_OPT_IN': 'Y',
        'RECIPIENT_THIS_IS_RESIDENTIAL_ADDRESS': 'Y',
        'RECIPIENT_ADDRESS_OPEN_TIME': np.nan,
        'RECIPIENT_ADDRESS_CLOSE_TIME': np.nan,
        'SHIPMENT_DECLARED_VALUE*': 150,
        'SIGNATURE_SERVICE*': 'SR',
        'SHIPMENT_SPECIAL_SERVICES': 'SAME_DAY_RETURN_TO_SENDER',
        'SHIPMENT_SERVICE_TYPE*': 'EC',
        'SHIPMENT_REFERENCE_PO_NUMBER': np.nan,
        'SHIPMENT_REFERENCE_DEPT_NUMBER': np.nan,
        'SHIPMENT_REFERENCE_RMA_NUMBER': np.nan,
        'SHIPMENT_REFERENCE_INVOICE_NUMBER': np.nan,
        'SHIPMENT_REFERENCE_OTHER': np.nan,
        'IDENTICAL_PACKAGE_COUNT*': 1,
        'PACKAGE_LENGTH*': 18,
        'PACKAGE_WIDTH*': 16,
        'PACKAGE_HEIGHT*': 16,
        'PACKAGE_WEIGHT*': 30,
        'HAZMAT_PACKAGE_TYPE**': np.nan,
        'HAZMAT_COMMODITIES_ID_TYPE**': np.nan,
        'HAZMAT_COMMODITIES_ID_NUMBER**': np.nan,
        'HAZMAT_COMMODITIES_DOT_SHIPPING_NM**': np.nan,
        'HAZMAT_COMMODITIES_TECHNICAL_NAME': np.nan,
        'HAZMAT_COMMODITIES_PACKAGING_GROUP': np.nan,
        'HAZMAT_COMMODITIES_TYPE_DOT_LABELS': np.nan,
        'HAZMAT_COMMODITIES_WEIGHT_LBS**': np.nan,
        'HAZMAT_COMMODITIES_PRIMARY_CLASS**': np.nan,
        'HAZMAT_COMMODITIES_SUBSIDIARY_CLASSES': np.nan,
        'HAZMAT_RADIOACTIVE_TRANSPORT_INDEX': np.nan,
        'HAZMAT_RADIOACTIVE_SURFACE_READING': np.nan,
        'HAZMAT_RADIOACTIVE_CRITICALITY_SAFETY_INDEX': np.nan,
        'HAZMAT_RADIOACTIVE_LABEL_TYPE': np.nan,
        'HAZMAT_RADIOACTIVE_RADIONUCLIDES': np.nan,
        'HAZMAT_RADIOACTIVE_ACTIVITY_VALUE': np.nan,
        'HAZMAT_RADIOACTIVE_ACTIVITY_UNITOFMEASURE': np.nan,
        'HAZMAT_RADIOACTIVE_PHYSCIAL_FORM': np.nan,
        'HAZMAT_RADIOACTIVE_CHEMICAL_FORM': np.nan,
        'OFFEROR_NAME**': np.nan,
        'NAME_OF_SIGNATORY': np.nan,
        'EMERGENCY_CONTACT_NUMBER**': 8289896049}

mapping_dict =  {
                  'Email'             : 'RECIPIENT_ADDRESS_NOTIFICATION_EMAIL'
                 ,'Shipping Name'     : 'RECIPIENT_ADDRESS_CONTACT_NAME*'
                 ,'Shipping Address1' : 'RECIPIENT_ADDRESS*'
                 ,'Shipping Address2' : 'RECIPIENT_ADDRESS_APT_FLOOR_SUITE'
                 ,'Shipping City'     : 'RECIPIENT_ADDRESS_CITY*'
                 ,'Shipping Province' : 'RECIPIENT_ADDRESS_STATE*'
                 ,'Shipping Zip'      : 'RECIPIENT_ADDRESS_ZIP*'
                 ,'Shipping Phone'    : 'RECIPIENT_ADDRESS_PHONE*'
                }
    
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index = False).encode('utf-8')
 
today = str(datetime.date.today())

#@st.cache
st.title('Same Day City Data Cleanse')

uploaded_file = st.file_uploader("Choose Shopify .csv File")
if uploaded_file is not None:
    #bytes_data = uploaded_file.getvalue()
    #with open(bytes_data, "r") as f:
    dataframe = pd.read_csv(uploaded_file)
    string_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
    csv_reader = csv.reader(string_data)
    shopify_lists = list(csv_reader)
    shopify_dictionary = {z[0]: list(z[1:]) for z in zip(*shopify_lists)} 
    #clean up weird shit from shopify
    #first apostrophe before zip
    shopify_dictionary['Shipping Zip'] = [zip_code.replace("'", '')[:5] for zip_code in shopify_dictionary['Shipping Zip']]
    #do I need to clean the shipping address2 to only be numbers?
    shopify_dictionary['Shipping Phone'] = [(re.sub("[^0-9]", "", number))[-10:] for number in shopify_dictionary['Shipping Phone']]
    #build new dictionary
    export_dictionary = {value : shopify_dictionary[key] for key, value in mapping_dict.items()}
    export_df = pd.DataFrame(export_dictionary).replace('', np.nan)\
                               .dropna(subset = [
                                                   'RECIPIENT_ADDRESS_CONTACT_NAME*'
                                                  ,'RECIPIENT_ADDRESS*'
                                                  ,'RECIPIENT_ADDRESS_CITY*'
                                                  ,'RECIPIENT_ADDRESS_STATE*'
                                                  ,'RECIPIENT_ADDRESS_ZIP*'                                                                                                                             
                                                                    ]
                                   ,how = 'all')
                               
    export_df = export_df[export_df['RECIPIENT_ADDRESS_ZIP*'].isin(sdc_zip_codes)]
    
    for key, value in default_sdc_columns.items():
        export_df[key] = value
    
    export_df = export_df[sdc_columns]
    export_df.fillna('N/A', inplace = True)

    st.write(export_df)
    csv_output = convert_df(export_df)
    st.download_button(
     label="Download Cleansed Data for Same Day City",
     data=csv_output,
     file_name='SameDayCity_' + today + '.csv',
     mime='text/csv',
 )
    
    























































