from kubernetes import client, config, watch

'''
This file will contain all common methods, imported throughout the rest of the test files
'''

def cluster_connect():
    """
    default class needed everytime to authenticate against k8s cluster
    """
    config.load_kube_config()  # when testing locally
    return client


def get_pod_from_name(pod_name, pod_namespace):
    """
     Create an instance of the API class
    """
    try:
        v1 = client.CoreV1Api()
        pod_assert = []
        all_pods_meta = v1.list_namespaced_pod(namespace=pod_namespace)

        # # ### Comment out when troubleshooting ###
        # print('DEBUG: ------------------------------------------------')
        # for item in all_pods_meta.items:
        #     print(
        #         "%s\t%s\t%s" %
        #         (item.status.pod_ip,
        #             item.metadata.name,
        #              item.status.phase))
        # print('END: --------------------------------------------------')

        for item in all_pods_meta.items:
            if str(pod_name) in str(item.metadata.name):
                print('We matched', pod_name)
                pod_assert.append(pod_name)
                return pod_name

        if len(pod_assert) == 0:
            return

    except Exception as err:
        print(err)


def get_pod_status_from_name(pod_name, pod_status, pod_namespace):
    """
    Create an instance of the API class
    """
    try:
        v1 = client.CoreV1Api()
        namespaced_pods = v1.list_namespaced_pod(namespace=pod_namespace)
    except Exception as err:
        print(f"Failure calling 'list_namespaced_pod': {err}")
    pods = [pod for pod in namespaced_pods.items if pod_name in pod.metadata.name]
    if len(pods) <= 0:
        print(f"💣  Unable to find pod named {pod_name}*, found these pods in namespace {pod_namespace}:")
        for target_pod in namespaced_pods.items:
            print(f"{target_pod.metadata.name}\t{target_pod.status.phase}")
    else:
        target_pods = [rpod for rpod in pods if rpod.status.phase == pod_status]
        if len(target_pods) <= 0:
            print(f"💣 Could not find pod names {pod_name} in state {pod_status}. Actual pod state:")
            for target_pod in pods:
                print(f"{target_pod.metadata.name}\t{target_pod.status.phase}")
            return 0
        else:
            return len(target_pods)


def delete_pod(pod_name, namespace):
    v1 = client.CoreV1Api()
    api_response = v1.delete_namespaced_pod(
        name=pod_name,
        namespace=namespace,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    return api_response
    print("Pod deleted. status='%s'" % str(api_response.status))


# This function watchs for events on a specific object list you specify and checks if object with name you specify exists in event logs
# Example can be found here: https://github.com/kubernetes-client/python/blob/master/examples/pod_namespace_watch.py
def watch_events(object_list, timeout, object_name):
    try:
        # Max count of streamed events to watch for if condition below to become true
        count = 100
        w = watch.Watch()
        # Wait for `count` number of events to occur within the `timeout_seconds` threshold
        for event in w.stream(object_list, timeout_seconds=timeout):
            print("Event: %s %s" % (
                event['type'],
                event['object'].metadata.name)
                  )
        count -= 1
        if not count:
            if event['object'].metadata.name == object_name:
                w.stop()
                print("Finished event stream.")
                return True
            else:
                return False
    except Exception as err:
        print(err)
