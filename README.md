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

Laravel is the most popular php framework. It is great framework but setting it up for the first time is quite complex. It is not a Laravel problem but a php problem. There a quite a lot of dependencies for Laravel. Unlike node.js Laravel does not have a webserver. To get started on node.js we only needed to download node.js which already have the webserver. For the laravel container we will have the following components.   
1\. Folder in which our application code resides.

2\. A container with php interpreter to execute our code. 

3\. Nginx webserver container which accepts the requests from clients, pass it to the php interpreter for processing, and return the result to the client based on the result from the interpreter. 

4\. MySQL database container which communicates with the php interpreter. 

The 3 containers are application containers, because they will be up and running as long as the application needs to be up and running. Apart from these we also need utility containers. 

Because for our Laravel application we require some additional utilities. We need:

1\. Composer: It is like a package manager for Laravel. It is similar to npm in node. We use composer to create applications. Laravel uses composer to install dependency. 

2\. Laravel artisan: Laravel ships with its own Laravel artisan tool. This is a command which we use to create migrations to our database as well create starting data for our database.

3\. npm: Laravel uses npm for some of its frontend logic. 

For this the first step is to create a docker-compose.yaml file. It will hold all our application containers and utility containers. In the compose file add the server. The image we will use will be nginx:stable-alpine which is lightweight image. We commonly wrap this in quotes to avoid confusion. Then we specify the port. By default, nginx runs on port 80\. So, we need to expose this to our local machine. Also, we need to specify the configuration file for nginx so that it will work as expected. We add this as a bind mount. We bind the configuration file to `/etc/nginx/nginx.conf` folder. This is as per the official nginx image documentation. Since this is a configuration file we have to make it read-only.

```javaScript
- ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
```

Then in our local machine we create a nginx.conf file inside the nginx folder. The content of the configuration file looks something like:

```javaScript
server {
    listen 80;
    index index.php index.html;
    server_name localhost;
    root /var/www/html/public;
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php:3000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
```

The compose file will now look like:

```javaScript
services:
  server:
    image: 'nginx:stable-alpine'
    ports:
      - '8000:80'
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  # php:
  # mysql:
  # composer:
  # artisan:
  # npm:
```

php has an official docker image but we need to extend this image so that we can add some extra extensions for the Laravel to work. We can create a separate folder to store the docker files. The is restriction in adding a name before .dockerfile. We can create something like `php.dockerfile` which is valid. In the docker file we can use the `php:7.4-fpm-alpine` image which is a lightweight image for php 7.4\. We then we need to add 2 additional extension which are pdo and pdo\_mysql extensions. We can install them using `docker-php-ext-install` . The command will look like:

`RUN docker-php-ext-install pdo pdo_mysql` . We must ensure that the above command is executed in the correct directory. For this we need to set the working directory to `/var/www/html` .

If you don't specify an entry point (a default command which runs when the container starts) the entry point of the base image will be used. The docker file will look like:

```javaScript
FROM php:7.4-fpm-alpine
 
WORKDIR /var/www/html
 
RUN docker-php-ext-install pdo pdo_mysql
```

Since we have changed the name of the dockerfile we need to explicitly specify the folder and filename, using context and dockerfile commands. It will look like:

```javaScript
  php:
    build: 
      context: ./dockerfiles
      dockerfile: php.dockerfile
```

Then the next step is to make sure that the php interpreter has access to our application code. We can place the application code in the src folder of our local machine to /var/www/html folder of the container. We can create a bind mount for that. We can add a` :delegated` tag to the bind mount. This means that the operations that performed on the files will not be instantly reflected in the local machine, it will be done in batches. This is much more performant because there are hardly any changes from the container. The nginx server sends requests to port 3000 of the php container. We had set this in the nginx.conf file. But internally the php container listens to port 9000\. So we need to map port 3000 to port 9000\. 

We don't really need the above because we are not directly interacting with the php container. Since this is container to container communication, we can directly specify the container name with the required port number in the nginx.conf file which is much simpler. For this just change the file like:  
` fastcgi_pass php:9000;` 

We can pull the official MySQL image from docker hub. To configure the MySQL database, we need to set some environment variables we can either do that in the docker compose file or as a separate .env file. We can specify an environment file using `env_file` option. The file will now look like:

```javaScript
services:
  server:
    image: 'nginx:stable-alpine'
    ports:
      - '8000:80'
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  php:
    build: 
      context: ./dockerfiles
      dockerfile: php.dockerfile
    volumes:
      - ./src:/var/www/html:delegated
  mysql:
    image: mysql:5.7
    env_file:
      - ./env/mysql.env
  # composer:
  # artisan:
  # npm:
 
```

To set up a laravel project we need composer. For this we can use a custom docker file. Inside this we can use the composer image, specify the working directory as` /var/www/html `and specify the entry point. The `ENTRYPOINT `command should run the `composer `command with `--ignore-platform-reqs `flag to ignore any dependency issues. The docker file will look like:

```javaScript
FROM composer:latest
 
WORKDIR /var/www/html
 
ENTRYPOINT ["composer","--ignore-platform-reqs"]
```

After the above step specify the build for the composer in the docker compose file. Then we need to connect the source folder of the code so that composer can access this. We can create a bind mount for this.

The docker compose file will now look like:

```javaScript
services:
  server:
    image: 'nginx:stable-alpine'
    ports:
      - '8000:80'
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  php:
    build: 
      context: ./dockerfiles
      dockerfile: php.dockerfile
    volumes:
      - ./src:/var/www/html:delegated
  mysql:
    image: mysql:5.7
    env_file:
      - ./env/mysql.env
  composer:
    build: 
      context: ./dockerfiles
      dockerfile: composer.dockerfile
    volumes:
      - ./src:/var/www/html
  # artisan:
  # npm:
```

To create a laravel project we can find the command to create project in the laravel documentation. We can run only the composer container with this command to create the project. The command for this will look like:

`docker compose run --rm composer create-project --prefer-dist laravel/laravel .` 

Once the laravel project is created with the above command we need to tweak the values in the generated .env file so that we can connect to our MySQL database. like:

```javaScript
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=homestead
DB_USERNAME=homestead
DB_PASSWORD=secret
```

In our current setup we are not exposing the files to nginx server. So, for this we can add another volume to the nginx container and connect the `src` folder with the `/var/www/html` folder. After this if we just run `docker compose up` it will run all the services including the composer service which we do not want. Instead, we can target specific services which we can run by specifying the service name with the docker compose up command. Before we run we need to make one small adjustment to the the server container. We need to adjust the path of nginx configuration file like:

```javaScript
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

After this we can run `docker compose up -d server php mysql` 

If a service depends upon on 2 or more other services we can use the **depends\_on** tag with that service. By doing this when we start that service the dependent services are automatically started.

If we want docker to re-evaluate the docker files every time you run docker compose we can use` --build `flag with docker compose up. Example:

`docker compose up -d --build server` 

If there are no changes in the images and docker files it will not re-evaluate the images. It will use the cached images.

In case if you get an error like Base table or view not found: 1146 Table 'homestead.sessions' doesn't exist. You need to manually create a new migration by entering into the php container in interactive mode by using the docker exec -it command. Then inside the container run `php artisan make:migration create_sessions_table --table=sessions  
`Then open the migration file in database/migrations. Then insert the below code:

  
```javaScript
<?php
 
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
 
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('sessions', function (Blueprint $table) {
            $table->string('id')->primary();
            $table->foreignId('user_id')->nullable()->index();
            $table->string('ip_address', 45)->nullable();
            $table->text('user_agent')->nullable();
            $table->text('payload');
            $table->integer('last_activity')->index();
        });
    }
 
    public function down(): void
    {
        Schema::dropIfExists('sessions');
    }
};
```

Then run the migration using `php artisan migrate` . Then open the mysql container in interactive mode, login to the database and use the database you have specified in the env file. Check if session table already exists using:

`SHOW TABLES LIKE 'sessions';`

Then insert the migration manually using:

```javaScript
INSERT INTO migrations (migration, batch)
VALUES ('2025_11_20_115358_create_sessions_table', 1);
```

Replace the name of the migration with the name of the actual file.

When you stop the containers and run again it again you might need to open the php container in interactive mode using `docker exec -it container_id sh` . Then run `php artisan migrate`.

artisan is tool in laravel which helps with configuration. We can use the php docker file for artisan also. Because it needs php to execute. We also need a volume because the artisan tool runs on the code. We can override commands defined in the docker file with in docker compose file. For example we can add an **entrypoint** command for artisan. By doing this we can correctly configure artisan. We can do the same step for npm as well but we will use the node image, and map the working directory, add the bindmount and specify the entrypoint. After running the docker compose file we can use:

`docker compose run --rm artisan migrate` . To run the migrations. The complete docker file will look like:

```javaScript
services:
  server:
    image: 'nginx:stable-alpine'
    ports:
      - '8000:80'
    volumes:
      - ./src:/var/www/html
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - php
      - mysql
 
 
```

```javaScript
 php:
    build:
      context: .
      dockerfile: dockerfiles/php.dockerfile
    volumes:
      - ./src:/var/www/html:delegated
  mysql:
    image: mysql:5.7
    env_file:
      - ./env/mysql.env
  composer:
    build:
      context: .
      dockerfile: dockerfiles/composer.dockerfile
    volumes:
      - ./src:/var/www/html
  artisan:
    build:
      context: .
      dockerfile: dockerfiles/php.dockerfile
    volumes:
      - ./src:/var/www/html
    entrypoint: [ "php", "/var/www/html/artisan" ]
  npm:
    image: node:14
    working_dir: /var/www/html
    entrypoint: [ "npm" ]
    volumes:
      - ./src:/var/www/html
```

You cannot use **COPY** or **RUN** commands inside docker compose file. You will need a docker file for that. Bind mount cannot be used in deployment environment. Bind mounts are only useful to make development easier by mirroring the local folder into volume. For this above case we can use a docker file and copy over the snapshot of the code and configuration files so that later we can deploy the application with all the necessary files. The docker file will look like:

```javaScript
FROM nginx:stable-alpine
 
WORKDIR /etc/nginx/conf.d
 
COPY nginx/nginx.conf .
 
RUN mv nginx.conf default.conf
 
WORKDIR /var/www/html
 
COPY src .
```

This docker file will copy the configuration files for the nginx and the source code inside of the container.

After creating the docker file change the build and context of the server service in the docker compose file. If you need something to be copied from your host machine setting the context to any child folder will not work. We must set the context to . Like:

```javaScript
 server:
    build:
      context: .
      dockerfile: dockerfiles/nginx.dockerfile
```

We can then safely comment out the bind mounts of the server service since we have already copied over the files to the container.   
We can then do the same thing for the php service because we are using bind mounts. We can edit the php docker file to copy over the files from src folder to the working directory of the php container.

The php docker file now will look like:

```javaScript
FROM php:8.2.4-fpm-alpine
 
WORKDIR /var/www/html
 
COPY src .
 
RUN docker-php-ext-install pdo pdo_mysql
 
RUN addgroup -g 1000 laravel && adduser -G laravel -g laravel -s /bin/sh -D laravel
 
RUN chown -R laravel:laravel /var/www/html
 
USER laravel
```

The RUN command is used to set permissions for the linux so that data can be copied to the container. The default user of php fpm service is www-data we can create a new user called laravel, so we need to give read permission to read and write data to the container(gives ownership to the laravel user). After this we can comment out the bind mount of php service also. Then if we run the docker compose command with build flag we can see the landing page of laravel which works fine. We can uncomment the bind mounts and use it fine for development mode also.

The complete docker compose file will now look like:

```javaScript
services:
  server:
    build:
      context: .
      dockerfile: dockerfiles/nginx.dockerfile
    ports:
      - '8000:80'
    volumes:
      - ./src:/var/www/html
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - php
      - mysql
  php:
    build:
      context: .
      dockerfile: dockerfiles/php.dockerfile
    volumes:
      - ./src:/var/www/html:delegated
  mysql:
    image: mysql:5.7
    env_file:
      - ./env/mysql.env
  composer:
    build:
      context: .
      dockerfile: dockerfiles/composer.dockerfile
    volumes:
      - ./src:/var/www/html
```

```javaScript
  artisan:
    build:
      context: .
      dockerfile: dockerfiles/php.dockerfile
    volumes:
      - ./src:/var/www/html
    entrypoint: [ "php", "/var/www/html/artisan" ]
  npm:
    image: node:14
    working_dir: /var/www/html
    entrypoint: [ "npm" ]
    volumes:
      - ./src:/var/www/html
```

Docker and containers lets us have same environments for development and production, thus ensuring that it works as expected. It also avoids the use of installing tools on the local machine. We can install the dependencies in the container which can be also used in the production environment containers. It also avoid unexpected errors when moving to production environments. Also we have to watch out for certain things when moving to production environment such as:

1\. We will not use bind mounts in the production environment.

2\. We may need to follow certain additional steps when moving to production, for example for react application we might need to use build command which optimizes the application for production.

3\. Multi container projects might need to be split across multiple hosts or remote machines. 

4\. Trade off between control and responsibility such as configuring an environment for production by yourself and using a managed environment.

In AWS we need to create an EC2 instance along with a VPC and a security group. Then we need configure the security groups to expose all the required ports to world wide web. We need to connect to this instance with SSH and install docker and run the docker container.

**NOTE**: During the development the containers should encapsulate the environment but not necessarily the code. We used bind mounts so that the we don't need to rebuild the image every time when there is a change in the code. But in production mode the container should be standalone, you should not have any source code in your remote machine. The image/container should be the single source of truth. We also must not move the code to the remote machines. That will destroy the idea of containers. We use COPY command instead of bind mount which copies the source code into the container. This ensure that every image runs without any extra surrounding configuration or code no matter where you run it.

To create a new EC2 instance login to aws management console, then search for EC2\. You will see an option to launch an instance. Once you click launch you will see the options to configure the machine. You can choose the instance type, operating system and leave the defaults for VPC and security group. Then click on the launch instance button. You will ne asked to create a key. Give a name to this key. And choose the encryption algorithm. This will download the key file so that we can use this to login to the instance. After downloading the key go to terminal in case of linux and run `chmod 400 "keyfile-name.pem"` To make sure that it is not publicly writable.

This can be skipped in windows. Then make sure that you are in the same folder as the key file inside the terminal. Then run :

`ssh -i "example-1.pem" ec2-user@ec2-98-130-60-223.ap-south-2.compute.amazonaws.com` 

A command like this will be shown when you click the connect option with the steps. 

Type yes to accept the fingerprint and you will be connected to the instance. After this we need to install docker. We can use the following commands:

```javaScript
sudo yum update -y
 
sudo yum -y install docker
 
sudo service docker start
 
sudo usermod -a -G docker ec2-user
```

After this logout and login again. Then run :

`sudo systemctl enable docker`   
Then you can check the docker version using `docker version` command.

We can either move the source code with the dockerfile into the remote machine and build the image there or we can build the image locally and move the image into the remote server. The first option has a lot of unnecessary steps and complexity. For pushing the image to docker hub. First build the image. Before building add a dockerignore file to ignore dockerfile and node\_modules. After building the image we can retag the image using the docker tag command. We need to retag the image in a format that is suitable for dockerhub. i.e,

`docker tag image-name dockerhub_username/repository_name`   
For example:

` docker tag node-deployment-example-1 pgsangeethkumar/node-example-1` 

This will create a new image with the provided tag. Now you will be able to see 2 images when you run docker images command.

This tagging allows us to push the image to docker hub. To push the image we use:

`docker push username/repository_name `   
Which is essentially the tag we added.  
Eg:  
`docker push pgsangeethkumar/node-example-1`   
You need to login to docker hub before pushing. To login use docker login command and enter the username and password. 

To run the image inside of a container in the remote machine we need to use:   
`docker run -d --rm username/repository_name`   
So the command for the above example would be:

`docker run -d --rm -p 80:80 pgsangeethkumar/node-example-1`   
here we are exposing the port 80 of the container. 

Even thought the above step runs the container we will not be able to access our application by visiting the public ip of the server because of the security group configuration. The inbound rule of the default security group is configured such that it only accepts traffic through port 22\. This is used for SSH. To add an inbound rule click on the EC2 instance, under the bottom bar inside security you can see the security group of inbound rule. Click on the security group. This will show the security group. Select the security group which will show the existing inbound rules. click on edit inbound rules. A new tab will be opened where you can see the existing rules. Click on add rule, choose HTTP since we are using http requests. If required you can use https also from the dropdown. Choosing the http will by default select port 80\. We can edit that if we want. You can choose the source to anywhere ipv4 since we want to access this from the internet.

After configuring the security group we will be able to access the application by using the public ipv4 address.

With our current setup we can make the changes locally and build the image and push it to dockerhub. Then we can pull the image inside of the EC2 instance and run it. We use the following commands :

```javaScript
docker build -t node-deployment-example-1
docker build -t node-deployment-example-1 .
docker tag node-deployment-example-1 pgsangeethkumar/node-example-1
docker push pgsangeethkumar/node-example-1
```

Then we need to login to the EC2 instance and use:

`docker pull pgsangeethkumar/node-example-1:latest`   
To pull the image. Then re running the image:

`sudo docker run -d --rm -p 80:80 pgsangeethkumar/node-example-1:latest`   
Our current approach has a couple of disadvantages.

With our current approach we need to do everything manually like creating our instance, configuring security groups etc. We are fully responsible for the server. SSHing to the remote machine and managing it is annoying. We also need to monitor them ourself and scale them manually by ourself.

We can use a managed service like amazon ECS which is **Elastic Container Service**. It is a service that help with running containers by automatically managing and monitoring them. Other cloud providers has similar container hosting services. The advantage of using such a service is that the creating, updating, monitoring and scaling is simplified. This is great if you simply want to deploy a container and run the applications. When we are using a managed service we should follow the rules of the service provider. To work with these containers each provider will provide a different set of rules which we need to use. The tools may differ based on the cloud provider.

AWS ECS thinks in 4 categories:

**1 Containers**: Contains the code and dependencies bundled into a single unit. We can pull the container from docker hub by providing the URI. In the express mode we will get options similar to that of the docker run command. Such adding environment variables, managing ports etc. Additionally we can set up logging and monitoring. 

**2\. Tasks**: Is the blueprint for your application. It tells ECS on how the server configured with docker run should run. A task can include more than 1 container. You can think of a single task as a single remote server which runs one or more containers. By default we are using FARGATE. Fargate is a specific way of launching your container which launches your container in serverless mode. This way aws will store the containers and the configuration in the cloud. When the task is to be executed it will start the container and perform the task and stop the containers. You can also use EC2 instead of fargate. 

This way a new EC2 instance will be created instead. Using fargate is cost effective because we will be paying only for the time that the container is executing. We don't need to pay for idle time.   
**3\. Services**: Service controls how the task should be executed. Here we can add load balancer and it manages all the heavy lifting of redirecting the requests to the running containers behind the scenes. Every task is executed by a service. You will have 1 service per task. 

**4 Clusters**: It is the overall network where the services run. If you have a multi container app you could group multiple containers into one cluster. This makes them logically tied together and all of them can talk to each other. 

We can choose the memory and cpu required for fargate. If you choose a higher configuration it will be relatively more expensive. If you choose a smaller configuration, when a large number of requests comes it will not be enough. AWS also offers auto scaling where it would actually create more than 1 running container handling the requests. You can use autoscaling when you want to handle more workload. 

To update a container we can make the changes locally build the image, tag it and push it to docker hub. AWS ECS cannot automatically update the image, we need to navigate to clusters>defaults>tasks>task definition of the running task> create new revision. Here we should leave all other settings as is. We just want to create the same task again, this way ECS will automatically pull the updated image. When you create a task and start the service in that task aws will automatically use the latest image version. Then click on actions button>update service. This will pull the latest image and restart the service in the task. Alternatively we can click on the update service and select force new deployment where we don't need to create a new task revision. We can see the application running by visiting the public ip address which is available by default. AWS will create a new public ip for every task(including revision of existing tasks). 

Docker compose is not a good option for production applications where we have multiple services. We also need to make consideration for a whole another set of parameters when we deploy the application to production. It is heavily dependent on the hosting provider we are using which requires some extra information which are not part of the compose file. Though docker compose is a good choice for running multiple containers locally. But as soon as moving to cloud where multiple different machines working together it reaches it's limit. We can manually deploy the services to ECS based on the docker compose file(without actually using the docker compose file). We need to manually create the image for each of the services. In ECS we cannot use the name of the container for connecting it with another container because the docker networks are not present here. Our code may not necessarily run inside of a single server due to this we cannot use the name of the containers. 

There is also an exception. If your containers are added in the same task in AWS ECS, then they are guaranteed to run in the same machine, still ECS will not create a docker network, instead it allows you to use localhost as an address in your container application code. 

We can create a cluster to run the backend container, for that we can create a networking only cluster. We can check the option to create a VPC and keep all the rest as defaults. This will create a cluster and the cluster is just the surrounding network for your containers. After the cluster is created we can click on view cluster. Here in the tasks tab we can add the tasks and services. Since services are based on tasks we need to create a task first. We do this under task defenitions. We can create a new task definition and user AWS fargate to have a serverless container environment. Give the task a name, on the role we should have an ecs task execution role available by default, if not you should delete the entire cluster again. Choose the required memory and cpu, on container definitions add container. Give the dockerhub repository name to the image name. Provide the port exposed by the containerized application. We should add the environment variables used by the container. 

We can override the run command here, in our container we had` nodmon index,js` to run the application, but we can override that to user node `index.js`. We can specify that by adding comma instead of space. This allows us to finetune the container runtime based on the environment we are running whether it is development or production. There is no concept of network in ecs. So we cannot directly specify the name of the container to communicate with it. But there is an alternative feature in aws, when we add multiple containers to the same task then these containers can communicate each other using the localhost key. Basically it emulates a local system. After this we can click create which will create our first container. We also had the mongodb container for this application. So we can use add container option to simply add another container. Give the container a name and provide the image name of the official mongo image. Map the default port of mongodb. 

For the backend we used bind mounts. In production we don't use them, so we ignored it. For the mongodb we need a volume because it is where the data is stored. For now add this as empty and add the container. This will now create our new task definition with our 2 containers inside it. Now we can launch a service based on this task with the defined configuration. For this click on the create option under services, choose fargate as launch type, choose the task definition, give service a name, specify the number of tasks as 1, after this create on the next step option. This page shows the network setup, choose the vpc which you had chosen when you initially created the cluster. Under the subnets add both the subnets. Enable auto assign public ip. Then for load balancing choose application load balancer. This will help in optimizing the network traffic and it also helps in adding a custom domain name if we want.

 If you don't have a load balancer we can create an application load balancer and give it any name of our choice. Make sure that internet facing is enabled so that it can be reached from the internet. Use port 80 as port of load balancer. You should use the same vpc which we used for our cluster. Next configure the security settings of the load balancer. If we want we can enable only https, but here we don't need that. In the next step configure the security group, choose the security group of the service. Next we need to configure routing, give it any name of your choice. Choose IP as the target type, this is required since we are using fargate. After this click on register targets. We don't need to specify anything here AWS will automatically add the running container here. So click on review button to review the settings and click on create to create the load balancer. After this in the configuration of networks choose the created load balancer. 

Choose the container port mapping to the load balancer. Choose the target group after this choose the next option, on this page you will be asked to setup auto scaling. Autoscaling is what enables the automatic creation of new containers simultaneously to handle the incoming request volume spikes. Choose create service, and after this the service will be available. On the service page we can click on the tasks page and we can we can view the status of the containers which are being created. We can use the public ip of the network to access the application. 

We can go to application Load balancer page either by searching or going to the EC2 page under which load balancers are present. Load balancer is responsible for checking the health of the containers and restart them if they are not healthy(if they are not responding). This is generally a good behavior because when our application crashes it will be restarted. In the configuration we should specify the correct path (endpoint) of our application so that it will get an output and load balancer verifies that the application is healthy. If this path is not correct, when you use the dns name of the load balancer to visit the website it will not work. If you made any mistake in this we can edit the load balancer settings and update the health checks path.

When using the dns name of the load balancer we don't need to worry about the automatically changing ip addresses. If we want we can define our custom domain name, check the AWS documentation for this.

To update the code changes, we can push the the image to dockerhub and then go to the service page and click on the service, click on update and click on force new deployment, click on review and click on update service. This will restart the service based on the updated container images. The old one will keep running until the new one is deployed and up and running. The old one will automatically get shut down and removed.

We can also create a volume in ECS, for this click on task definitions and click on the latest task definition which you find then click on create new revision to create a new configuration based on the previous one. Here we can review the configuration of the tasks and we can add a volume here to make the data in the db persist. Choose a name for the volume choose EFS(Elastic file system). EFS is a service offered by aws to attach a file system to our serverless container. This way data will remain even if the containers are redeployed. Since there is no file system initially we need to go to the amazon EFS page to create a new file system. Click the option to create a file system, give it any name of your choice, choose the VPC which we used for ECS. Then click on customize where we need to customize one setting. In the first page that comes up click on continue. Then in the next page we will the network access settings. 

We need to create a new security group which we can create by going to the EC2 page and clicking on the security group name. Give the security group a name. Add the security group to the VPC. Then add the inbound rule, choose NFS from the drop down, choose the security group of the containers which lets the containers communicate with the services used in the group. The port and protocol is automatically selected by default and we cannot change it. Without adding this security group and inbound rule the containers and the tasks in ECS would not be able to talk to the EFS. Click create security group. After creating this go back to the EFS configuration page and choose this instead of the default one. After this click next and click on the confirmation and click on create, this will create the file system. Choose the newly created file system in the filesystem id field. We can set an access point if we want which allows us to target some nested path inside of the file system. 

If you have multiple volumes and you don't want to create multiple file systems you can have nested folders on the same file system for the different volumes. But we can now ignore this. If we click on add we will define the volume for the container. This is like adding volumes at the end of docker compose file, this is not the only thing we want to do to connect with the container. We need to click on the container and edit the configuration of the container. We need to go to the storage and logging section and for the mount point choose the volume that we created. The bind it to the path inside of the container where data needs to be stored which we used inside of the docker compose file. After this click update. After this click on create to create a new task revision, go to actions, click on update service, choose redeployment of the service with the new revision, you should also choose the platform version (which ever is the latest). Click review and then click on update.

We can create and manage our own database containers if we want like we did above, but there are couple of issues with this:

* Scaling and managing availability can be challenging. We need to be prepared for multiple read/write operations to occur simultaneously. So we might need to have multiple containers with the same configuration and working on same data base files up and running simultaneously. We need to ensure that these database containers will work on the same database so they are synchronized across each other, which another database does not know. So scaling means more than running 2 containers simultaneously.
* Problems with performance during traffic spikes, if we don't have scaling and if we only have 1 container to do all the work.
* Backups and security, we need to ensure that the data is secured and cannot be accessed without our permission. We need to ensure that data is backed up regularly so we can rollback easily.  
These things don't matter in our local machines.

It is a good idea to use a managed database service, for relational databases there is AWS RDS, for NoSQL there is mongodb atlas. The managed service takes care about all the above issues for you. 

After using the mongodb atlas we need to deploy a container for the react single page application. These kind of application requires a build step. This simply means that we run code in development which is not the code we will deploy later. Because it will be transformed and optimized. This is the case for web applications that run in the browser. The development and production steps are different. We cannot fix this with docker alone. The code we write in react is not natively supported by the browser(JSX code). This code is compiled when during development and it is slower. When we previously ran the react application we use the npm start command which runs the application in development mode which runs the application in the development server. But in production we can't use this. React has it's own build script which will run when you use `npm build` command. 

It will perform the code compilation and optimizations and we can serve these optimized files ourselves with the help of any webserver of our choice. 

We can create separate docker files for development and production. We can create docker files like: `Dockerfile.prod` which is perfectly valid. The dockerfile will look like:

```javaScript
FROM node:14-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD["npm","run","build"]
```

The above script is enough to build the application but it is not enough to deploy it. To tackle this we can use multi stage builds.

Multistage builds allow you to have one dockerfile but define multiple build steps inside of that file. Stages can copy results from each other(created files and folders). You can either build the complete image or selected individual stages upto which you want to build and skipping all stages there after. This is called multi stage builds. So the above mentioned docker file can be modified by using the RUN command instead of the CMD command. Like:

`RUN npm run build`

After this command we need to switch to a different base image, because we only need node to build the optimized files. After build we will get regular html, css and js files. We can use nginx which is a very light weight webserver. **Every FROM instruction will create a new stage in your docker file even if you are using the same image as in the previous step.** We also don't want to discard the changes from the previous step. So we can give a name of our choice to the first step using the `as `keyword. eg:

`FROM node:14-alpine as build`

Then in our second stage we can copy from the first stage using the special syntax `--from=stage_name` with the `COPY `instruction. After this we need to add a space and provide the source path from the file system in the build stage and the destination path. After building the react project the files are stored inside of the build folder so we can specify the path. The destination path for nginx is `/usr/share/nginx/html` , this is the default folder for nginx to serve files. This is listed in the official dockerhub nginx documentation. You can have as many stages as we want for a dockerfile. Then we need to expose the port of nginx. Finally we need to use the command to start the nginx server using `CMD ["nginx","-g","daemon off;"]` The complete docker file will look like:

```javaScript
FROM node:14-alpine as build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
```

After this we need to make adjustments to out application, in our application we are using the localhost to access the backend api. Since we will deploy the frontend in the same task as the backend and the same frontend will be accessible through the same domain name as the backend we can skip the use of localhost in the backend calling url. Because the frontend code is running the users browser and the browser will automatically add the domain name before the requested path in the request. We can also use environment variables to use different URL's for production and development. 

We can use the -f flag to specify the dockerfile name to build the image. Eg:  
`docker build -f frontend/Dockerfile.prod ./frontend` 

We need to specify the full path of the dockerfile. 

To deploy this we can go back to the cluster we had created and inside of the task definition and go to the latest task revision and create a new task revision. In the container definitions part click on add container. Give it a name provide the dockerhub repository image, map the port 80\. We can skip the following health check and environment variables section. We can utilize the startup dependency ordering. We can select our backend service and choose the success option to ensure that only after the successful starting of the backed we will start the frontend container. Since we don't need anything else we can skip the following steps and click on add to add the container. We cannot map 2 containers to same port 80, this will cause a problem and we will not be able to create the task revision. You can technically change the ports of backend or frontend to make sure that it works. You cannot have 2 webservers on the same host. We have an nginx server and node server here. 

We can skip the above approach and create a new task definition and use fargate. Give the task definition a name, choose the same task role we used for backend and provide the minimum required hardware configuration. Then click on add container and provide a container name, choose the dockerhub image. Map port 80\. Since this is a new task it will have it's own url. We can skip the remaining settings and create add. Then create the task definition.

Since the frontend and backend are now in different tasks they will be created in 2 different services. The `process.env.NODE_ENV` holds identifies the environment. When you run the npm start command it will be development, if we run npm run build it will be production in a react application. Based on this we can set the url of the backend. We can also create a new load balancer for the front end application. For this go to EC2 page and click on load balancers, click on create load balancer, give it a name, and ensure that it is internet facing. Choose the port which you want to expose, choose the same vpc as the other load balancer we created earlier for the backend. Then use the same security group for the frontend (since this security group allows all traffic through port 80 only). Then create a target group, give it a name, choose target type as IP, provide the health check path as default because we will access our application from the root path.

Review the settings and create the load balancer. We can check the DNS name of the load balancer which will become the url through which we can access our application. We should also take the DNS name of the backend load balancer so that we can use this inside of our front end application. After adding the url we can build the image and redeploy it to dockerhub.   
We can then create a new service based on the task, choose fargate as launch type, use the cluster name we created, provide a name to the service, set the number of tasks to 1, choose rolling updates. In the next page we need to add the 2 subnets that our vpc provides. For security groups we can choose the same security group of load balancer that we created earlier. For load balancing choose application load balancer, choose the load balancer we created and click on add. Choose the target group name leave all the other settings as is. Click on next and then click on create service. 

We can run builds of a single stage of a multi stage docker file by using the `--target stage_name`parameter with the docker build command. In our above case we can use:

`docker build --target build -f frontent/Dockerfile.prod ./frontend`

  