import re
import pickle
import os
from pypdf import PdfReader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clf = pickle.load(open(os.path.join(BASE_DIR, 'ml_models', 'clf.pkl'), 'rb'))
tfidf = pickle.load(open(os.path.join(BASE_DIR, 'ml_models', 'tfidf.pkl'), 'rb'))

CATEGORY_MAPPING = {
    0: "HR", 1: "DESIGNER", 2: "INFORMATION-TECHNOLOGY", 3: "TEACHER",
    4: "ADVOCATE", 5: "BUSINESS-DEVELOPMENT", 6: "HEALTHCARE", 7: "FITNESS",
    8: "AGRICULTURE", 9: "BPO", 10: "SALES", 11: "CONSULTANT",
    12: "DIGITAL-MEDIA", 13: "AUTOMOBILE", 14: "CHEF", 15: "FINANCE",
    16: "APPAREL", 17: "ENGINEERING", 18: "ACCOUNTANT", 19: "CONSTRUCTION",
    20: "PUBLIC-RELATIONS", 21: "BANKING", 22: "ARTS", 23: "AVIATION",
}

def clean_resume(txt):
    cleanTxt = re.sub(r'http\S+\s', ' ', txt)
    cleanTxt = re.sub(r'@\S+', ' ', cleanTxt)
    cleanTxt = re.sub(r'#\S+\s', ' ', cleanTxt)
    cleanTxt = re.sub(r'RT|CC', ' ', cleanTxt)
    cleanTxt = re.sub('[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_'{|}~"""), ' ', cleanTxt)
    cleanTxt = re.sub(r'[^\x00-\x7f]', ' ', cleanTxt)
    cleanTxt = re.sub(r'\s+', ' ', cleanTxt)
    return cleanTxt.strip()

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def classify_resume(resume_text):
    cleaned = clean_resume(resume_text)
    vector = tfidf.transform([cleaned])
    prediction_id = clf.predict(vector)[0]

    try:
        proba = clf.predict_proba(vector)[0]
        confidence = float(proba[prediction_id])
    except AttributeError:
        confidence = None

    category_name = CATEGORY_MAPPING.get(prediction_id, "Unknown")
    return category_name, confidence