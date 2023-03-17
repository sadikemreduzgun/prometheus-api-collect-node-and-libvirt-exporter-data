from reach_time import *


def check_installed():

    node_query_exist = False
    libvirt_query_exist = False

    query_node = "node_load1"
    query_libvirt = "libvirt_domain_block_stats_allocation"

    url_node = f"http://localhost:9090/api/v1/query?query={query_node}"
    query_libvirt = f"http://localhost:9090/api/v1/query?query={query_libvirt}"

    try:
        data_node = rq.get(url_node).json()
        data_libvirt = rq.get(query_libvirt).json()

        if data_node['status'] == 'success':
            node_query_exist = True

        if data_libvirt['status'] == 'success':
            libvirt_query_exist = True

    except:
        pass

    return node_query_exist, libvirt_query_exist
