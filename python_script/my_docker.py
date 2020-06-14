import docker, types, json
import sys
from os import system

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[0;32;7m"
BLINK = "\033[0;5;32m"
YELLOW = "\033[0;33m"
END = "\033[0m"

class manage_docker:
    def __init__(self, menu_list):
        self.client = docker.from_env()
        self.menu_list = menu_list
    
    def version(self):
        return(json.dumps(self.client.version(), indent=2))

    def menu(self):
        for idx, val in enumerate(self.menu_list):
            print(YELLOW, idx+1,val, END)
    
    def answer(self, text):
        return(input("{} {} {}".format(GREEN,text,END)))

class manage_docker_images(manage_docker):
    def __init__(self):
        super().__init__(self)

    def image_list(self):
        image_l = []
        for i in (self.client.images.list()):
            image_l += str(i).replace("<Image: '", "").replace("'>", "").replace(" ", "").replace("'", "").split(',')
        return image_l
    
    def image_delete(self):
        id = self.answer("Please enter the image number seprated by comma.\nTo delete the multiple images enter image number in decending orde(e.g.14,13,6)):").split(',')
        for i in id:
            self.client.images.remove(self.image_list()[int(i)-1])


    def pull_image(self, tag="latest"):
        self.repo = input("Please enter the image name:")
        tag = input("Please enter the tag:")
        self.client.images.pull(self.repo, tag)

class manage_networks(manage_docker_images, manage_docker):
    def list_network_names(self):
        return[val.name for val in self.client.networks.list(greedy=True)]

    def list_networks(self):
        for val in self.client.networks.list(greedy=True):
            print("-----------------------\nNetwork Name:",val.name,"\nID:",val.short_id)
            for n in val.attrs.get('IPAM').get('Config'):
                print("Subnet: " + n.get('Subnet'), "\nGateway: " + n.get('Gateway'))
        print("-----------------------")

    def create_network(self):
        ans = self.answer("A for Advance and B for basic network option?")
        if ans.lower() == "b":
            print("Following Networks are avalable on Docker host.")
            self.list_networks()
            name = self.answer("Please provide the network name: ")
            driver = self.answer("Please provide the network driver: ")
            self.client.networks.create(name, 
                                        driver=driver,
                                           )
        elif ans.lower() == "a":
            print("Following Networks are avalable on Docker host.")
            self.list_networks()
            name = self.answer("Please provide the network name: ")
            driver = self.answer("Please provide the network driver: ")
            ipam_pool = docker.types.IPAMPool(
                                            subnet=self.answer('Subnet(e.g. 192.168.52.0/24): '),
                                            gateway=self.answer('Gateway(e.g. 192.168.52.254): ')
                                            )
            ipam_config = docker.types.IPAMConfig(
                                                pool_configs=[ipam_pool]
                                                )
            self.client.networks.create(name, 
                                        driver=driver,
                                        ipam=ipam_config
                                        )

    def delete_network(self):
        cont_list = [val for val in self.client.networks.list(greedy=True)]
        for idx, val in enumerate(cont_list):
            print("\n-----------------------\n",idx+1,"Name:",val.name,"\n   ID:",val.short_id)
            for n in val.attrs.get('IPAM').get('Config'):
                print("   Subnet: " + n.get('Subnet'), "\n   Gateway: " + n.get('Gateway'))
        print("-----------------------")
        index = self.answer("Please enter the network number seprated by comma.\nTo start the multiple networks enter image number in decending orde(e.g.14,13,6)):").split(",")
        for i in index:
            cont_list[int(i)-1].remove()

class manage_docker_containers(manage_networks, manage_docker_images, manage_docker):
    def list_containser_names(self):
        return [container.name for container in self.client.containers.list(all)]

    def list_containers(self):
        if self.client.containers.list(all):
            for val in self.client.containers.list(all):
                print("Name:",val.name,"\n", str(val).replace("<Container: ", "ID:").replace(">", ""),"\n", "Image:", str(val.image).replace("<Image: '","").replace("'>", ""),"\n", "Status:", val.status)
        else:
            print("No Containers available!")
            
    def advance_create_containers(self, name, image, network, local_port, d_port):
        self.name = name
        self.image = image
        self.network = network
        self.local_port = local_port
        self.d_port = d_port
        self.client.containers.run(self.image,
                                        detach=True,
                                        tty=True,
                                        network=self.network,
                                        name=self.name,
                                        ports={
                                            self.d_port: self.local_port},
                                        volumes={
                                            '/Users/summit/Learning': {'bind': '/data', 'mode': 'rw'}})
    
    def basic_create_containers(self, image):
        self.image = image
        self.name = self.answer("Containe Name: ")
        self.client.containers.run(
                                    self.image,
                                    detach=True,
                                    name=self.name,
                                    tty=True,
                                    volumes={
                                        '/Users/summit/Learning': {'bind': '/data', 'mode': 'rw'}})
    def delete_container(self):
        if self.client.containers.list(all):
            cont_list = [val for val in self.client.containers.list(all)]
            for idx, val in enumerate(self.client.containers.list(all)):
                print(idx+1, val.name, "-", val.status)
            index = self.answer("Please enter the container number seprated by comma.\nTo delete the multiple images enter image number in decending orde(e.g.14,13,6)):").split(",")
            for i in index:
                cont_list[int(i)-1].remove(force= True)
        else:
            print("No Containers available!")

    def stop_container(self):
        if self.client.containers.list(all):
            cont_list = [val for val in self.client.containers.list(all)]
            for idx, val in enumerate(self.client.containers.list(all)):
                print(idx+1, val.name, "-", val.status)
            index = self.answer("Please enter the container number seprated by comma.\nTo stop the multiple images enter image number in decending orde(e.g.14,13,6)):").split(",")
            for i in index:
                cont_list[int(i)-1].stop(timeout= 120)
        else:
            print("No Containers available!")

    def start_container(self):
        if self.client.containers.list(all):
            cont_list = [val for val in self.client.containers.list(all)]
            for idx, val in enumerate(self.client.containers.list(all)):
                print(idx+1, val.name,"-", val.status)
            index = self.answer("Please enter the container number seprated by comma.\nTo start the multiple images enter image number in decending orde(e.g.14,13,6)):").split(",")
            for i in index:
                cont_list[int(i)-1].start()
        else:
            print("No Containers available!")
    
    def connect_container(self):
        self.list_containers()
        self.cont = self.answer("container name/ID: ")
        system("docker exec -ti %s /bin/bash"%(self.cont))



"""    def choice_menu(self):
        choice = {}
        for idx, val in enumerate(self.menu_list):
            choice[idx]=val
        return choice

    def menu_selection(self):
        choice = int(input())
        if choice <= len(self):
            return(self.menu_list[choice-1])"""