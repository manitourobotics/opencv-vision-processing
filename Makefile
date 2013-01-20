# run create_config first
SHELL=bash
configuration_file=make_config.txt
-include $(configuration_file)

cipher=blowfish #Doesn't need to be very secure; use a fast cipher
send_files=processor.py main.py

# run create_config first

# remote_ip from $(configuration_file)
# I assume you are using a ssh key without 

create_config:
	# check if file exists
	if [ ! -e $(configuration_file) ]; then cp $(configuration_file).example $(configuration_file); fi

deploy: create_config
	scp $(send_files) $(remote_username)@$(remote_ip):

deploy_run: 
	ssh -c $(cipher) -Y $(remote_ip) 

