from pypdf import PdfReader
import requests
import time

print('| PDF to Speech/Audio Converter v. 0.1. Needs internet connection')
print('| Extracts text and gets audiobook in WAV file via API ')
print('| Usage: filename.pdf')
print('| Where filename.pdf is a file within the app directory!')
print('| Remember to use your RapidAPI account!')
print('------------------------------------------------------')

filename = input('Write filename with extension (i.e. myfile.pdf): ')
try:
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text_from_pdf = page.extract_text()
except FileNotFoundError:
    print('No proper file!')
else:
    print('PDF file parsed. Converting to audio file')
    print('...wait...')

# ============ send text to TTS engine ------------------

url = "https://large-text-to-speech.p.rapidapi.com/tts"

payload = {"text": text_from_pdf}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "ENTER-YOUR-RAPIDAPI-KEY-TO-USE-APP!",
    "X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com"
}
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
except ConnectionError:
    print('Connection problems. Cannot process file. Quitting')
else:
    job_id = response.json()["id"]
    job_eta = response.json()["eta"]


#  ------------ get audio file --------------------


querystring = {"id":job_id}

headers = {
    "X-RapidAPI-Key": "ENTER-YOUR-RAPIDAPI-KEY-TO-USE-APP!",
    "X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com"
}

try:
    time.sleep(job_eta + 1)
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
except ConnectionError:
    print('Connection problems. Cannot receive audio file. Quitting')
else:
    file_url = response.json()["url"]
    file_response = requests.get(file_url, stream=True)
    wave_filename = filename + '.wav'
    with open(wave_filename, mode="wb") as file:
        for chunk in file_response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
    print(f"File <{wave_filename}> saved successfully!")
