from behave import *

import common


@given(u'I have connected to the kube api')
def step_impl(context):
    try:
        context.v1 = common.cluster_connect().CoreV1Api()
    except Exception as err:
        raise AssertionError("failed with exception: " + str(err))


@when(u'I check pods with name "{pod_name}" in "{pod_namespace}" namespace')
def step_impl(context, pod_name, pod_namespace):
    try:
        print("Checking if pod with names " + pod_name + " exists" + " in " + pod_namespace + " namespace")
        assert common.get_pod_from_name(pod_name, pod_namespace)
    except Exception as err:
        raise AssertionError("failed with exception: Unable to find pod with name " + pod_name + str(err))

@then(u'I should see the "{pod_name}" pods are "{pod_status}" in "{pod_namespace}" namespace')
def step_impl(context, pod_name, pod_status, pod_namespace):
    try:
        print("Checking if pod with names " + pod_name + " is " + pod_status + " in " + pod_namespace + " namespace")
        result = common.get_pod_status_from_name(pod_name, pod_status, pod_namespace)
        print (f'output: {result}')
        assert result
    except Exception as err:
        raise AssertionError("failed with exception: Unable to find Pod " + pod_name + " in Namespace " + pod_namespace
                             + " in " + pod_status + " State" + str(err))
