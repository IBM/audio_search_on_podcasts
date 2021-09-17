from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from werkzeug.utils import secure_filename
from moviepy.editor import *
from pydub import AudioSegment
import speech_recognition as sr
from ibm_watson import SpeechToTextV1
from os import path
import time
import shutil


''' Initialize Flask Variables '''

app = Flask(__name__)

app.config["CORPUS_UPLOAD"] = "static/raw/"
app.config["AUDIO_UPLOAD"] = "static/audios/"
app.config["TRANSCRIPT_UPLOAD"] = "static/transcripts/"
app.config["COS_TRANSCRIPT"] = "transcript/"
app.config["COS_AUDIOS"] = "audios/"
app.config["CHUNK_FILES"]="static/audios/chunks"

'''Initialize Global Variables'''
global file_name
apikey_discovery='<Enter-Discovery-apikey>'
url_discovery='<Enter-Discovery-url->'
apikey_speech2text='<Enter-Speech2Txt-apikey>'
url_speech2text='<Enter-Speech2Txt-url>'
# Environment Name to create or Existing Environment Name
envname='Podcast_collection'
collection_name='Audio_Podcast_collection'
interval=10*1000

'''Connect to Discovery'''
authenticator = IAMAuthenticator(apikey_discovery)
discovery = DiscoveryV2(
version='2020-08-30',
authenticator=authenticator)
discovery.set_service_url(url_discovery)

# Function that chunks audio files and converts speech to text

def chunk_files(interval, audioname, fname,apikey,url):

    authenticator = IAMAuthenticator(apikey)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(url)
    chunk_storage=dict()
    # Length of the audiofile in milliseconds
    audio = AudioSegment.from_mp3(audioname)
    n = len(audio)

    counter = 1
    # Initialize start and end seconds to 0
    start = 0
    end = 0

    # Flag to keep track of end of file.
    # When audio reaches its end, flag is set to 1 and we break
    flag = 0

    # Iterate from 0 to end of the file,
    # with increment = interval
    for i in range(0, n, interval):

        if i == 0:
            start = 0
            end = interval


        else:
            start = end
            end = start + interval


        if end >= n:
            end = n
            flag = 1

        # Storing audio file from the defined start to end
        chunk = audio[start:end]

        # Filename / Path to store the sliced audio
        filename = fname+str(counter)+'.mp3'

        file_name=os.path.splitext(filename)[0]
        file_name=file_name.split('/')[3]
        chunk_storage[file_name+'.html']=start/1000
        # Store the sliced audio file to the defined path
        chunk.export(filename, format ="mp3")
        # Print information about the current chunk
        print("Processing chunk "+str(counter)+". Start = "
                            +str(start)+" end = "+str(end))




        # Text file to write the recognized audio
        filename_chunked_text = fname+str(counter)+".txt"
        fh = open(filename_chunked_text, "w")

         # Increment counter for the next chunk
        counter = counter + 1

        with open(filename ,'rb') as audio_file:
            speech_recognition_results = speech_to_text.recognize(audio=audio_file, content_type='audio/mp3').get_result()
            print(json.dumps(speech_recognition_results, indent=2))
            chunk_string = ""
            for i in speech_recognition_results["results"]:
                chunk_string = chunk_string + i["alternatives"][0]["transcript"]
            fh.write(chunk_string)
            fh.close()

    return chunk_storage

# Function to convert text file to HTML

def convert_txt_to_html(begin, fpath):
    import os
    print(fpath)
    for file in os.listdir('./'+fpath):
        if file.startswith(begin) and file.endswith(".txt"):
            file_name=os.path.splitext(file)[0]

            with open(fpath+'/'+file,'r') as f:
                with open(fpath+'/'+file_name+".html", "w") as e:
                    for lines in f.readlines():
                        e.write("<pre>" + lines + "</pre> <br>\n")

# Uplad the chunked files to Discovery

def uploadToDiscovery(begin, environ_id, collection_id, fpath):
    import os
    for file in os.listdir(fpath):
        if file.startswith(begin) and file.endswith(".html"):
            with open(fpath+'/'+file) as fileinfo:
                    add_doc = discovery.add_document(
                        environ_id,
                        collection_id,
                        file=fileinfo).get_result()
                    print(json.dumps(add_doc, indent=2))
# Connecto Discovery and create your Environment and Collection

def connectToDiscovery(apikey, url,envname,collection_name,fpath):


    environ=discovery.list_environments().result
    flag=0
    for e in environ['environments']:
        if e['name'] == envname:
            flag=1
            environ_details=e


    if(not flag):
        environ_details=discovery.create_environment(envname).result

    flag=0
    collection=discovery.list_collections(environ_details['environment_id']).result
    for c in collection['collections']:
        if c['name'] == 'Audio_Podcast_collection':
            flag=1
            collection=discovery.delete_collection(environ_details['environment_id'],c['collection_id']).result
            #time.sleep(1)

            collection=discovery.create_collection(environ_details['environment_id'], 'Audio_Podcast_collection').result
            print(collection)
            break

    if(not flag):
        collection=discovery.create_collection(environ_details['environment_id'], 'Audio_Podcast_collection').result
    return environ_details,collection

# Get environment_id and collection_details

def getDiscoveryDetails(apikey_discovery,url_discovery,envname,collection_name):
        environ=discovery.list_environments().result

        for e in environ['environments']:
            if e['name'] == envname:
                environ_details=e
        collection=discovery.list_collections(environ_details['environment_id']).result
        for c in collection['collections']:
            if c['name'] == 'Audio_Podcast_collection':
                flag=1
                collection=discovery.get_collection(environ_details['environment_id'],c['collection_id']).result
        return environ_details,collection


''' Method to handle POST upload '''


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    try:
        if (os.path.exists(app.config["CHUNK_FILES"])):
            shutil.rmtree(app.config["AUDIO_UPLOAD"])
            os.mkdir(app.config["AUDIO_UPLOAD"])
            os.mkdir(app.config["CHUNK_FILES"])

        if (os.path.exists("./chunk_storage.json")):
            os.remove("./chunk_storage.json")
        if request.method == 'POST':
            f = request.files["video"]
            filename_converted = f.filename.replace(
                " ", "-").replace("'", "").lower()

            f.save(os.path.join(
                app.config["AUDIO_UPLOAD"], secure_filename(filename_converted)))

            video = VideoFileClip(os.path.join(os.path.join(app.config["AUDIO_UPLOAD"], secure_filename(filename_converted))))
            raw_name=filename_converted.split('.')
            filename_converted_mp3=raw_name[0]+'.mp3'
            if not path.exists(os.path.join(app.config["AUDIO_UPLOAD"], secure_filename(filename_converted_mp3))):
                video.audio.write_audiofile(os.path.join(app.config["AUDIO_UPLOAD"], secure_filename(filename_converted_mp3)))
            #Delete previous contents if exists


            # Call Chunking Function
            # Chunks the audio file to desired time chunks
            chunk_storage=chunk_files(interval, os.path.join(app.config["AUDIO_UPLOAD"], secure_filename(filename_converted_mp3)),os.path.join(app.config["CHUNK_FILES"], secure_filename('chunk')),apikey_speech2text,url_speech2text)
            chunk_storage_json=dict()

            chunk_storage_json['chunks']=chunk_storage

            # Store the time frame for respective chunks
            with open('chunk_storage.json', 'w') as fp:
                json.dump(chunk_storage_json, fp)

            # Convert generated text files to HTML for Discovery
            convert_txt_to_html("chunk",app.config["CHUNK_FILES"])

            # Setup your Discovery Instance
            environ_details,collection=connectToDiscovery(apikey_discovery,url_discovery,envname,collection_name,app.config["CHUNK_FILES"])
            check=discovery.list_collections(environ_details['environment_id']).result

            uploadToDiscovery('chunk',environ_details['environment_id'],collection['collection_id'],app.config["CHUNK_FILES"])

        myResponse = {
            "filepath": app.config["AUDIO_UPLOAD"]+filename_converted
            }

    except Exception as e:
        print("Unable {0}".format(e))
        myResponse = {"message": str(e)}

    return json.dumps(myResponse, indent=2)

@app.route("/get")
def get_bot_response():

    user_query = request.args.get('msg')
    x=dict()
    with open('chunk_storage.json', 'r') as fp:
        chunk_storage = json.load(fp)

    environ_details,collection=getDiscoveryDetails(apikey_discovery,url_discovery,envname,collection_name)
    query_result=discovery.query(environ_details['environment_id'], collection['collection_id'],query=user_query).result
    q = query_result['results'][0]
    file=q['extracted_metadata']['filename']
    x["text"]=user_query
    x["time"]=chunk_storage['chunks'][file]
    x = json.dumps(x)
    print(x)
    return x

@app.route("/query/<file_path>", methods=['GET', 'POST'])
def display_video(file_path):
    file_path = "/static/audios/" + file_path
    return render_template('query.html', file_path=file_path)


@app.route('/')
def index():
    return render_template('index.html')


port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)
