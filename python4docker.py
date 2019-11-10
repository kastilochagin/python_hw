#Prior to running this script please install the Docker Engine Python SDK (https://docker-py.readthedocs.io)

import docker

client = docker.from_env() #by having the DOCKER_HOST environment variable unset we follow the default client behaviour to connect to the local (Unix) socket
deeperclient = docker.APIClient(base_url='unix://var/run/docker.sock') #Low-level API comes here for our need to find out (below) additional details of containers and images

print()

if len(client.containers.list(all=True)) == 0: #here we check whether we have any containers at all
 print("No containers (of any status) found")
else:
 for container in client.containers.list(all=True): #and the boolean parameter is used for listing all containers (not just running, as by default)
  container.reload()
  if container.status == "exited" or container.status == "dead": #looking for "stopped" and "dead" containers
   print("Warning: {} container found. With ID: {} and name: {}".format(container.status, container.short_id, container.name))
  else: #here we look for the rest of possible containers, neither exited nor dead
   mapped_ports = deeperclient.inspect_container(container.id)['NetworkSettings']['Ports']
   path = deeperclient.inspect_container(container.id)['Path']
   container_birth_time = deeperclient.inspect_container(container.id)['Created']
   print("Neither exited nor dead container found. ID: {}, image: {}, command: {}, created: {}, status: {}, mapped ports (if any): {}, name: {}".format(container.short_id, container.image, path, container_birth_time, container.status, mapped_ports, container.name)) #output is similar to "docker ps -a"
   print("Container inspection:")
   print(deeperclient.inspect_container(container.id)) #output is identical to "docker inspect"

print()

if len(client.images.list()) == 0: #here we check whether we have any images at all
 print("No images found")
else:
 print("List of images found:")
 for image in client.images.list():
  repotags = deeperclient.inspect_image(image.id)['RepoTags']
  image_birth_time = deeperclient.inspect_image(image.id)['Created']
  size = deeperclient.inspect_image(image.id)['Size']
  print("RepoTags: {}, ID: {}, created: {}, size: {} byte(s)".format(repotags, image.short_id, image_birth_time, size)) #output is similar to "docker image ls"

print()
