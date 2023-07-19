import json
import os
from datetime import date
from json import JSONEncoder
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormField
from azure.ai.formrecognizer import FieldData

credentials = json.load(open('credential.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']
form_recognizer_client = FormRecognizerClient(ENDPOINT, AzureKeyCredential(API_KEY))

# intone image
invoice_url = 'https://eagleeye365ocrstorage.blob.core.windows.net/files/a_resized.jpg'

#online pdf
#invoice_url = 'https://slicedinvoices.com/pdf/wordpress-pdf-invoice-plugin-sample.pdf'

#online image
#invoice_url = 'https://freeinvoicebuilder.com/wp-content/uploads/2022/01/it-services-564x804.jpg'

class FormFieldEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FormField):
            if isinstance(obj.value, date):
                return obj.value.isoformat()
            else:
                return {'value': obj.value}
        elif isinstance(obj, FieldData):
            return {'text': obj.text, 'page': obj.page_number}
            
        return super().default(obj)


poller = form_recognizer_client.begin_recognize_invoices_from_url(invoice_url)
result = poller.result()


res = (result[0].fields)
with open('test_invoice_fields.json', 'w') as outfile:
      json.dump(res, outfile, indent=2, cls=FormFieldEncoder)
