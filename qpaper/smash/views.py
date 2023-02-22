from django.shortcuts import render
import requests
from django.http import HttpResponse




def toText(request, language = 'eng', overlay = False):

    api_key = 'K86627853288957'
    url = 'https://api.ocr.space/parse/image'
    
    
    if request.method == 'POST' and request.FILES['pdf_file']:

        pdf_file = request.FILES['pdf_file']
        file_content = open(pdf_file, 'rb')

        payload = {
            'apikey': api_key,
            'language': 'eng',
            'isOverlayRequired': False,
            'OCREngine': 5,
            'filename': pdf_file.name,
            'isTable' : True,
        }

        response = requests.post(url, data=payload, files={pdf_file.name: file_content})

        if response.status_code == 200:
            response_data = response.json()
            text_data = ''
            for result in response_data['ParsedResults']:
                text_data += result['ParsedText']
            response = HttpResponse(text_data, content_type='text/plain')
        

    return render(request, 'process_pdf.html')
