Welcome to the audio_search_on_podcasts wiki!
# Short title
​A Python Flask Audio Search Application.


# Long title
​
Create a Python Flask Audio Search Application with Watson Speech to Text and Watson Discovery.
​
# Author
​* Neha <neha1221@in.ibm.com>
* Smruthi Raj Mohan <smrraj32@in.ibm.com>
* Rahul Reddy Ravipally  <raravi86@in.ibm.com>
​
# URLs
​
### Github repo
​
* https://github.com/IBM/audio_search_on_podcasts/
​
### Other URLs
​
* Video URL
* Demo URL
​
# Summary
​Often while listening to a Podcast or probably listening to a course video/audio files, we might want to straight jump to the topic of our interest rather than going through the entire recording again and again. But finding the topics and keywords in the entire recording could be challenging.

In this code pattern, we will create an application with which you can search within the video/audio files. Not only search but it will highlight the part where Search String/Topic is occurring in the video/audio. This code pattern will perform Natural language query search in audio files and get back with the results with the proper time frame where your search is being talked about.

# Technologies
​
* Analytics
* Artificial Intelligence
​
# Description
Often while listening to a Podcast or probably listening to a course video/audio files, we might want to straight jump to the topic of our interest rather than going through the entire recording again and again. But finding the topics and keywords in the entire recording could be challenging. 

In this code pattern, we will create an application with which you can search within the video/audio files. Not only search but it will highlight the part where `Search String/Topic` is occurring in the video/audio. This code pattern will perform  Natural language query search in audio files and get back with the results with the proper time frame where your search is being talked about.  

In this example, we will use a [Watson Machine Learning Introduction Video](https://github.com/IBM/audio_search_on_podcasts/blob/master/video/watson_studio_tutorial_part1.mp4) to illustrate the process.

When the reader has completed this code pattern, they will understand how to:

* Prepare audio/video data and perform chunking to break it into smaller chunks to work with.
* Work with the `Watson Speech to Text` service through API calls to convert audio/video to text.
* Work with the `Watson Discovery` service through API calls to perform a search on text chunks.
* Create a python flask Application and deploy it on IBM Cloud.

​
# Flow

1. The user uploads the video/audio file on the UI.
2. The Video/Audio is processed with python libraries moviepy and pydub and perform chunking on them to convert it into smaller chunks to work with.
3. The user interacts with the Watson Speech to Text service via the provided application UI. The Audio chunks are converted into text chunks with Watson's Speech to Text.
4. The text chunks are uploaded on Watson Discovery by calling Discovery APIs with python SDKs.
5. The user hit a search query using Discovery.
6. The results are shown on the UI.
​
​
# Instructions
​
1. Prepare audio/video data and perform chunking to break it into smaller chunks to work with.
2. Work with the Watson Speech to Text service through API calls to convert audio/video to text.
3. Work with the Watson Discovery service through API calls to perform a search on text chunks.
4. Create a python flask application and deploy it on IBM Cloud.
​
# Components and services

## Included components

* [IBM Watson Speech to Text](https://www.ibm.com/watson/services/speech-to-text): easily convert audio and voice into written text for quick understanding of content.
* [IBM Watson Discovery](https://developer.ibm.com/articles/introduction-watson-discovery/):  IBM Watson Discovery, you can ingest, normalize, enrich, and search your unstructured data (JSON, HTML, PDF, Word, and more) with speed and accuracy.

## Featured technologies

* [Python Flask](https://flask.palletsprojects.com/en/1.1.x/): Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
* [IBM Watson Speech to Text](https://www.ibm.com/watson/services/speech-to-text): easily convert audio and voice into written text for quick understanding of content.
* [IBM Watson Discovery](https://developer.ibm.com/articles/introduction-watson-discovery/):  IBM Watson Discovery, you can ingest, normalize, enrich, and search your unstructured data (JSON, HTML, PDF, Word, and more) with speed and accuracy.

# Announcement
Ever felt like searching within Podcasts or News so you don't have to listen to the entire audio. Well, we have a solution for you. Our Application can search within the podcasts or any audio file. Not only search but it will highlight the part where `Search String/Topic` is occurring in the video/audio. This code pattern will perform  Natural language query search in audio files and get back with the results with the proper time frame where your search is being talked about.  

In this example, we will use a [Watson Machine Learning Introduction Video](https://github.com/IBM/audio_search_on_podcasts/blob/master/video/watson_studio_tutorial_part1.mp4) to illustrate the process.

When the reader has completed this code pattern, they will understand how to:

* Prepare audio/video data and perform chunking to break it into smaller chunks to work with.
* Work with the `Watson Speech to Text` service through API calls to convert audio/video to text.
* Work with the `Watson Discovery` service through API calls to perform a search on text chunks.
* Create a python flask application and deploy it on IBM Cloud.
