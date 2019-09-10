# Kubernetes traininig continued

## Discuss Kubernetes core components

- kubectl,
- kubelet,
- kube-proxy,
- api-server.

## Kubernetes architecture

- each node contains of pods, the docker-engine running the pods, kubelet and kube-proxy,
- the docker engine is responsible for running the containers although other providers are also supported,
- kubelet is responsible for starting and monitoring the pods,
- kube-proxy is responsible for securing proper routing inside the cluster by modifying iptables.

## Scaling pods

- stateless applications can be easily horizontally scaled,

> **stateless** - has no state; doesn't write any local files or keep local sessions

- all traditional databases are **stateful**,
- most web applications are **stateless**,
- since our Pods are running the containers using Docker additional steps need to be taken to provide data persistency.

## Pods

- a pod describes an application running on Kubernetes
- a pod can contain one or more tightly coupled containers
- the containers can easily communicate with each other using their local port numbers

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: flaskapp
  labels:
    app: flaskapp
spec:
  containers:
    - name: flaskapp
      image: goraje/flaskapp:1
      ports:
        - name: flask-port
          containerPort: 5000
---

```

### PODS - USEFUL COMMANDS

```shell
kubectl get pod
kubectl describe pod POD_NAME
kubectl expose pod POD_NAME --port=PORT_NUMBER --name=SERVICE_NAME
kubectl port-forward POD_NAME TARGET_PORT_NUMBER:POD_PORT_NUMBER
kubectl attach POD_NAME -i
kubectl exec POD_NAME -- COMMAND
kubectl label pods POD_NAME new_label=new_label_value
kubectl run -i --tty POD_NAME --image=DOCKER_IMAGE_NAME -- COMMAND
```

## Replication Controller

- the Replication Controller ensures that a specified number of pod replicas is running at all times (yield desired state),
- if a Pod crashes, fails gets deleted or is terminated in any other way the Replication Controller will ensure that it is started once again,
- you can use a Replication Controller even with a single replica to ensure that a Pod is always running even post reboot.

```yaml
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: flaskapp-rc
spec:
  replicas: 2
  selector:
    app: flaskapp
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
        - name: flaskapp
          image: goraje/flaskapp:1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
---

```

- kubectl scale --replicas=4 -f FILE_NAME
- kubectl scale --replicas=1 rc/flaskapp-rc

## Replica Set

- introduced as the successor of Replication Controller,
- supports a new selector that can perform filtering according to a set of values (evaluation of custom logical expressions)

## Deployments

- a Deployment declaration allows the Kubernetes user to do deploy and update their apps,
- it describes the desired state of the app,
- the desired state is then ensured by Kubernetes.

A deploment object allows you to:

- create a deployment,
- update a deployment,
- perform rolling updates,
- perform rollbacks,
- pause/resume during deployment.

```yaml
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: flaskapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flaskapp
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
        - name: k8s-training
          image: goraje/flaskapp:1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
---

```

### DEPLOYMENTS - USEFUL COMMANDS

```shell
kubectl get deployments
kubectl get rs
kubectl get pods --show-labels
kubectl rollout status deployment DEPLOYMENT_NAME
kubectl set image DEPLOYMENT_NAME IMAGE_NAME=IMAGE_VERSION
kubectl edit deployment DEPLOYMENT_NAME
kubectl rollout history deployment DEPLOYMENT_NAME
kubectl rollout undo deployment DEPLOYMENT_NAME {--to-revision=n}
```

## Services

- a Service is an abstraction which defines a logical set of Pods and a policy by which to access them,
- set of Pods targeted by a Service are usually determined by a Label Selector,
- Kubernetes-native applications are offered a simple Endpoints API that is updated whenever the set of Pods in a Service changes. Non-native applications are offered a bridged connection,
- Pods are dynamic and as such should not be accessed directly; Services provide the logical bridge between the end user and the Pods.

### TYPES OF ENDPOINTS

- Cluster IP - a VIP address that is accessible only internally from inside the k8s cluster,
- NodePort - tunnels the connection to a specified port on each node (by default Services can be exposed on ports 30000-32767),
- LoadBalancer - used to assign a load balancer with an external IP while using a cloud provider (eg. Openstack, AWS, Google Cloud etc.).

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: flaskapp-service
spec:
  ports:
    - port: 5000
      targetPort: flask-port
      protocol: TCP
  selector:
    app: flaskapp
  type: NodePort
---

```

You can concatenate multiple resource types into a single YAML file, where "---" is used as a separator.

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: flaskapp
  labels:
    app: flaskapp
spec:
  containers:
    - name: flaskapp
      image: goraje/flaskapp:1
      ports:
        - name: flask-port
          containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: flaskapp-service
spec:
  ports:
    - port: 5000
      targetPort: flask-port
      protocol: TCP
  selector:
    app: flaskapp
  type: NodePort
---

```

## Labels

- key/value pairs that can be attached to k8s objects,
- used to tag different resources eg. environment=dev, department=magic,
- labels are not unique and multiple labels can be added to one object.

```yaml
metadata:
  name: some-name
  labels:
    app: some-app
    environment: prod
    department: magic
```

- you can use labels to tag nodes,

```shell
kubectl label node NODE_NAME LABEL_KEY=LABEL_VALUE
kubectl label node NODE_NAME LABEL_KEY-
```

```yaml
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: flaskapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flaskapp
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
        - name: k8s-training
          image: goraje/flaskapp:1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
      nodeSelector:
        hw: high-performance
---

```

## Health Checks

- your application may malfunction, but the container or the Pod might still keep on working,
- you can perform health checks either by running a command in the container periodically or using a periodic HTTP check on the endpoint

```yaml
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: flaskapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flaskapp
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
        - name: k8s-training
          image: goraje/flaskapp:1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          livenessProbe:
            httpGet:
              path: /
              port: 5000
            initialDelaySeconds: 15
            timeoutSeconds: 30
---

```

- livenessProbe indicates if the container is running,
- readinessProbe indicates whether the container is ready to serve requests.

```yaml
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: flaskapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flaskapp
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
        - name: k8s-training
          image: goraje/flaskapp:1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          livenessProbe:
            httpGet:
              path: /
              port: 5000
            initialDelaySeconds: 15
            timeoutSeconds: 30
          readinessProbe:
            httpGet:
              path: /
              port: 5000
            initialDelaySeconds: 15
            timeoutSeconds: 30
---

```

## Pod state

- all pods have a status field

### STATUSES

- running - bound to a node, containers were created, at least one container is running,
- pending - Pod is accepted but is not running; no resources, still downloading the image,
- succeeded - all containers were successfully run and have now terminated,
- failed - opposite of succeeded,
- unknown - cannot determine the state of the Pod; could be do to kubelete failure/network failure.

### CONDITIONS

- PodScheduled - scheduled to a node,
- Ready - Pod can serve requests,
- Initialized - initialization containers were successfully started,
- Unschedulable - cannot schedule to a node,
- ContainersReady - all containers inside the Pod have reached the Ready status.

## Pod Lifecycle

init container -> main container (post star hook -> probes -> pre stop hook)

## ConfigMaps

- used to store configuration files that don't contain secrets,
- this way you can inject configuration settings to a container.

```python
import os

from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def hello_world():
    message = dict(
            message=os.environ.get('FLASK_MESSAGE'),
            version='3'
            )
    return jsonify(message)
```

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: flaskapp-configmap
data:
  APP_MESSAGE: Your custom message
---

```

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: flaskapp
  labels:
    app: flaskapp
spec:
  containers:
    - name: flaskapp
      image: goraje/flaskapp:3
      envFrom:
        - configMapRef:
            name: flaskapp-configmap
      ports:
        - name: flask-port
          containerPort: 5000
---

```

## StatefulSet

- introduced to run stateful applications,
- apps that need a stable Pod hostname,
- stable storage,
- scaling the StatefulSet will preserve the data,
- typical usecases - databases.

## DaemonSet

- ensure that every single node runs the same Pod resource,
- new Pods will be started on every new node that is added to the cluster,
- typical usecases: monitoring, api-gateways, reverse proxies.
