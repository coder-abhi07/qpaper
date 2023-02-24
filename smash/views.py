# from django.shortcuts import render
# import requests
# from django.http import HttpResponse
# from kneed import KneeLocator

# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import CountVectorizer
# import joblib 

# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings
# from kneed import KneeLocator
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import CountVectorizer
# import joblib 

# def upload_file(request):
#     result = ''
#     if request.method == 'POST':
#         files = request.FILES.getlist('file')
#         ocr_results = []
#         for file in files:
#             # send file to OCR.Space API and get response
#             response = ocr_space(file)
#             ocr_results.append(response)
#         # concatenate OCR results into a single string
#         result = ''.join(ocr_results)
#         # render result in template
#         return render(request, 'index.html', {'result': result})
#     return render(request, 'upload.html')



# def ocr_space(file):
#     api_key = 'K86627853288957'
#     endpoint = 'https://api.ocr.space/parse/image'
#     payload = {

#         'apikey': api_key,
#         'OCREngine' : 5,
#         'isTable' : True,
#     }
#     files = {'image': (file.name, file.read(), file.content_type)}
#     response = requests.post(endpoint, data=payload, files=files)
#     result = response.json()

#     if result['IsErroredOnProcessing']:
#         raise Exception(result['ErrorMessage'])
#     text_data = ''
#     for result in result['ParsedResults']:
#         text_data += result['ParsedText']
#     return text_data




# def load_and_predict(request):
#     # Load the machine learning model
#     model = joblib.load('static/kmeans_model.pkl')
#     question = upload_file()
#     # Use the loaded model to perform predictions
#     vectorizer = CountVectorizer()
#     X = vectorizer.fit_transform([question])
#     cluster = model.predict(X)[0]

#     return cluster

# def index(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filepath = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filepath)
#         file = open(settings.MEDIA_ROOT + '/' + myfile.name, 'r')
#         question = file.read().replace('\n', '')
#         file.close()

#         # Use the machine learning model to predict the cluster of the given question
#         cluster = load_and_predict(question)

#         return render(request, 'index.html', {'cluster': cluster})
#     return render(request, 'upload.html')


from django.shortcuts import render
from django.conf import settings
import requests
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster

stemmer = PorterStemmer()
sw = stopwords.words('english')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def tokenizer(keyword):
    return [stemmer.stem(w) for w in keyword.split()]

def upload(request):
    if request.method == 'POST' and request.FILES.getlist('myfile'):
        # Upload files to OCR.space and parse the results
        parsed_text = []
        api_key = settings.OCR_API_KEY  # Replace with your OCR.space API key
        payload = {
        'apikey': api_key,
        'OCREngine': 5,
        'isTable': True
        }
        
        for file in request.FILES.getlist('myfile'):
            response = requests.post('https://api.ocr.space/parse/image',
                                     files={file.name: file},
                                     data=payload)
            result = response.json()
            for result in result['ParsedResults']:
                parsed_text.append(result['ParsedText'])
        

        # Use the parsed text to predict the clusters
        tfidf = TfidfVectorizer(tokenizer=tokenizer, stop_words=sw)
        X = pd.DataFrame(tfidf.fit_transform(parsed_text).toarray(),
                         index=parsed_text, columns=tfidf.get_feature_names_out())
        c = cluster.AffinityPropagation()
        pred = c.fit_predict(X)

        # Pass the questions and predicted clusters to the index.html template
        questions = parsed_text
        clusters = pred.tolist()
        return render(request, 'index.html', {'questions': questions, 'clusters': clusters})

    return render(request, 'upload.html')
