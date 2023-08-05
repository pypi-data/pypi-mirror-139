def use_aws_secret_extra(
    secret_name="aws-secret",
    aws_access_key_id_name="AWS_ACCESS_KEY_ID",
    aws_secret_access_key_name="AWS_SECRET_ACCESS_KEY",
    aws_region=None,
):
    """An operator that configures the container to use AWS credentials.

    AWS doesn't create secret along with kubeflow deployment and it requires users
    to manually create credential secret with proper permissions.

    ::

        apiVersion: v1
        kind: Secret
        metadata:
          name: aws-secret
        type: Opaque
        data:
          AWS_ACCESS_KEY_ID: BASE64_YOUR_AWS_ACCESS_KEY_ID
          AWS_SECRET_ACCESS_KEY: BASE64_YOUR_AWS_SECRET_ACCESS_KEY
    """

    def _use_aws_secret(task):
        from kubernetes import client as k8s_client

        task.container.add_env_variable(
            k8s_client.V1EnvVar(
                name="AWS_ACCESS_KEY_ID_EXTRA",
                value_from=k8s_client.V1EnvVarSource(
                    secret_key_ref=k8s_client.V1SecretKeySelector(
                        name=secret_name, key=aws_access_key_id_name
                    )
                ),
            )
        ).add_env_variable(
            k8s_client.V1EnvVar(
                name="AWS_SECRET_ACCESS_KEY_EXTRA",
                value_from=k8s_client.V1EnvVarSource(
                    secret_key_ref=k8s_client.V1SecretKeySelector(
                        name=secret_name, key=aws_secret_access_key_name
                    )
                ),
            )
        )

        if aws_region:
            task.container.add_env_variable(
                k8s_client.V1EnvVar(name="AWS_REGION", value=aws_region)
            )
        return task

    return _use_aws_secret
