#!/bin/bash
# A menu driven shell script sample template 
## ----------------------------------
# Step #1: Define variables
# ----------------------------------
RED='\033[0;41;30m'
STD='\033[0;0;39m'
YEL='\033[0;43;30m'
 
# ----------------------------------
# Step #2: User defined function
# ----------------------------------

show_containers(){
    echo "--------------------------"
	if [ "$(docker ps -a --format "Name: {{.Names}}\nContainer ID: {{.ID}}\nImage: {{.Image}}\nPorts: {{.Ports}}\nStatus: {{.Status}}\n--------------------------")" ]; then
	docker ps -a --format "Name: {{.Names}}\nContainer ID: {{.ID}}\nImage: {{.Image}}\nPorts: {{.Ports}}\nStatus: {{.Status}}\n--------------------------"
	else
	echo "No Container available!"
	fi
	Manage_Containers
}

Create_Containers(){
local_dir=~/Learning/Docker/DockDir
docker_dir=/data

printf "Please provide the image name for container.\nfollowing Images are availabe on host.\n-------------------------------\nImages\n"
docker images --format "{{.Repository}}:{{.Tag}}"
printf "________________________________\nImage Name: "
read image
printf "________________________________\n"

printf "Please provide the Docker network name.\nfollowing docker networks are availabe on host.\n-------------------------------\n"
docker network ls --format "{{.Name}}"
printf "________________________________\nDocker Network Name: "
read net
printf "________________________________\n"

printf "Please provide the Name for container.\nfollowing Names are already in use.\n-------------------------------\nNames in use:\n"
docker ps -a --format "{{.Names}}"
printf "________________________________\nName: "
read name
printf "________________________________\n"

printf "Please provide the local port for mapping.\nfollowing ports are already in use.\n-------------------------------\nPorts in use:\n"
docker ps -a --format "{{.Ports}}"
printf "________________________________\nLocal Port: "
read local_port
printf "________________________________\n"
read -p "Please provide the docker port for mapping: " docker_port

docker run -d --network $net -p $local_port:$docker_port -v $local_dir:$docker_dir --name $name $image && printf "Container $name creared successfully.\n"
Manage_Containers
}

Delete_Containers(){
	printf "Following containers are available on docker host:\n________________________________\n"
	docker ps -a --format "Name: {{.Names}}\nContainer ID: {{.ID}}\nStatus: {{.Status}}\n--------------------------"
	read -p "Type the container Name/ID to delete single container or 'ALL' to delete all containers: " cont_to_delete
	if [ "$cont_to_delete" == "all" -o "$cont_to_delete" == "All" -o "$cont_to_delete" == "ALL" ]; then
		docker rm -f $(docker ps -a -q) 2> /dev/null || echo -e "${RED}Error......Try again${STD}"
	else
		docker rm $cont_to_delete 2> /dev/null || echo -e "${RED}Error......Try again${STD}"
	fi
Manage_Containers
}

Stop_Containers(){
	printf "Following containers are running:\n________________________________\n"
	docker ps --filter "status=running" --format "Name: {{.Names}}\nID: {{.ID}}\n________________________________"
	read -p "Type the container Name/ID to stop single container or 'ALL' to stop all running containers: " cont_to_stop
	if [ "$cont_to_stop" == "all" -o "$cont_to_stop" == "All" -o "$cont_to_stop" == "ALL" ]; then
		docker stop $(docker ps -a -q)
	else
		docker stop $cont_to_stop
	fi
Manage_Containers
}

Start_Containers(){
	printf "Following containers are stopped on Docker host:\n________________________________\n"
	docker ps --filter "status=exited" --format "Name: {{.Names}}\nID: {{.ID}}\nStatus: {{.Status}}\n________________________________"
	read -p "Type the container Name/ID to start single container or 'ALL' to start all stopped containers: " cont_to_start
	if [ "$cont_to_start" == "all" -o "$cont_to_start" == "All" -o "$cont_to_start" == "ALL" ]; then
		docker start $(docker ps -a --filter "status=exited" --format {{.ID}})
	else
		docker start $cont_to_start
	fi
Manage_Containers
}

Manage_Containers_options(){
	local choice
	read -p "Enter choice [ 0 - 5] " choice
	case $choice in
		1) show_containers;;
		2) Create_Containers ;;
        3) Stop_Containers ;;
		4) Start_Containers ;;
        5) Delete_Containers ;;
        6) ;;
		0) break ;;
		*) echo -e "${RED}Error......Try again${STD}" && Manage_Containers_options
	esac
}
Manage_Containers(){
	echo "----------------------------------"	
	echo " M A N A G E - C O N T A I N E R S"
	echo "----------------------------------"
    echo "1. Show Containers"
	echo "2. Create Containers"
	echo "3. Stop Containers"
	echo "4. Start Containers"
    echo "5. Delete Containers"
	echo "6. Go to Main Menu"
	echo "0. Exit"
    Manage_Containers_options
}
 
####################Manage Docker Images#######################
Show_Images(){
    echo "--------------------------"
docker images --format "Image: {{.Repository}}:{{.Tag}}\nID: {{.ID}}\nSize: {{.Size}}\n--------------------------"
Manage_Images
}

Pull_Images(){
    read -p "Please provide the image name with version(default is latest)" image_name
docker pull $image_name
Manage_Images
}

Delete_Images(){
    printf "Following Images are available:\n"
    docker images --format "{{.Repository}}:{{.Tag}}"
    read -p "Please provide the images name seprated by space: " image_name
    docker image rm $image_name
	Manage_Images
}

Manage_Image_options(){
	local choice
	read -p "Enter choice [ 0 - 4] " choice
	case $choice in
		1) Show_Images ;;
        2) Pull_Images ;;
        3) Delete_Images ;;
        4) ;;
		0) break ;;
		*) echo -e "${RED}Error......Try again${STD}" && Manage_Image_options
	esac
}
Manage_Images(){
	echo "--------------------------"	
	echo " M A N A G E - I M A G E S"
	echo "--------------------------"
    echo "1. Show Images"
	echo "2. Pull Images"
	echo "3. Delete Images"
	echo "4. Go to Main Menu"
	echo "0. Exit"
    Manage_Image_options
}


#########################Manage Networks#############################
Show_Networks(){
	echo "--------------------------"
	docker network ls --format "Name: {{.Name}}\nNetwork-ID: {{.ID}}\nDriver: {{.Driver}}\nScope: {{.Scope}}\n--------------------------"
	Manage_Networks
}

Create_Networks(){
	echo "--------------------------"
	read -p "Network Name?: " nw_name
	read -p "Driver(e.g. bridge)?: " driver
	printf "Please provide CIDR.\nFollowing Subnet IPs are already in use.\n--------------------------\n"
	for net in $(docker network ls --format {{.Name}})
	do
	docker inspect $net --format "Name: {{.Name}}"
	docker inspect $net --format "Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}"
	docker inspect $net --format "Gateway: {{range .IPAM.Config}}{{.Gateway}}{{end}}"
	echo "--------------------------"
	done
	read -p "Subnet IP(e.g. 192.168.0.0/16)?: " subnet
	docker network create --driver=$driver --subnet=$subnet $nw_name
	Manage_Networks
}

Delete_Networks(){
	echo "--------------------------"
	echo "Following Networks are available."
	docker network ls --format "Name: {{.Name}}"
	read -p "Network Name/Names sep by space?: " nw
	docker network rm $nw || echo "$nw deleted successfully!"
	Manage_Networks
}
Manage_Network_options(){
	local choice
	read -p "Enter choice [ 0 - 5] " choice
	case $choice in
		1) Show_Networks ;;
        2) Create_Networks ;;
        3) Delete_Networks ;;
        4) ;;
		0) break ;;
		*) echo -e "${RED}Error......Try again${STD}" && Manage_Network_options
	esac
}

Manage_Networks(){
	echo "------------------------------"	
	echo " M A N A G E - N E T W O R K S"
	echo "------------------------------"
    echo "1. Show Networks"
	echo "2. Create Networks"
	echo "3. Delete Networks"
	echo "4. Go to Main Menu"
	echo "0. Exit"
        Manage_Network_options
}
SSH2VMs(){
    read -p "Provide the VM IP/Name: " vm
	read -p "Provide the user name(default is root): " user
	if [ "$user" == "" ]; then
		ssh -o ConnectTimeout=5 root@$vm || echo "Unable to connect, Try again!"
	else
		ssh -o ConnectTimeout=5 $user@$vm || echo "Unable to connect, Try again!"
	fi
	break
}
# Connect to Containers
SSH(){
	list_ssh_cont(){
	for c in $(docker ps --format {{.Names}})
	do
		if [ $(docker inspect $c --format='{{range $p, $conf := .NetworkSettings.Ports}}{{$p}}{{end}}') == 22/tcp ]; then
			docker inspect $c --format="{{.Name}}" | tr -cd "[:alnum:]"
			docker inspect $c --format='{{range $p, $conf := .NetworkSettings.Ports}} ---> {{(index $conf 0).HostPort}} {{end}}'
		fi
	done
	}

	if [ "$(list_ssh_cont)" != "" ]; then
		printf "Following Containers are available for SSH:\n--------------------------\n"
		list_ssh_cont
		read -p "Enter the container SSH port: " ssh_port
		read -p "Enter the user name(default is root): " ssh_user
			if [ "$ssh_user" == "" ]; then
				ssh root@0.0.0.0 -p $ssh_port
			else
				ssh $ssh_user@0.0.0.0 -p $ssh_port
			fi
	else
		echo -e "${YEL}No Container is available for SSH!${STD}"
	fi
	Connect2Container
}

Exec(){
	running_cont(){
		docker ps --filter "status=running" --format "Names: {{.Names}}\nID: {{.ID}}\n--------------------------"
	}
	if [ "$(running_cont)" ]; then
		printf "Following Containers are available:\n--------------------------\n"
		running_cont
		read -p "Type the container Name/ID to connect: " cont
		docker exec -it $cont bash 2> /dev/null || echo -e "${RED}Error......Try again${STD}"
	else
		echo -e "${YEL}No Container is available!${STD}"
	fi
	Connect2Container
}

Connect2Container_options(){
	local choice
	read -p "Enter choice [ 0 - 3] " choice
	case $choice in
		1) SSH ;;
        2) Exec ;;
        3) ;;
		0) break ;;
		*) echo -e "${RED}Error......Try again${STD}" && Connect2Container_options
	esac
}
Connect2Container (){
	echo "----------------------------------------"	
	echo " C O N N E C T - 2 - C O N T A I N E R S"
	echo "----------------------------------------"
    echo "1. Connect via SSH"
	echo "2. Connect via Exec"
	echo "3. Go to Main Menu"
	echo "0. Exit"
    Connect2Container_options
}
# function to display menus
show_menus() {
	echo "---------------------------"	
	echo " M A N A G E - D O C K E R "
	echo "---------------------------"
	echo "1. Manage Containers"
	echo "2. Manage Images"
    echo "3. Manage Networks"
    echo "4. SSH2VMs"
    echo "5. Connect2Container"
	echo "0. Exit"
}
# read input from the keyboard and take a action
# invoke the one() when the user select 1 from the menu option.
# invoke the two() when the user select 2 from the menu option.
# Exit when user the user select 3 form the menu option.
Manage_Docker_options(){
	local choice
	read -p "Enter choice [ 0 - 5] " choice
	case $choice in
		1) Manage_Containers ;;
		2) Manage_Images ;;
        3) Manage_Networks ;;
        4) SSH2VMs ;;
        5) Connect2Container ;;
		0) break;;
		*) echo -e "${RED}Error......Try again${STD}"
	esac
}
 
# ----------------------------------------------
# Step #3: Trap CTRL+C, CTRL+Z and quit singles
# ----------------------------------------------
#trap '' SIGINT SIGQUIT SIGTSTP
 
# -----------------------------------
# Step #4: Main logic - infinite loop
# ------------------------------------
while true
do
	show_menus
	Manage_Docker_options
done