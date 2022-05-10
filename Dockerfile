FROM ubuntu

COPY . .

RUN apt-get update -y 
RUN apt-get install -y python3 && apt install p7zip-rar p7zip-full -y
RUN apt-get install python3-pip -y
RUN apt-get install bash wget curl -y
RUN curl https://rclone.org/install.sh | bash
RUN apt install ffmpeg -y



RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["bash", "start.sh"]