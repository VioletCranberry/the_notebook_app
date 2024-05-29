import argparse

from kubernetes import client, config


class KubernetesManager:
    def __init__(self, namespace: str = "the-notebook-app"):
        """
        Initialize the Kubernetes manager and load the Kubernetes configuration.
        """
        config.load_incluster_config()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
        self.networking_v1 = client.NetworkingV1Api()

        self.namespace = namespace

    def create_deployment(self, name: str, args: argparse.Namespace):
        """
        Create a Kubernetes deployment for an instance.
        """
        container = client.V1Container(
            name=name,
            image=args.image,
            image_pull_policy="Never",  # Note: for minikube testing only
            ports=[client.V1ContainerPort(container_port=args.port)],
            args=[
                f"--hard-memory-limit={args.hard_memory_limit}",
                f"--soft-memory-limit={args.soft_memory_limit}",
                f"--timeout-sec={args.timeout_sec}",
                f"--host={args.host}",
                f"--port={args.port}",
            ],
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": name}),
            spec=client.V1PodSpec(containers=[container]),
        )

        spec = client.V1DeploymentSpec(
            replicas=1,
            template=template,
            selector={"matchLabels": {"app": name}},
        )

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=name),
            spec=spec,
        )

        self.apps_v1.create_namespaced_deployment(
            namespace=self.namespace, body=deployment
        )

        # Create a service for the deployment
        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1ServiceSpec(
                selector={"app": name},
                ports=[
                    client.V1ServicePort(port=args.port, target_port=args.port)
                ],
            ),
        )

        self.core_v1.create_namespaced_service(
            namespace=self.namespace, body=service
        )

        self.update_ingress(name)

    def update_ingress(self, name: str, port: int = 5000, remove: bool = False):
        """
        Update the Ingress resource to add or remove paths for services.
        """
        ingress = self.networking_v1.read_namespaced_ingress(
            name="the-notebook-app-ingress", namespace=self.namespace
        )

        paths = ingress.spec.rules[0].http.paths
        if remove:
            paths = [p for p in paths if p.backend.service.name != name]
        else:
            path = client.V1HTTPIngressPath(
                path=f"/{name}",
                path_type="Prefix",
                backend=client.V1IngressBackend(
                    service=client.V1IngressServiceBackend(
                        name=name, port=client.V1ServiceBackendPort(number=port)
                    )
                ),
            )
            paths.append(path)

        ingress.spec.rules[0].http.paths = paths
        self.networking_v1.replace_namespaced_ingress(
            name="the-notebook-app-ingress",
            namespace=self.namespace,
            body=ingress,
        )

    def scale_deployment(self, name: str, replicas: int):
        """
        Scale a Kubernetes deployment to the specified number of replicas.
        """
        scale = client.V1Scale(spec=client.V1ScaleSpec(replicas=replicas))
        self.apps_v1.patch_namespaced_deployment_scale(
            name=name, namespace=self.namespace, body=scale
        )

    def delete_deployment(self, name: str):
        """
        Delete a Kubernetes deployment and its associated service.
        """
        self.apps_v1.delete_namespaced_deployment(
            name=name, namespace=self.namespace, body=client.V1DeleteOptions()
        )
        self.core_v1.delete_namespaced_service(
            name=name, namespace=self.namespace, body=client.V1DeleteOptions()
        )
        self.update_ingress(name, remove=True)

    def get_service_ip(self, name: str) -> str:
        """
        Get the external IP address of a service.
        """
        service = self.core_v1.read_namespaced_service(
            name, namespace=self.namespace
        )
        if (
            service.status.load_balancer
            and service.status.load_balancer.ingress
        ):
            return service.status.load_balancer.ingress[0].ip
        return service.spec.cluster_ip
