default: install

RELEASE := traefik
NAMESPACE := kube-system

install:
	helm install --wait --timeout=600 --values ./valuesTraefik.yaml --name $(RELEASE) --namespace $(NAMESPACE) stable/traefik

clean:
	helm del --purge $(RELEASE)
