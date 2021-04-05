import pprint

from behave import *
from kubernetes import client, utils

import common

product_list = [{"color": "#98B2D1", "id": 1, "name": "cerulean", "pantone_value": "15-4020", "year": 2000},
                {"color": "#C74375", "id": 2, "name": "fuchsia rose", "pantone_value": "17-2031", "year": 2001},
                {"color": "#BF1932", "id": 3, "name": "true red", "pantone_value": "19-1664", "year": 2002},
                {"color": "#7BC4C4", "id": 4, "name": "aqua sky", "pantone_value": "14-4811", "year": 2003},
                {"color": "#E2583E", "id": 5, "name": "tigerlily", "pantone_value": "17-1456", "year": 2004},
                {"color": "#53B0AE", "id": 6, "name": "blue turquoise", "pantone_value": "15-5217", "year": 2005}]
sample_app_yaml = "tests/behave/resources/sample-app.yaml"
load_generator_yaml = "tests/behave/resources/load-generator.yaml"


@then(u'I check for hpa in product-app namespace it should exist')
def step_impl(context):
    try:
        context.co = client.CustomObjectsApi()
        assert context.co.get_namespaced_custom_object("autoscaling", "v2beta1", "product-app",
                                                       "horizontalpodautoscalers", "product-app-hpa-policy")
    except Exception as err:
        raise AssertionError("Failed to find HorizontalPodAutoscaler " + str(err))


@when(u'I deploy a pod to connect to my product-app')
def step_impl(context):
    try:
        k8s_client = client.ApiClient()
        utils.create_from_yaml(k8s_client, sample_app_yaml, namespace="product-app")
        common.watch_events(context.v1.list_pod_for_all_namespaces, 10, "sample-app")
        assert common.get_pod_status_from_name("sample-app", "Succeeded", "product-app")
    except Exception as err:
        raise AssertionError(f"Failed to create sample app {str(err)}")


@then(u'it should display full product list')
def step_impl(context):
    try:
        logs = client.CoreV1Api().read_namespaced_pod_log("sample-app", namespace="product-app",
                                                          container="sample-app")
        if str(product_list) in logs:
            assert True
        else:
            print(f"log output : \n\n {logs}")
            assert False
    except Exception as err:
        raise AssertionError(f"Could not read pod logs for 'product-app/sample-app' failed with exception: '{err}'")


@then(u'I clean up the pod')
def step_impl(context):
    try:
        assert common.delete_pod("sample-app", "product-app")
    except Exception as err:
        raise AssertionError(f"Failed to delete sample app {str(err)}")


@when(u'I deploy my load-generator deploymemt')
def step_impl(context):
    try:
        k8s_client = client.ApiClient()
        utils.create_from_yaml(k8s_client, load_generator_yaml, namespace="product-app")
        common.watch_events(context.v1.list_pod_for_all_namespaces, 75, "sample-app")
    except Exception as err:
        raise AssertionError(f"Failed to create deployment {str(err)}")


@then(u'I should see my product app deployment replicas scale to three pods')
def step_impl(context):
    try:
        v1 = client.AppsV1Api()
        deploy = v1.read_namespaced_deployment(name="product-app-deployment", namespace="product-app")
        replicas = deploy.status.replicas
        pprint.pprint(replicas)
        assert 3 == replicas
    except Exception as err:
        raise AssertionError(f"Failed to check product-app replicas {str(err)}")


@then(u'I clean up the load-generator deployment')
def step_impl(context):
    try:
        v1 = client.AppsV1Api()
        assert v1.delete_namespaced_deployment("load-generator", "product-app")
    except Exception as err:
        raise AssertionError(f"Failed to delete load-generator deployment {str(err)}")
