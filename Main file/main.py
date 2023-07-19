import json
import os
from datetime import date
from json import JSONEncoder
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormField
credentials = json.load(open('credential.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']
form_recognizer_client = FormRecognizerClient(ENDPOINT, AzureKeyCredential(API_KEY))

## for testing in local files ###
# invoice_path = 'a_resized.jpg'
# with open(invoice_path, "rb") as f:
#     poller = form_recognizer_client.begin_recognize_invoices(f)
#     result = poller.result()
########################################

# intone image
#invoice_url = 'https://eagleeye365ocrstorage.blob.core.windows.net/files/a_resized.jpg'

# online image
invoice_url = 'https://freeinvoicebuilder.com/wp-content/uploads/2022/01/it-services-564x804.jpg'

poller = form_recognizer_client.begin_recognize_invoices_from_url(invoice_url)
result = poller.result()

result[0].fields.keys()


# class FormFieldEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, FormField):
#             if isinstance(obj.value, date):
#                 return obj.value.isoformat()
#             else:
#                 return {'value': obj.value, 'confidence': obj.confidence}
#         return super().default(obj)

# class FormFieldEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, FormField):
#             if isinstance(obj.value, date):
#                 return obj.value.isoformat()
#             else:
#                 return obj.value
#         return super().default(obj)
    
class FormFieldEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FormField):
            return {'value': obj.value}
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)

def extract_invoice_field_value(invoice, field_name):
    try:
        if field_name == 'Items':
            for item in invoice.fields.get('Items').value:
                for key in item.value.keys():
                    print('\t' + str(key))
                    print('-'*25)
                    print('\t' + str(item.value.get(key).value) + '|' + str(item.value.get(key).confidence))
                    print()
        else:
            print(field_name)
            print('-'*25)
            print(str(invoice.fields.get(field_name).value) + '|' + str(invoice.fields.get(field_name).confidence))
    except AttributeError:
        print('Nothing is found')

if poller.status() == 'succeeded':
    invoice_fields = {}
    for page in result:
        field_keys = page.fields.keys()
        # for field_key in field_keys:
        #     extract_invoice_field_value(page, field_key) 
        for field_key in page.fields.keys():
            # Extract the field value and confidence score
            field_value = page.fields.get(field_key).value
            confidence = page.fields.get(field_key).confidence

            # Store the field value and confidence score in the dictionary
            invoice_fields[field_key] = {'value': field_value, 'confidence': confidence}

# Convert FormField object to dictionary
result_json = json.dumps(result[0].fields, cls=FormFieldEncoder)
result_dict = json.loads(result_json)


# # Write the modified dictionary to a JSON file
with open('img_invoice_fields.json', 'w') as outfile:
     json.dump(result_dict, outfile, indent=2)