FROM node 

WORKDIR /app

COPY . ./  
# the above is same as COPY . /app 

RUN npm install 

EXPOSE 80

CMD ["node", "server.js"]

