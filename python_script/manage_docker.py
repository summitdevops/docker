import my_docker
import sys, os
from os import system

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE_red = "\033[0;31;7m"
BLINK = "\033[0;5;32m"
END = "\033[0m"

def answer(text):
    return(input("{} {} {}".format(GREEN,text,END)))

def blink_answer(text):
    return(input("{} {} {}".format(BLINK,text,END)))

def red_text(text):
    return("{} {} {}".format(RED,text,END))

def error(text):
    print("{} {} {}".format(REVERSE_red,text,END))

def head_line(text):
    new_text = text.upper().replace(" ","-").split()
    for t in new_text:
        print(GREEN + "---------------->"," ".join(t),"<----------------", END)

Docker_Menu = ["Show Docker Version",
    "Manage Docker Images",
    "Manage Docker Containers",
    "Manage Docker Networks",
   ]
Docker_Image_Menu = ["Show Docker Images",
    "Pull Docker Images",
    "Delete Docker Images",
    "Go Back to main menu"]

Docker_container_Menu = ["Show Docker Containers",
    "Run Docker Container",
    "Stop Docker container",
    "Start Docker container",
    "Delete Docker Container",
    "Connect Container",
    "Go Back to main menu"]

Docker_Network_Menu = ["Show Docker Networks",
    "Create Docker Networks",
    "Delete Docker Networks",
    "Go Back to main menu"]

"""
def selection():
    choice = int(input(f"Please select the option from {1}...{len(Docker_Menu)} to continue:"))
    if manage.choice_menu(Docker_Menu)[choice-1] == Docker_Menu[choice-1]:
        print(Docker_Menu[choice-1])"""

main_menu = my_docker.manage_docker(Docker_Menu)
image = my_docker.manage_docker_images()
container=my_docker.manage_docker_containers()
network = my_docker.manage_networks()
image_sub_menu =  my_docker.manage_docker(Docker_Image_Menu)
container_sub_menu = my_docker.manage_docker(Docker_container_Menu)
network_sub_menu = my_docker.manage_docker(Docker_Network_Menu)

def image_menu():
    try:
        head_line("Manage Images")
        ans_image = 0
        while ans_image < 5:
            image_sub_menu.menu()
            ans_image = int(blink_answer("Please select an option?"))
            if ans_image == 1:
                for idx, val in enumerate(image.image_list()):
                    print(idx+1, val)
            elif ans_image == 2:
                image.pull_image()
            elif ans_image == 3:
                for idx, val in enumerate(image.image_list()):
                    print(idx+1, val)
                image.image_delete()
            elif ans_image == 4:
                menu_selection()
                break
    except ValueError:
        error("Wrong Value provided!")
    except KeyboardInterrupt:
        print("")
        error("You cancelled the operation!")

def container_menu():
    head_line("Manage Containers")
    try:
        ans_cont = 0
        while ans_cont <= 6:
            container_sub_menu.menu()
            ans_cont = int(blink_answer("Please select an option?"))
            if ans_cont == 1:
                container.list_containers()
            elif ans_cont == 2:
                choice = answer("A for advance and B for basic container options :")
                if choice.lower() == "a":
                    print(red_text("Names in use: "), container.list_containser_names())
                    name_n = answer("Please provide the container name:")
                    print(red_text("Available Images: "), image.image_list())
                    image_name = answer("Please provide the image name:")
                    print(red_text("Available Networks: ") , network.list_network_names())
                    network_name = answer("Please provide the network name:")
                    local_port = answer("Please provide the local_port:")
                    d_port = answer("Please provide the docker port:")
                    if name_n not in container.list_containser_names() and image_name in image.image_list() and network_name in network.list_network_names():
                        container.advance_create_containers(name_n, image_name, network_name, local_port, d_port)
                    else:
                        print("try again")
                elif choice.lower() == "b":
                    print(red_text("Available Images(Local): "), image.image_list())
                    image_name = answer("Please provide the image name:")
                    container.basic_create_containers(image_name)

            elif ans_cont == 3:
                container.stop_container()

            elif ans_cont == 4:
                container.start_container()

            elif ans_cont == 5:
                container.delete_container()

            elif ans_cont == 6:
                container.connect_container()

            elif ans_cont == 7:
                menu_selection()
                break

    except ValueError:
        error("Wrong Value provided!")
    except KeyboardInterrupt:
        print("")
        error("You cancelled the operation!")

def network_menu():
    try:
        head_line("Manage Networks")
        ans_nw = 0
        while ans_nw <= 4:
            network_sub_menu.menu()
            ans_nw = int(blink_answer("Please select an option?"))

            if ans_nw == 1:
                network.list_networks()

            elif ans_nw == 2:
                network.create_network()

            elif ans_nw == 3:
                network.delete_network()
            
            elif ans_nw == 4:
                menu_selection()
                break
    except ValueError:
        error("Wrong Value provided!")
    except KeyboardInterrupt:
        print("")
        error("You cancelled the operation!")
    except:
        error("Try again!!!")

def menu_selection():
    try:
        system('clear')
        head_line("Manage Docker")
        main_menu.menu()
        ans = int(blink_answer("Please select an option?"))
        if ans == 1:
            print(main_menu.version())
            blink_answer("Enter to go back:")
            menu_selection()
        elif ans == 2:
            image_menu()
        elif ans == 3:
            container_menu()
        elif ans == 4:
            network_menu()
    except ValueError:
        error("Wrong Value provided!")
    except KeyboardInterrupt:
        print("")
        error("You cancelled the operation!")


menu_selection()


