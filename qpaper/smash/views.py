from django.shortcuts import render
import requests
from django.http import HttpResponse




# def toText(request, language = 'eng', overlay = False):

#     api_key = 'K86627853288957'
#     url = 'https://api.ocr.space/parse/image'
    
    
#     if request.method == 'POST' and request.FILES['pdf_file']:

#         pdf_file = request.FILES['pdf_file']
#         file_content = open(pdf_file, 'rb')

#         payload = {
#             'apikey': api_key,
#             'language': 'eng',
#             'isOverlayRequired': False,
#             'OCREngine': 5,
#             'filename': pdf_file.name,
#             'isTable' : True,
#         }

#         response = requests.post(url, data=payload, files={pdf_file.name: file_content})

#         if response.status_code == 200:
#             response_data = response.json()
#             text_data = ''
#             for result in response_data['ParsedResults']:
#                 text_data += result['ParsedText']
#             response = HttpResponse(text_data, content_type='text/plain')
        

#     return render(request, 'process_pdf.html')

def ocr_space(file):
    api_key = 'K86627853288957'
    endpoint = 'https://api.ocr.space/parse/image'
    payload = {

        'apikey': api_key,
        'OCREngine' : 5,
        'isTable' : True,
    }
    files = {'image': (file.name, file.read(), file.content_type)}
    response = requests.post(endpoint, data=payload, files=files)
    result = response.json()

    if result['IsErroredOnProcessing']:
        raise Exception(result['ErrorMessage'])
    text_data = ''
    for result in result['ParsedResults']:
        text_data += result['ParsedText']
    return text_data


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # send file to OCR.Space API and get response
        response = ocr_space(file)
        # render result in template
        return render(request, 'index.html', {'result': response})
    return render(request, 'upload.html')

