#Base Image to use
FROM python:3.10-slim

#Expose port 8080
EXPOSE 8080

#Copy Requirements.txt file into app directory


#install all requirements in requirements.txt
RUN pip install -r requirements.txt

#Copy all files in current directory into app directory
COPY . /app

#Change Working Directory to app directory
WORKDIR /app

#Run the application on port 8080
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]