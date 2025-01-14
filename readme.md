# Fetching Detail Information GKE Service

GKE-Details is a programme designed to fetch information on Cluster and Nodepool in Google Kubernetes Engine (GKE). The information you will get by running this program is related to three essential details which are Cluster, Nodepool, Image and Disk with the following details.

#### Related Cluster

- Cluster Name
- Cluster Version
- Control plane address range
- Private Endpoint
- Network
- Subnet
- Cluster Pod IPv4 range (default)
- Maximum Pods per Node
- Labels
- Vertical Pod Autoscaling
- Autoscaling profile

#### Related Nodepool

- Node Pool name
- Node version
- Number of nodes
- Autoscaling
- Node zones

#### Related Image and Disk

- Image type
- Machine type
- Boot disc type
- Boot disc size (per node)
- Taints
- GCE instance metadata

## Code Configuration

To run this project, you will need to prepare the fire environment you are using with the following steps:

```
pip install pandas
pip install google-cloud
pip install google-cloud-container
pip install google-api-core
```

## Environment Configuration

Since your running.py script explicitly specifies the environment when calling the load_projects function (e.g., load_projects(‘prod’) and load_projects(‘non-prod’)), you do not need to use environment variables in the terminal to set the environment.

```
export ENV=prod 
export ENV=non-prod 
 ```

## Running Code 

To run this programme, you just need to execute this command
```
python running.py
```
