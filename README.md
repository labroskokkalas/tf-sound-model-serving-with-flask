Template for serving a tensorflow model with a sound file as input with flask

Can be used for sound event detection

STEPS :

1. export model to 'tensorflow-server' directory 

     python export_model.py
	 
2. run docker in terminal
     docker run -t --rm -p 8501:8501 -v "tensorflow-server:/models/test" -e MODEL_NAME=test tensorflow/serving	 
	 
	 
3. run flask server that serves the model  

     python app.py	 

4. test flask server from URL or command line 

     curl 127.0.0.1:5000 -X POST -F files=@1.wav -F files=@2.wav -F files=@3.wav  

