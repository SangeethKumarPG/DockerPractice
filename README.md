# Docker
A Docker file is used to create a template for the image. For this we create a Dockerfile in the particular folder of our project. inside this we need to specify a base image. this base image maybe an image present in the docker hub or something that is cached locally(if you have used docker pull). we use the FROM <image-name> for this. then we specify a working directory if we need one. we use WORKDIR <path> to specify this. Then we have to copy the files to the working directory. all the commands are being run in the working directory. so once working directory is specified we can easily run the required commands on the working directory. 

COPY <source> <destination> command is used to copy files from a source folder in the image to the destination folder in the image. '.' specifies the root folder. To run commands in the docker image i.e commands to setup the environment we use the RUN command. to execute or run certain things inside the container once the image is ready we use CMD command. the syntax is CMD\['command','seperated","by","comma","and","doublequotes"\]. the spaces are seperated by comma and commands are wrapped in double quotes. and everything is enclosed in \[\] brackets.

The EXPOSE <port> is a command used to expose a port to the system outside the container(the system that is running the container). this is done after the image is ready. the CMD commands must be last in the docker file. 

docker build is a terminal command which creates a docker image based on the docker file. docker build will create a new image. 

` docker build . ` indicates to build an image where the dockerfile is present in the same folder. 

after you run the above command all the commands required for building the docker image will be run. then you need to run `docker images` to get the image id of the newly created image. to run the container use `docker run <imageid>` . this will run the image but the application will not be accessible to outside the container. for this we need to use `docker run -p <localport:internalport> imageid` this specifies that it will expose the application to localhost port 3000 in the system that runs the container, where the internal port is 80\. the -p indicates publish.

  
eg: docker run -p 3000:80 f0e9363347d8

`docker ps` will list all docker runnning processes. `docker ps -a` will show all docker processes. `docker stop <containername>` will stop the container. the containername is present at the last column and it is assigned automatically.

  
You can also **just use the first (few) character(s)** \- just enough to have a unique identifier.

So instead of

```javaScript
docker run abcdefg
```

you could also run

```javaScript
docker run abc
```

or, if there's no other image ID starting with "a", you could even run just:

```javaScript
docker run a
```

**This applies to ALL Docker commands where IDs are needed.**

  
**Images are read only. Once you create an image all the code and the files are moved into the file system of the image which is 'app' here. any changes you apply to the local files are not reflected to the files in the image file system unless you rebuild the image.**

Images are layerbased. **Once you make a change in the file and build it. only the changes that we make(the docker instruction corresponding to the change such as copying the source file to the image filesystem etc) and the further instructions are evaluated again even if there are no changes in the subsequent docker instruction they are executed again.** if there are no changes when you run docker build the docker engine uses caching because there is no need to run the build again as there are no changes. in an image every instruction in the docker file creates a layer. when you run a container on the image it adds an extra layer over the image. the last layer becomes active when you run the image as a layer(the command that runs when you run the image). 

**NOTE that the files are not actually not copied over from one folder to another folder. it only exists in the image, the container just utilizes the code in the image.** whenever you make a change it is not copied over and over. this makes it very efficient. your code, environment and dependencies are existing inside an isolated container. The concept of containers and images allows us to have multiple containers based on the same image but isolated from each other. By default containers based on same image does not share data or state.

`**docker <command> --help**` **will show the documentation of the command.**

If you don't have any changes in the files or dependencies the docker run command is not necessary. you can simply restart the container using `docker start <imageid>` 

after running the docker start command it will keep running the container but you can run other commands because, it will not interrupt the shell. 

**for docker run attach mode is the default**(we cannot enter other commands in the terminal), **for docker start** detach mode is the default(we can enter other commands to the same terminal). **Attached mode means that we are listening to the output from the terminal. So the output from the container (application) will be seen in the console.** 

you can run the image with docker run in detach mode by passing the -d flag before the image id

i.e, `docker run -p 8000:80 -d 2ddfgjnvsaa` 

you can reattach to the docker container by 

`docker container attach <container name/id>` 

to see the logs of a container we can use `docker logs <container name/id>` this will show the past logs

if you want to keep seeing the logs of a container we have to pass the follow flag to the docker logs command. this will attach ourself to the container's log output.

`docker log -f <containerid/name>`

if you want to restart a container with attach mode we can use 

`docker start -a <containerid/name>` 

Even though we are in attached mode doesn't mean that we can interact with the container application. For this we need to use 

`docker run -it <containerid>` this will activate an iteractive pseudo terminal. after the process is completed it will stop the container automatically(in case of the python application).

when restarting the container in attached mode we can only enter the input once, after this it is exited. to overcome this we need to make the container interactive in attached mode.

`docker start -a -i <containerid>` 

**you can remove a container by using the** `**docker rm <container name/id>** `command. make sure that the container is stopped, otherwise it will cause an error. **we can delete multiple containers at once by simply passing the container names seperated by white spaces.**

`**docker rm <container1> <container2> <container3>**`

  
`**docker container prune**` **will remove all the stopped containers.**

`**docker images** ` **list all the images you have.** you can remove images by using rmi command.

`**docker rmi <imageid>**` . **you can only remove images once they are not being used by any containers, that includes stopped containers also.** 

**to remove all the unused images we can use** `**docker image prune**` **command.** tagged images cannot be removed like this.

 to remove tagged images `docker image prune -a` 

**To automatically remove a container once it is exited we use the --rm** flag with the docker run command. eg: `docker run -p 3000:80 -d --rm <containerId>`. this is useful when you need to rebuild the image once the container is stopped(often used for containers which don't need restart). 

The container is build on top of the image. The contents of the container are not copied again. The container is a wrapper around the image. Containers cannot change the code. But it can create additional files inside the container. `docker image inspect <imageId> ` used to inspect the structure of the image and the details about the image. 

**docker cp command lets you copy files into a running container or out of a running container.**

`**docker cp source destination**`

if you want to copy all files inside a folder specify foldername/.

**if either the source or destination is a container specify container\_name:/folder**

eg: `docker cp dummy/. boring_vaughan:/test` will copy all the contents of your dummy folder into the container.

This helps you to add files without restarting the container or rebuilding the image. (this can cause errors). 

The best way is to copy files out of a container(log files etc) this is not error prone.

you can give your own names and tags to easily identify the containers. t**o give your own name to the container you can pass** `**--name name_of_container**` when running the container.

eg: 

```javaScript
docker run -p 3000:80 -d --rm --name goalsapp 2ddf2ede7d6c
```

we can use the custom name to access and modify the container. eg: docker stop goalsapp

We can also give custom names and tags to images. **in case of images we have name which is the repository(main group) and tag(specific version) in the format of name:tag.** the name specifies a group for example node. the tag specifies a particular version for example 14\. 

**The name and tag can also be used for dockerhub to get a particular version or configuration of an image eg: node:14 in the docker file to pull node version 14.** The list of possible tags will be available in dockerhub for that particular image. 

This can be done to our own images. we can do this when building the image. syntax:` docker build -t name:tag`

tag can be a word, number or a combination of both

  
you can run a container based on name:tag combination of the image. 

eg: `docker run -p 3000:80 -d --rm --name goalsapp goals:latest` . 

We can share our images by:

1. Sharing the docker file with the source code. build the docker file locally with the docker build command.
2. Share a built image: the other user can simply download the image and run a container based on it. we don't need to build the image. we use this for sharing to deplyoment environments.

We can share the images with dockerhub or any third party private registry. Docker hub also have a lot of official images we can use for free.

To get started create a free docker account. click on the repository tab on the navbar. inside this click on create repository. give a name and an optional description to the repository. choose the type of repository. There is no limit for public repository in free account. The public images will be visible to everyone. Only 1 private repository is available for free account. click the create button and the repository is created.

if you want to push images to the dockerhub we need to use `docker push username/repository_name` command. but the local image you created maynot have this name. so when you try to push your image into the repository with this command, it will not work. for this you need to rename the image or you can rebuild the image with the `-t username/repository_name` . or `**use docker tag oldrepo:oldtag username/repository:[optinal tag]**`to retag the image. this will create a clone of the old image. 

Before pushing image into docker hub we need to login to docker account with docker login command.

`**docker login** `will prompt you to enter the username and password. there is also a `docker logout` command. 

after successful login push local image to dockerhub.

eg: `docker push sangeethkumarpg/node-hello:hello-app`

this will not completely push the images but pushes the necessary files in a smart way without wasting much memory.

To pull an image from docker hub we need to use` **docker pull username/respository_name:[tag if any].**`

eg: 

```javaScript
docker pull sangeethkumarpg/node-hello:hello
-app
```

docker pull will always fetch the latest image from the container registry. note that docker run will check for the images that are present locally. but it will not check for updates if you have it locally. if you need the latest image you need to use docker pull first.

Till now we have worked with read only data i.e, the code and files of the image. This is application data.

Then we have temporary data which is created by the application/running containers. such as user inputs, log files etc. These are stored in temporary memory. this type of data is dynamic, but cleared regularly. This is Read+Write. This type of layer is present in the container which wraps the image. 

Then we have permanent data such as user credentials. we are fetching and producing the data is in the container. The data must not be lost even if the container is deleted. This is read+write and must be stored permanently. this is done through volumes.

  
**Volumes are folders in your host machine that are mapped to your containers.** these folders are mapped to folders inside of the containers. **there is no relation between the Volume and COPY command**. With volume you can connect the folder inside a container to a folder outside of the container. **The changes in either folder will be reflected in the other one**. eg:- if there is a file in the host machine, the file is also accessible by the container. if there is some files in a specified path in the container, they are also accessible by host machine. **The data in the volume will not be removed even when a container is removed. containers can read and write data from and to a volume.** 

We create a volume by using `**VOLUME ["path"]**` in our docker file. eg: `VOLUME ["/app/feedback"]` this is a folder inside the container that should be mapped to some other folder outside of the container. The folder in the host machine is not specified here. here it is controlled by docker. 

`docker logs container-name` will show the log of the container. These volumes cannot be shared with other containers. They cannot be shared across containers of the same image also. 

There are two types of external data storages in docker. Volumes and Bind mounts.

Currently we used anonymous volumes. we can also names to the volumes. In both cases we don't readily know where the data is getting stored in the host machine. We can use the` docker volume ls ` to get the name of the anonymous volume. for anonymous volume docker assigns a name automatically. even when we stop the container or remove it even, the volume still remains(unless we use --rm flag when running the container). A defined path in the container is mapped to the created volume/mount. This path is not accessible by the user and we should not try to access it also. Data stored in named volumes will still be available even when we stop the container. This data can be accessible by new containers that you create. **Named volume is a good place to store data that you want to persist but don't need to edit.** 

To create a named volume we build the image as usual but when running the container we use -v

along with -v we need to pass a name and the path of the folder inside of the container.

i.e, `**-v folder_name_for_host_machine:path/inside/container**` **.**

eg: `docker run -d -p 3000:80 --name feedback-app -v feedback:/app/feedback feedback-app:volume` NOTE that the name provided should be same inside the docker file.

Named volumes are not attached to a container. 

`docker volume prune` will remove any unlinked anonymous volumes, 

```javaScript
docker volume rm volume_name
```

will remove the specified named volume. 

Even though the anonymous volumes will persist even after deleting the containers, they are unusable since a new volume will be created when you create a new image.

We only copy the files of the project to the docker container. Subsequent changes we make to the project folder will not be reflected to the container. During development this can cause problem, because everytime we will have to rebuild the image and restart the container for the changes to reflect. This is where bind mounts can help us. Volumes are managed by docker so we don't know where the volume will be placed. **But for bind mounts we set the path to which the data is stored.** We define our own path in the host machine for the bind mounts. **We can put our source code into bind mounts so that the code need not be copied everytime.** The container will have always access to the latest code. **Bind mounts are great for persistent and editable data.** We need to setup the bindmount before we run a container. 

to define a bind mount we specify the -v flag when we run the container. we need to place two -v flags, the first one is similar to that of a named volume. for the second one we need to provide the absolute path to the folder.

eg: `docker run -d -p 3000:80 --rm --name feedback-app -v feedback:/app/feedback -v /Users/Desktop/Development/docker:/app feedback-node:volumes` 

**NOTE : You should wrap your absolute path in double quotes if your path has white spaces or special characters.**

When setting up bind mounts you should make sure that docker has access to the folder.

**after running the above command the app will immediately crash**. This is something that we need to do with bind mounts. Here we are binding everything in our local folder with the app folder. i.e, we are overwriting the folders inside of the container with our local folder. **Our local folder doesn't have node\_modules folder which has all the dependencies that our app needs**. To deeply understand the issue we need to know how the volumes and containers interact with each other. as we have seen that a volume and bind mounts can be connected together. This means that some folders in the container are connected to some folders in the host machine. **If we have some files that are already inside of the container they will also exist in the volume which is outside of the container. If the program in the container create a folder it is replicated in the volume of the host machine. When the container starts up if does not have any files inside it, it will then load the files from the volume.**

That is actually what we utilize with the bind mount. **Here we have files inside of the container(created by instructions in docker file such as npm install) and outside of the container. Docker will not overwrite files in the local machine. Instead the local folder overwrites what is inside of the container, this removes the node\_modules.** This is what is happening here. **_To overcome this we tell docker that there are certain parts of the container which should not be overwritten from the host machine(or outside of the container)._**   **This can be acheived with another anonymous docker volume(volume without name). for this we add a third -v flag with the path of the node modules inside of the container. we can add this inside the docker file also by specifying the VOLUME command. so the command is** 

`**docker run -d -p 3000:80 --name feedback-app -v feedback:/app/feedback -v "/Users/sangeethkumarpg/Desktop/Development/docker/data-volumes-01:/app" -v /app/node_modules feedback-node:volume**`

**This works because docker always evaluates all the volumes you are setting on a container, if there are clashes, the longer internal path wins.** Here we have a volume (bind mount) that is mapped to the /app and another one (anonymous volume) that is mapped to /app/node\_modules. **So docker will choose the more specific path.** Thus the node\_modules folder which is created at the time of image creation will co-exist with the bind-mount in the container. 

**NOTE: the / before the app. it denotes that it is the absolute path. If you don't provide / before the app it will throw an error saying that mount path should be absolute. also note that there is no line breaks between path names.**

In macos when creating bind mounts we need to allow docker to access the file system. for this go to docker settings under resources>file sharing add the specific folder or it's parent folder to the path and save changes.

By adding the bind mount any change we make to the html files inside the node app is reflected immediately. but the changes in the server.js file it will not be reflected. For this we need to restart the container(by stopping and starting again). To fix this we use nodemon npm module. This will automatically restart the server.js whenever there is a change. add this as devDependency to package.json, add script tag and specify start script as nodemon server.js. rebuild the docker image. **To delete a bind mount you will need to delete the folder in the host machine.**

By default bind-mounts are read write. The docker can write to the bind mount. To make sure that only we(the hosting machine) can write into a bind mount we can provide a ":ro" after the container folder name.

eg: `docker run -d --rm -p 3000:80 --name feedback-app -v feedback:/app/feedback -v "/Users/sangeethkumarpg/Desktop/Development/docker/data-volumes-1:/app:ro" -v /app/node_modules feedback-node:volumes ` 

but this might not be something you want such as files that are being written into this folder by the program. for those files we must add additional volumes (anonymous or named volume) ro ensure that those files will be able to write from inside of the container.

i.e, `docker run -d --rm -p 3000:80 --name feedback-app -v feedback:/app/feedback -v "/Users/sangeethkumarpg/Desktop/Development/docker/data-volumes-1:/app:ro" -v /app/node_modules -v /app/temp feedback-node:volumes  
`

  
Since this path is more specific it will override the bind mount. **To make sure that the behaviour of bind mount is overwritten we must specify it when running the container and not inside of the docker file.**

`docker volume create volume-name` will create a volume. when running the docker with the -v flag docker will automatically create the volume, so you don't need to manually create the volume with the above command. The `docker volume ls` command will list all the volumes that is managed by docker (named and anonymous volumes). you can remove volumes with `docker volume rm volume-name` command. or `docker volume prune` command. 

You can inspect a volume by using `docker volume inspect volume-name`. when inspecting the volume we can see when the volume was created, the mount point which is the actual path where the volume is created. This is inside the virtual machine which is used by docker so we cannot find this path in our host machine. if it is a readonly volume you will see that under the options key when inspecting the volume. The volumes which have active containers mapped to it cannot be moved unless we stop the running container. When you remove a volume all the data inside it are lost.

Creating the volume with the same name would not bring back the data inside the volume. 

**When we use bind mount we don't need to use copy command inside the docker file to copy data into the container. Bind mounts are used in development environments.** In production the snapshot of our code is exposed as a container, where we don't need the ability to directly edit the source code. 

**we use .dockerignore file to ignore files that need not be copied to the image.** This makes sure that these files are not copied by the copy command in the dockerfile. it is similar to gitignore. you can add any number of files and folders which are not required by the application for the execution.

Docker support built time arguments and runtime environment variables. 

ARG : Allows us to have flexible arguments from the command line. These variables are declared in the docker file. we pass the arguments using --build-arg flag when you run docker build command. 

ENV : Available inside of docker file in application code. You can set them using ENV command in the docker file or --env flag with docker run. 

This helps you to create more flexible containers.

eg: `ENV PORT 80` will set an environment variable with port as 80\. where PORT is the environment variable name. If we want to use an environment variable inside the same docker file we need to add a $ before the variable name. eg: `EXPOSE $PORT` . Inside your application you still need to use the language specific libraries to access the environment variables. This approach does not lock you into using this particular value. in runtime you can update the value of environment variables defined inside of the docker file.

you need to pass `--env variable=value` when running the container will modify the default value of the environment variable. You can add multiple environment variables like this.(But you need to provide multiple --env flags with docker run command). another shortcut is to use --e. 

Another option is to define a .env variable and pass this file name to docker run command using `--env-file filename` 

eg: `docker run --env-file ./.env sample-app` we need to add a ./ before the file name if it is in the same folder as the docker file. The approach of using environment variables as file is the safer approach because once you put your environment variables inside the docker file, if anybody uses `docker history <image>` command on your image they can see the values of the environment variable. So for security purposes give environment variable values inside a seperate .env file and pass it during the runtime. also make sure that you are not sharing the .env file.

Build time arguments lets us plugin values into our docker file or our image at the time of building an image. For example we can use this for setting up the port number. To set up an argument inside the docker file we use the `ARG arg_name [=optional_default_value]` syntax.

eg: `ARG DEFAULT_PORT = 80`

 These variables are not available in your code, They are only available to use inside the docker file. There are also limitation on where you can use it. You cannot use it on commands (CMD) because it is a runtime command which gets executed when the container starts. We can use them on instructions like ENV. eg:

`ENV PORT $DEFAULT_PORT`   
We don't need to specify the ports when building the docker image because the default is set inside the docker file. But if you need to override the default port you can use them like:

  
`docker build -t feedback-node:dev --build-arg DEFAULT_PORT=8000 .` 

We specify the arguments using `--build-arg arg_name=value` syntax.

You should note the placement of the arguments in the docker file. Ideally it should be placed after after copying of the code files because whenever a change in the port number occurs docker only need to rebuild the layers after this command. So if it is placed first the subsequent layers such as npm install, copy etc will have to run again and again which is unnecessary.

We may need to communicate with the www to get some data which is obviously outside of the container. Also you might need to communicate with services or databases in the host machine which is also outside of the container. Another possibility is to communicate with another container which runs a service in your machine. Building such application is very common. 

**NOTE: Sending requests to the world wide web works out of the box without any extra configuration.**

If we have a service that is running on the local machine which you want to access from the container. For this type of communication you only need to change the url of the service. Instead of **localhost** we can use **host.docker.internal** . This automatically translates to the ip address of the host machine as seen from inside of the docker container. You can use this anywhere you need a url. 

if you run `docker run mongodb` which is the official name of the docker image in docker hub. It will try to check if the image is found locally. If it not found locally, it will pull the image automatically from docker hub. 

To get the ip address of a container we can inspect the docker container using the  
` docker container inspect container_id/container_name`   
When you run this command under the `NetworkSettings` section you can see the `IPAddress` key which is the ip address of the container. You can use this ip address in your code to connect to the container. 

The disadvantage of the above approach is that everytime you restart the container of the service the ip address may change. So everytime you need to manually modify the ip address. 

We can create a network with containers through which containers can talk to each other. Docker will manage the ip addresses of the containers automatically handles the ip lookup. To run a container in network we can use the following command syntax when running the container:

`docker run --name container_name --network network-name image_name`   
But this command will not work by default as the network will not be automatically created by the docker. for this we need need to create a create a network using `docker network` command.

```javaScript
connect     Connect a container to a network
create      Create a network
disconnect  Disconnect a container from a network
inspect     Display detailed information on one or more networks
ls          List networks
prune       Remove all unused networks
rm          Remove one or more networks
```

The above shown as the options for the docker network command.

To create a network we use `docker network create network-name ` syntax. eg:   
`docker network create favorites-net`   
To list all the networks we use:  
`docker network ls`   
After this we can run the container in this network. For example :  
` docker run -d --name favorites-db --network favorites-net mongo:latest`   
**NOTE: Here we are not using the -p tag when running the container because we don't need to access the db from our localhost. The only communication is through container network which is managed by docker without any user configuration.** 

If two containers are in the same network we can use the container names in the url to talk to each other. When using the url we can use :  
`mongodb://favorites-db:27017/swfavorites` the `favorites-db` is the name of the container which has the mongodb.

To run the app in the same network we can use the same network which has the mongodb. so the command will be like:  
`docker run -d --name favorites-app --network favorites-net --rm -p 3000:3000 favorites-node`   
To check the logs of the container we can use:  
`docker logs favorties-app`   
We can check if the container is successfully started or not using this.

**NOTE: 2 Containers are not able to talk to each other unless they are in the same network or you manually use the ip address of each container to connect them.**

In container to container communication we don't need to publish the port unless we want it to expose it outside of the container. There are different types drivers in docker. By default when you create a network it uses **bridge** **driver**. Using bridge driver we can communicate with containers in the same network using the container names.   
**host** : This type of driver is used for standalone containers where the isolation between the host system and the container is removed.   
**macvlan :** You can set a custom MAC address to a container - this address can then be used for communication with that container  
**none :** All networking is disabled.  
To manually specify the driver when creating a network we can use:  
`docker network create --driver driver_name network_name`  
**NOTE : In most scenarios bridge driver is suitable.** 

Docker doesn't change the source code to resolve ip addresses. Instead it has access to the environment which the code is placed in. When your code sends an http request, docker resolves the IP address corresponding to the resource in the docker environment.

For this first we need to pull the docker image of mongodb using :  
`docker run -d --name mongodb --rm mongo:latest`   
Then create separate docker files for frontend and backend. The backend docker file looks like:

```javaScript
FROM node
 
WORKDIR /app
 
COPY package.json .
 
RUN npm install
 
COPY . .
 
EXPOSE 80
 
CMD ["node","app.js"]
```

And the backend file looks like:

```javaScript
FROM node 
 
WORKDIR /app
 
COPY package.json .
 
RUN npm install 
 
COPY . .
 
EXPOSE 3000
 
CMD ["npm","start"]
```

After this build images for both the files.

We then need to create a network using the docker network create command like :

`docker network create goals-net`   
Then first run mongodb container with this network  
`docker run --name mongodb --rm -d --network goals-net mongo ` 

Then we need to run the backend with the network. But before that we need to update the url in the app.js. We need to replace the host in the url of mongodb connection with the name of the container which is mongodb. After this we need to rebuild the image using:

```javaScript
docker build -t goals-node .
```

We need to use this now because we haven't created a bind mount. After building the image run the container with the network.

`docker run --name goals-backend --rm -d --network goals-net goals-node`   
Similarly for the frontend replace the host with the backend container name and rebuild the image. After this if we run :  
`docker run --name goals-frontend --rm -d -p 3000:3000 --network goals-net goals-react`   
This will not work because we will be unable to connect the frontend with backend.

This is because for our node app it is running inside of the container but our react app is running inside of the user's browser. This means that the browser will not be able to translate the hostname of the backend container service. So this means that we need to change the url of our backend service back to localhost. Then we need to publish the port 80 of the backend service. If the port is already used by the system you an change the port like:  
`docker run --name goals-backend --rm -d -p 90:80 --network goals-net goals-node` 

then build the image and run the frontend container again by publishing the port. the command will be like:  
`docker run --name goals-frontend --rm -d -p 3000:3000 goals-react `   
This will publish the react container on port 3000 of localhost, and it will work as expected. This is not an ideal solution because we haven't implemented data persistence, access limiting and live code updates.

To make the data persistent we need to create a volume. Internally the mongodb container stores the data in `/data/db` folder. We need to bind this folder with the local folder of our host machine. If we need to create a bindmount we need to specify   
`**docker run -v absolute_path_to_host_folder:path_in_container** `   
**Example:** 
`docker run --name mongodb --rm -d --network goals-net -v data:/data/db mongo:latest`   
By doing this our data persists even after the container is restarted because the data will loaded from the data volume if already exists, if not it will create a new volume.

To setup authentication for mongodb we can set environment variables for username and password using the -e flag when running the container. We need to specify `MONGO_INITDB_ROOT_USERNAME=username  
and  
MONGO_INITDB_ROOT_PASSWORD=password`   
example: `docker run --name mongodb --rm -d --network goals-net -v data:/data/db -e MONGO_INITDB_ROOT_USERNAME=sangeeth -e MONGO_INITDB_ROOT_PASSWORD=password mongo:latest`   
After adding this we need to pass the username and password with the connection string. It should be in a specific format i.e `mongodb://username:password@hostname:27017` .  
eg: `'mongodb://sangeeth:password@mongodb:27017/course-goals?authSource=admin'`   
Also note that we need to pass the authSource=admin query param. I**f you created a mongodb container with an image to store data if we add the environment variables we may not be able to connect to mongodb. For that we first need to remove the volume of mongodb and create it again before setting up the environment variables.**

To add live source code updates and persistence for the node application we need to create 2 volumes. 1 for saving the log files, which can be either a bind mount or a named volume. If you want access to log files you can choose bindmounts. For creating a named volume we can use: -v name\_of\_volume:/app/folder\_name.   
To create bind mounts we need to specify the full path of the folder in the host machine so that it can be binded to the container folder. In our case we want to bind the entire folder of the node app with the container so that any change we make in the files are reflected immediately.   
We actually need one more volume for the node\_modules because we should tell the container that the existing node\_modules inside of the container should stay there instead of looking for the node\_modules in the local folder. This can be an anonymous volume. 

Before we run the container we need to make sure that the node server is restarted automatically for code updates so for this we use `nodemon` as a `devDependency` in package.json of our backend application. 

```javaScript
"devDependencies": {
    "nodemon": "3.1.10"
  }
```

To make sure that the nodemon is getting correctly utilized, we can use a start script in the package.json. like:

```javaScript
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start":"nodemon app.js"
  },:
```

make sure to update the start script to npm start in the docker file like:  
`CMD ["npm","start"]`   
One final improvement on this setup is to avoid the hardcoding of username and password in the js code. To avoid this we can use the ENV command in the docker file to set a default username and password for mongodb. `` `mongodb://${process.env.MONGODB_USERNAME}:${process.env.MONGODB_PASSWORD}@mongodb:27017/course-goals?authSource=admin`  
 ``in the js file and 

```javaScript
ENV MONGODB_USERNAME=root
ENV MONGODB_PASSWORD=secret
```

The default value for the environment variable is specified using = in the docker file  
The final command will be :  
`docker run --name goals-backend --rm -d -p 90:80 --network goals-net -v /Users/sangeethkumarpg/Desktop/Development/docker/multi-01-starting-setup/backend:/app -v logs:/app/logs -v /app/node_modules -e MONGODB_USERNAME=sangeeth -e MONGODB_PASSWORD=password goals-node`   
  
The final step is to add a docker ignore file so that unnecessary files are not copied over to the container. we create a docker ignore file by creating .dockerignore at the root of the project where docker file is also present. once you make changes in the docker ignore you need to rebuild the image.

For the front-end service we just need to create a bind mount for the live code changes. The src folder is only required for the bind mount because most of the changes we do will be inside the src folder where we place our components. So for this when we run the container we put the absolute path of the src folder and bind it to a volume.  
The command is:  
`docker run -v /Users/sangeethkumarpg/Desktop/Development/docker/multi-01-starting-setup/frontend/src:/app/src --name goals-frontend --rm -d -p 3000:3000 goals-react`   
As a final step create a docker ignore file to avoid the copying of node\_modules, .git and dockerfile to the container so that running the container becomes faster.

**NOTE** : The setup till we did now is only for development. this is not suitable for production environments. 

Till now we created and managed containers with long commands. In that setup we need to manually remove named volumes and networks. **Docker compose is built-in tool in the docker which helps in managing the multi container setup easier.** With just one command we can setup a multi container environment and with just one command we can tear down all the setup.

docker compose let's you replace multiple docker build and docker run commands with just one configuration file and set of orchestration commands to start, stop all the containers at once. Even though docker compose can be used in a single container setup it is more powerful and convenient in multi container setups. NOTE: Docker compose doesn't replace the dockerfiles, instead they work together with the dockerfiles. I also doesn't replace images and containers. It makes working with them easier.  
Docker compose is not suitable for managing multiple containers in multiple hosts(different machines). Docker compose file consists of services(containers) their configuration such as ports, environment variables, volumes, networks. We can do almost anything we usually do with docker commands in the docker compose file.

The first step is to create a **docker-compose.yaml** file. The first line of the docker compose file is version key where we specify the docker version. **This key is not required in newer versions of docker compose.** After this we specify the services. For services we define children with 2 space indentation. With further indentation we define the configuration of each of the container. For each service again with 2 space indentation we specify the image with a string value. This value can be an image name or a dockerhub url. We don't need to specify the remove flag because docker compose will automatically remove the containers once the services are stopped by docker compose command. To create a volume we specify the volumes we specify volumes as a child to the container. under this we specify each volume with a -.

To specify environment variables there are 2 syntaxes:  
under the environment key we can specify like:  
`variable_name: value`

or like:  
` -variable_name=value`   
eg:

```javaScript
  mongodb:
    image: 'mongo'
    volumes:
      - data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: sangeeth
      MONGO_INITDB_ROOT_PASSWORD: password
```

If you want to place the sensitive information inside a .env file we need to create a env folder in the same level as the docker compose file. then we use 

```javaScript
container_name:
  env_file: 
    - relative_path_to_the_env_file
```

**NOTE: The .env file should not contain white spaces except new lines.**  
example:

```javaScript
  mongodb:
    image: 'mongo'
    volumes:
      - data:/data/db
    env_file:
      - ./env/mongo.env
```

**NOTE: We use - to specify list of items if we have only single values. If we have key value pair values we don't use -.**

We don't need to create a network when using docker compose because it will automatically create an environment in which all of the containers will be placed. It will by default create a network for us. But if we want we can specify additional networks using the networks key under the service.

```javaScript
networks:
  - network_name
```

example:

```javaScript
mongodb:
  networks:
    - goals-net
```

If you are using a named volume we must specify them again as in the same level of the services. like:

```javaScript
volumes:
  volume_name:
```

we don't need to specify a value after specifying the volume name.   
eg:

```javaScript
volumes:
  data:
```

Here data is the name of our volume. By doing this these volumes can be shared by multiple containers. NOTE : Anonymous volumes and bind mounts need not to be specified here. The docker compose file will look like:

```javaScript
# version is deprecated
#version: '3.8'
services:
  mongodb:
    image: 'mongo'
    volumes:
      - data:/data/db
    env_file:
      - ./env/mongo.env
  #backend:
  #frontend:
volumes:
  data:
```

The older versions use `docker-compose up` command to start the services. But in newer versions we use `**docker compose up**` without the -. The docker compose up will also pull images from docker hub if the image is not available locally. The docker compose up starts the services in attached mode. If we want we can specify the -d flag to start the services in detached mode like:  
`docker compose up -d`   

The docker compose down command stops all the containers and remove them.   
`docker compose down`   
If you also want to remove the volumes you must specify the -v flag with docker compose down command.  
`docker compose down -v` 

You can either choose the image which you already built or create a new image from the start. We can do that by using the build argument under the service. We can specify the relative path of the docker file to build the image. The syntax is:

```javaScript
service:
  build: relative_path_to_dockerfile
```

There also another longer form to this:  
service:

```javaScript
  build:
    context: folder_in_which_docker_file_is_present
    dockerfile: name_of_the_docker_file
    args:
      argument_name: value
```

If you have the dockerfile named as dockerfile itself you don't need to specify the docker file name.   
To specify ports which you want to expose we use the port key under the service. Then we specify the ports as children of this using single or double quotes. The syntax is like:

```javaScript
service:
  port: 'host_port:container_port'
```

example:

```javaScript
backend:
    build: ./backend
    ports:
      - '90:80'
```

When we are setting up bind mounts using the docker run command we needed to specify the absolute path, but when using docker compose we only need to specify the relative path from the docker-compose file. For example:

```javaScript
    volumes:
      - logs:/app/logs
      - ./backend:/app
```

we want all the files in the backend folder to be a bind mount like this.   
If we have multiple containers in the docker compose, there might be some containers that depend upon other containers. For this we can specify the depends\_on key. Under this we can specify the list of containers/services. The service will not start unless all the dependent services are up and running. The syntax is:

```javaScript
  depends_on:
    - service_name
```

example:

```javaScript
    depends_on:
      - mongodb
```

So the current dockercompose file looks like:

```javaScript
# version is deprecated
#version: '3.8'
services:
  mongodb:
    image: 'mongo'
    volumes:
      - data:/data/db
    env_file:
      - ./env/mongo.env
  backend:
    build: ./backend
    ports:
      - '90:80'
    volumes:
      - logs:/app/logs
      - ./backend:/app
      - /app/node_modules
    env_file:
      - ./env/backend.env
    depends_on:
      - mongodb
  #frontend:
volumes:
  data:
  logs:
```

**NOTE: When check the services we can see that the name of the container/service is a different one. But when we use the container name in the code we can still access them. The service name we specified in the docker compose is designated as the name of the service.**

For the frontend react service most of the steps are essentially the same, we need to build an image from the frontend folder, publish the port in 3000, add bind mount for code changes. Additionally if you want interactive mode you have to add 2 options:

```javaScript
  stdin_open: true
  tty: true
```

These 2 are entirely optional as we may not always need to have an interactive terminal for our container.  
The frontend depends on backend service, so we need to add depends\_on to this service.

`docker compose down --volumes --remove-orphans  
`Removes the volumes and their data along with removing the containers. The entire setup of the docker compose file will look like:

```javaScript
# version is deprecated
#version: '3.8'
services:
  mongodb:
    image: 'mongo'
    volumes:
      - data:/data/db
    env_file:
      - ./env/mongo.env
  backend:
    build: ./backend
    ports:
      - '90:80'
    volumes:
      - logs:/app/logs
      - ./backend:/app
      - /app/node_modules
    env_file:
      - ./env/backend.env
    depends_on:
      - mongodb
  frontend:
    build: ./frontend
    ports:
      - '3000:3000'
    volumes:
      - ./frontend/src:/app/src
    stdin_open: true
    tty: true
    depends_on:
      - backend
volumes:
  data:
  logs:
```

You can find the information about a particular docker compose command using --help flag. If we use `docker compose up --help`  
We can see the optional flags that can be used along with the command. One important command is:  
`docker compose up --build `  
This command rebuilds the images of the containers. NOTE: This will only rebuild the images we define using the build key of the containers and not the images that we are directly pulling from docker hub(Specified using the image key).  
If you just want to build the images we can use:  
`docker compose build `   
This will only build the images of the services.

The name of the container is taken from the folder name followed by the name you defined in the docker compose file and finally an incremental number starting from 1\. If you want a specific name for your container we can define container\_name key inside the service.

The syntax is :

```javaScript
  service:
    container_name: name_you_choose
```

example:

```javaScript
mongodb:
  image: mongo
  container_name: mongodb
```

Till now we have seen containers used to expose the functionality of a service. These types of containers had the environment as well as the code bundled as a single unit. **Utility containers** is not an official term, it basically means that we are storing the container in the environment and when we run the container we append certain commands to utilize some features of the environment.

For example if we need to create a node project we can either create a folder and create a package.json file by hand. But this is cumbersome. So we use the npm init command to create a starting project to create a node application. The problem is that we need to have the node.js installed in the system, but this is the problem that docker tries to resolve. We need to have an environment to create projects, that is where the utility containers comes in.

We can run a container in different ways, for example if you run docker run node, It will immediately start and stop the container. If we need to interact with the node container we can use the -it flag to run the node in interactive mode. By this way you can utilize the node runtime to execute javascript code in the console. Suppose we run `docker run -it -d node` It will keep running the container but you won't be able to interact with the container. If you need to attach yourself to a container you can use `docker container attach container_name`   
We use the `docker exec` command to run commands inside of a container beside the default command(commands in the dockerfile) the container executes.   
For example if we have a node container named my\_node\_container, we can create a node project using  
`docker exec -it my_node_container npm init`   
We are running the exec in interactive mode because we need to provide input for configuring a new project when running npm init.  

There is also another way. By default when you run the node container it opens REPL(Read, execute, print, loop). We can override this behavior if we specify additional commands after the name of the image. For example if we want to initialize an node project when the container is started we can use:  
`docker run -it node npm init`   
Here also we need to use interactive mode because we need to provide inputs when creating a node project. When you run the above command the container will run the npm init command and after we provide the inputs, it will create a package.json file and stops the container.

**NOTE: docker exec command don't disturb the main process of the container, so it is useful for things like reading the log file in the running container without stopping or interrupting the container.**

To utilize the utility container we first need create a docker file in which we need to use the image of our environment for example node.js. Then we need to create a working directory. Then build the image. When running the container we need to use the interactive mode and we need to create a bind mount so that the files generated by the environment are available in the host machine folder. At the end of the docker run command we need to specify the command to be executed in the environment. for example:  
`docker run -it -v C:\Users\pgsan\OneDrive\Documents\Docker\DockerPractice-main\DockerPractice-main\utility-container\node-project:/app node-utility npm init`   
This runs the utility container, after entering the necessary information the package.json file is created inside the node-project folder of the host machine.

It is a good idea to restrict the commands which can be run inside the utility container. In the current setup we can run any command. The `ENTRYPOINT` command is used for this. It is similar to the `CMD` instruction we used in the docker file, the difference is that if you use CMD the command you pass as argument in the docker run will overwrite the command specified in CMD. But in case of ENTRYPOINT command the command you passed as argument will be appended to the entrypoint command. So if we specify npm in the entrypoint we can run any npm command. So the docker file will look like:

```javaScript
FROM node:18-alpine
 
WORKDIR /app
 
ENTRYPOINT [ "npm" ]
```

And the command to run the container will be:  
`docker run -it -v C:\Users\pgsan\OneDrive\Documents\Docker\DockerPractice-main\DockerPractice-main\utility-container\node-project:/app node-utility init` 

We can use any npm commands using the above command. Once the command is executed the container automatically shuts down.

The problem of the above approach is that we need to manually run the above commands every time. We can simply that by creating a docker compose file.

For this we create a docker-compose.yaml file. Specify the service which we need to be containerized. specify the docker file for the image to build, set the stdin\_open and tty flags to true and finally add the bind mount with the relative path to the docker compose yaml file. So the file will look like:

```javaScript
services:
  npm:
    build: ./
    stdin_open: true
    tty: true
    volumes:
      - ./node-project:/app
```

But the problem is we cannot run the commands with docker compose like we used to do in docker run. There are two ways you can run commands with docker compose, they are exec and run.

* exec : is used to run commands on the running container.  
syntax : `docker compose exec service command`
* run: used to run a single service by using the service name. The syntax is:  
`docker compose run service command`

So the command to run the container will be:  
`docker compose run npm init`   
Where npm is the service name and init is the command. This will use the entrypoint specified in the docker file and append the init command with it.

Note that for every time we run the utility container using docker compose run command the container is not automatically removed like in docker compose up and down. We can use the --rm flag with the docker compose run command so that the container is automatically removed once the task of the container is completed.  
The syntax is:  
`docker compose run --rm service command`   
example:  
`docker compose run --rm npm init` 