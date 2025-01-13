import json
import pandas as pd
from google.cloud import container
from google.api_core import exceptions  # Import exceptions directly

# Mapping for image type to more descriptive text
image_type_mapping = {
    "COS_CONTAINERD": "Container-Optimized OS with containerd (cos_containerd)",
    "UBUNTU": "Ubuntu",
    "UBUNTU_CONTAINERD": "Ubuntu with containerd",
    "CUSTOM_IMAGE": "Custom Image",
    "ML_IMAGE": "Machine Learning Optimized Image",
    "BIG_DATA_IMAGE": "Big Data Optimized Image",
    "LEGACY_IMAGE": "Legacy Image"
}

disk_type_mapping = {
    "pd-standard": "Standard persistent disk",
    "pd-balanced": "Balanced persistent disk",
    "pd-ssd": "SSD persistent disk",
    "regional-ssd": "Regional SSD",
    "local-ssd": "Local SSD",
    "confidential-vm": "Confidential VM"
}

def get_cluster_details(project_id, location, cluster_name):
    cluster_client = container.ClusterManagerClient()
    cluster_full_name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}"

    try:
        cluster = cluster_client.get_cluster(name=cluster_full_name)
    except exceptions.NotFound:  # Using the correct exception
        print(f"Cluster '{cluster_name}' not found in project '{project_id}' and location '{location}'.")
        return {}

    details = {
        "Cluster Name": cluster.name,
        "Version Cluster": cluster.current_master_version,
        "Control plane address range": getattr(cluster.private_cluster_config, "master_ipv4_cidr_block", "Not available"),
        "Private Endpoint": getattr(cluster.private_cluster_config, "private_endpoint", "Not available"),
        "Network": cluster.network,
        "Subnet": cluster.subnetwork,
        "Cluster Pod IPv4 range (default)": getattr(cluster.ip_allocation_policy, "cluster_ipv4_cidr_block", "Not available"),
        "Maximum Pods per Node": getattr(cluster.default_max_pods_constraint, "max_pods_per_node", "Not available"),
        "Labels": cluster.resource_labels,
        "Vertical Pod Autoscaling": "disabled" if getattr(cluster.vertical_pod_autoscaling, "enabled", False) is False else "enabled",
        "Autoscaling profile": getattr(cluster.autoscaling, "profile", "Not available"),
    }

    return details

def get_node_pool_details(project_id, location, cluster_name, node_pool_name):
    cluster_client = container.ClusterManagerClient()
    node_pool_full_name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}/nodePools/{node_pool_name}"

    try:
        node_pool = cluster_client.get_node_pool(name=node_pool_full_name)
    except exceptions.NotFound:  # Using the correct exception
        print(f"Node pool '{node_pool_name}' not found in cluster '{cluster_name}'.")
        return {}

    # Initialize details dictionary
    details = {
        "Node Pool name": node_pool.name,
        "Node version": node_pool.version,
        "Number of nodes": calculate_total_nodes(node_pool),
        "Autoscaling": "On" if getattr(node_pool.autoscaling, "enabled", False) else "Off",
        "Node zones": node_pool.locations,
    }

    # Safely access instance template and disks information if available
    if hasattr(node_pool, 'config'):
        image_type = getattr(node_pool.config, "image_type", "Not available")
        disk_type = getattr(node_pool.config, "disk_type", "Not available")
        details.update({
            "Image type": image_type_mapping.get(image_type, image_type),
            "Machine type": getattr(node_pool.config, "machine_type", "Not available"),
            "Boot disk type": disk_type_mapping.get(disk_type, disk_type),
            "Boot disk size (per node)": f"{getattr(node_pool.config, 'disk_size_gb', 'Not available')} GB",
            "Taints": get_taints(node_pool.config.taints),
            "GCE instance metadata": getattr(node_pool.config, "metadata", "Not available"),
        })

    return details

def calculate_total_nodes(node_pool):
    if hasattr(node_pool, "instance_group_urls"):
        total_nodes = len(node_pool.instance_group_urls)
        return f"{total_nodes} total ({1} per zone)"
    elif hasattr(node_pool, "initial_node_count"):
        return f"{node_pool.initial_node_count} total"
    return "Not available"

def get_taints(taints):
    if not taints:
        return "Not available"
    
    formatted_taints = []
    for taint in taints:
        key_value = f"{taint.key}={taint.value}"  # Only key and value
        formatted_taints.append(key_value)
    
    return ", ".join(formatted_taints)

from kubernetes import client, config