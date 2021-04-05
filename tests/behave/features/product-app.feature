@productapp
Feature: Test product app deployment and verify autoscaling
  As an Developer
  I want to deploy my application on gke with hpa
  So that I can obtain the product list from  https://reqres.in/api/products/ when I query my app

  Acceptance Criteria
    - product app pod is in running status
    - product app hpa is configured
    - Upon generating load, hpa will scale up number of app pods

   Scenario: Check product app deployment is running
    Given I have connected to the kube api
    When I check pods with name "product-app" in "product-app" namespace
    Then I should see the "product-app" pods are "Running" in "product-app" namespace


  Scenario: Check hpa exists in product-app namespace
    Given I have connected to the kube api
    Then I check for hpa in product-app namespace it should exist

   Scenario: Connect to the app and verify we return product-list
     Given I have connected to the kube api
     When I deploy a pod to connect to my product-app
     Then it should display full product list
     Then I clean up the pod

   Scenario: Generate load and verify hpa has scaled product-app replicas
     Given I have connected to the kube api
     When I deploy my load-generator deploymemt
     Then I should see my product app deployment replicas scale to three pods
     Then I clean up the load-generator deployment
