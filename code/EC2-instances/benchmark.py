# Comments with the help of chatgpt

# Import required modules
import requests  # Module for making HTTP requests
import time  # Module for handling time-related functions
from multiprocessing import Process  # Module for enabling parallel function execution
from metrics import analytics  # Importing a custom function to gather performance metrics
from clusters import link
from datetime import datetime

# what for ?
# 1000 GET requests sequentially.
# 500 GET requests, then one minute sleep, followed by 1000 GET requests.

# Define a function to send HTTP requests to the /cluster1 endpoint of the load balancer
def call_cluster1():
    # Define the URL for the /cluster1 endpoint
    print(link)
    url = link + "/cluster1"

    # Print a message indicating that 1000 requests to /cluster1 are being initiated
    print("=====================================")
    print("1000 requests to /cluster1 loading ...")
    print("======================================= \n")

    # Loop 1000 times to send requests to /cluster1 endpoint
    for i in range(1000):
    #for i in range(200):
        try:
            # Send a GET request to the specified URL with headers
            response = requests.get(url, headers={"content-type": "application/json"})
            # status prompt
            print("Status of req - " + str(i) + "/1K : " + str(response.status_code))
            # Raise an exception if the response contains an HTTP error status code
            response.raise_for_status()  
        except pip._vendor.requests.RequestException as e:
            # Handle any exceptions that occur during the request and print an error message
            print(f"Request [ {url} ] failure: {e}")

    # Print a message indicating that requests to /cluster1 have been sent
    print("\n 1000 Requests done!")
    print("======================================= \n")


# Define a function to send HTTP requests to the /cluster2 endpoint of the load balancer
def call_cluster2():
    # Define the URL for the /cluster2 endpoint
    url = link + "/cluster2"

    # Print a message indicating that 500 requests to /cluster2 are being initiated
    print("=======================================")
    print("500 requests to /cluster2 loading ...")
    print("======================================= \n")

    # Loop 500 times to send requests to /cluster2 endpoint
    for i in range(500):
    #for i in range(100):
        try:
            # Send a GET request to the specified URL with headers
            response = requests.get(url, headers={"content-type": "application/json"})
            # Print the status code of the response
            print("Status of req - " + str(i) + "/0.5K : " + str(response.status_code))
            # Raise an exception if the response contains an HTTP error status code
            response.raise_for_status()
        except pip._vendor.requests.RequestException as e:
            # Handle any exceptions that occur during the request and print an error message
            print(f"Request [ {url} ] failure: {e}")

    print(" \n 500 Requests done!")
    print("======================================= \n")


    print(" \n Cluster 2 Sleeping...")
    print("======================================= \n")

    # Pause execution for 60 seconds
    time.sleep(60)
    #time.sleep(10)

    print(" \n Cluster 2 Awake...")
    print("======================================= \n")

    # Print a message indicating that 1000 additional requests to /cluster2 are being initiated
    print("======================================= \n")
    print("1000 requests to /cluster2 loading ...")
    print("======================================= \n")
    
    # Loop 1000 times to send additional requests to /cluster2 endpoint
    for i in range(1000):
    #for i in range(200):
        try:
            # Send a GET request to the specified URL with headers
            response = requests.get(url, headers={"content-type": "application/json"})
            #status 
            print("Status of req - " + str(i) + "/1K : " + str(response.status_code))
            # Raise an exception if the response contains an HTTP error status code
            response.raise_for_status()
        except pip._vendor.requests.RequestException as e:
            # Handle any exceptions that occur during the request and print an error message
            print(f"Request to {url} failed: {e}")

    # Print a message indicating that additional requests to /cluster2 have been sent
    print("======================================= \n")
    print("Requests done!")
    print("======================================= \n")

# Check if the script is being run directly (not imported as a module)
if __name__ == '__main__':
    # start time for metric
    overall_start_time = datetime.utcnow()

    # Create two separate processes to execute call_cluster1 and call_cluster2 functions in parallel
    process1 = Process(target=call_cluster1)
    process2 = Process(target=call_cluster2)
    
    # Start both processes simultaneously
    process1.start()
    process2.start()
    
    # Wait until both processes complete their tasks
    process1.join()
    process2.join()
    
    # endtime for metric 
    overall_end_time = datetime.utcnow()
    
    print("Waiting 90 secondes for the cloudwatch... \n")
    time.sleep(90)
    # Call a function (analytics) to gather performance metrics
    print("Starting the script execution... \n")
    analytics(overall_start_time, overall_end_time)
    print("Script execution completed. \n")