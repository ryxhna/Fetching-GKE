import json
import pandas as pd
from google.api_core import exceptions
from main import get_cluster_details, get_node_pool_details

def load_projects():
    file_path = 'project/NON-PROD.json'
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Load all projects from the JSON file
projects = load_projects()
all_details = []

# Loop through each project and retrieve details
for project in projects:
    project_id = project['project_id']
    location = project['location']
    cluster_name = project['cluster_name']
    node_pool_name = project['node_pool_name']

    try:
        cluster_details = get_cluster_details(project_id, location, cluster_name)
        node_pool_details = get_node_pool_details(project_id, location, cluster_name, node_pool_name)

        # Combine the details if both were retrieved successfully
        if cluster_details and node_pool_details:
            combined_details = {**cluster_details, **node_pool_details}
            all_details.append(combined_details)
        else:
            print(f"Could not retrieve details for project {project_id}.")

    except Exception as e:
        print(f"Error retrieving details for project {project_id}: {e}")

# Save all details to CSV
if all_details:
    output = 'output'
    output_path = output + '/Asset List GKE NON-PROD.csv' 
    
    df = pd.DataFrame(all_details)
    df.to_csv(output_path, index=False)
    print("Created Asset List for GKE NON-PROD")
else:
    print("No details found to save.")