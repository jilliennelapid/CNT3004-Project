# CNT3004-Project

To test on Google Cloud:

1) Clone the repository to your desired local directory with `git clone`.
2) Open the local version of the repository `CNT3004-Project`.
3) On a browser, navigate to [Google Cloud](https://console.cloud.google.com/).
4) Create a new project.
5) Navigate to the [Compute Engine](https://console.cloud.google.com/compute/instances) page for your project, and select on the 'VM Instances' tab.
6) Create a VM Instance with the 'Create Instance' button
7) Configure your instance to suit your billing affordance.
8) Start your instance.
9) Open the instance. Scroll to network interfaces:
* In `server.py` change `host` to the IP address listed under 'Primary internal IP address'
* In `client.py` change `host` to the IP address listed under 'External IP address'. Remember that this address can change with Starting/Stoping the instance or overtime.
8) Scroll back to the top and open an SSH window with the 'SSH' button.
9) Upload the file `server.py` into the SSH with the 'Upload File' button.
10) Create a directory for the server files named `server_files` in your main directory.
> use command `mkdir server_files` to create the folder.
11) Create a file named `passwords.txt` in your main directory.
> use command `touch passwords.txt` to create the file.
12) In `view.py`, update `FILE_STORAGE_DIR` to the path of `server_files`
> use command `realpath server_files` to get the exact path; copy it and assign the value to `FILE_STORAGE_DIR`
13) In `view.py` in the method `validate_credentials()` in the class `LoginView`, update `filepath` to the path of `passwords.txt`.\
> use command `realpath passwords.txt` to get the exact path; copy it and assign the value to `filepath`
14) Start the server with the command `python3 server.py`.
15) Start the program by running `main.py`.
16) When finished, Stop your VM instance to avoid extra billing.
