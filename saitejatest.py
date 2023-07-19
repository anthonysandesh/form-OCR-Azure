import json
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import document_analysis_client
from azure.core.credentials import AzureKeyCredential
import os

credentials = json.load(open('credential.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']

client = FormRecognizerClient(ENDPOINT, AzureKeyCredential(API_KEY))

model_id = os.environ["cheque_only_fields"]

formUrl = 'https://eagleeye365ocrstorage.blob.core.windows.net/files/a_resized.jpg'

result = client.begin_recognize_custom_forms_from_url(model_id=model_id, form_url=formUrl).result()

# document_analysis_client = DocumentAnalysisClient(
#     endpoint=endpoint, credential=AzureKeyCredential(key))

poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-invoice", formUrl)
# invoices = poller.result()



# for idx, invoice in enumerate(invoices.documents):
#     print("--------Recognizing invoice #{}--------".format(idx + 1))
#     cheque_no = invoice.fields.get("Check")
#     if cheque_no:
#         print("check number: {}".format(cheque_no.value))
#     cheque_date = invoice.fields.get("ChkDate")
#     if cheque_date:
#         print("cheque date: {}".format(cheque_date.value))
# print("----------------------------------------")

for recognized_form in result:
    for name, field in recognized_form.fields.items():
        print("Field '{}' has value '{}' with a confidence score of {}".format(name, field.value, field.confidence))