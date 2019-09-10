default: install

RELEASE := metallb
NAMESPACE := metallb-system

install:
	helm install --wait --timeout=600 --values ./valuesMetalLB.yaml --name $(RELEASE) --namespace $(NAMESPACE) stable/metallb

clean:
	helm del --purge $(RELEASE)
