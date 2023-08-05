# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from github.com.metaprov.modelaapi.services.k8score.v1 import k8score_pb2 as github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2


class CoreK8sServiceStub(object):
    """///////////////////////////// Jobs

    The Core K8s service is used to list and get a kubernetes object
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListK8sSecrets = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sSecrets',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListSecretsRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListSecretResponse.FromString,
                )
        self.GetK8sSecret = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sSecret',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetSecretRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetSecretResponse.FromString,
                )
        self.ListK8sServices = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sServices',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListServicesRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListServicesResponse.FromString,
                )
        self.GetK8sService = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sService',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetServiceRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetServiceResponse.FromString,
                )
        self.ListK8sDeployments = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sDeployments',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListDeploymentsRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListDeploymentsResponse.FromString,
                )
        self.GetK8sDeployment = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sDeployment',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetDeploymentRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetDeploymentResponse.FromString,
                )
        self.ListK8sPods = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sPods',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListPodsRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListPodsResponse.FromString,
                )
        self.GetK8sPod = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sPod',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetPodRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetPodResponse.FromString,
                )
        self.ListK8sJobs = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sJobs',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListJobsRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListJobsResponse.FromString,
                )
        self.GetK8sJob = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sJob',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetJobRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetJobResponse.FromString,
                )
        self.ListEvents = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListEvents',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListEventsRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListEventsResponse.FromString,
                )
        self.GetContainerLog = channel.unary_unary(
                '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetContainerLog',
                request_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetContainerLogRequest.SerializeToString,
                response_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetContainerLogResponse.FromString,
                )


class CoreK8sServiceServicer(object):
    """///////////////////////////// Jobs

    The Core K8s service is used to list and get a kubernetes object
    """

    def ListK8sSecrets(self, request, context):
        """//////////////// secret
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetK8sSecret(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListK8sServices(self, request, context):
        """//////////////// service
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetK8sService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListK8sDeployments(self, request, context):
        """//////////////// deployment
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetK8sDeployment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListK8sPods(self, request, context):
        """//////////////// pod
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetK8sPod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListK8sJobs(self, request, context):
        """////////////// jobs
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetK8sJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEvents(self, request, context):
        """Events

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetContainerLog(self, request, context):
        """//////////////////////////// container log
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CoreK8sServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListK8sSecrets': grpc.unary_unary_rpc_method_handler(
                    servicer.ListK8sSecrets,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListSecretsRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListSecretResponse.SerializeToString,
            ),
            'GetK8sSecret': grpc.unary_unary_rpc_method_handler(
                    servicer.GetK8sSecret,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetSecretRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetSecretResponse.SerializeToString,
            ),
            'ListK8sServices': grpc.unary_unary_rpc_method_handler(
                    servicer.ListK8sServices,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListServicesRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListServicesResponse.SerializeToString,
            ),
            'GetK8sService': grpc.unary_unary_rpc_method_handler(
                    servicer.GetK8sService,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetServiceRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetServiceResponse.SerializeToString,
            ),
            'ListK8sDeployments': grpc.unary_unary_rpc_method_handler(
                    servicer.ListK8sDeployments,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListDeploymentsRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListDeploymentsResponse.SerializeToString,
            ),
            'GetK8sDeployment': grpc.unary_unary_rpc_method_handler(
                    servicer.GetK8sDeployment,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetDeploymentRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetDeploymentResponse.SerializeToString,
            ),
            'ListK8sPods': grpc.unary_unary_rpc_method_handler(
                    servicer.ListK8sPods,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListPodsRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListPodsResponse.SerializeToString,
            ),
            'GetK8sPod': grpc.unary_unary_rpc_method_handler(
                    servicer.GetK8sPod,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetPodRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetPodResponse.SerializeToString,
            ),
            'ListK8sJobs': grpc.unary_unary_rpc_method_handler(
                    servicer.ListK8sJobs,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListJobsRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListJobsResponse.SerializeToString,
            ),
            'GetK8sJob': grpc.unary_unary_rpc_method_handler(
                    servicer.GetK8sJob,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetJobRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetJobResponse.SerializeToString,
            ),
            'ListEvents': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEvents,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListEventsRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListEventsResponse.SerializeToString,
            ),
            'GetContainerLog': grpc.unary_unary_rpc_method_handler(
                    servicer.GetContainerLog,
                    request_deserializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetContainerLogRequest.FromString,
                    response_serializer=github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetContainerLogResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CoreK8sService(object):
    """///////////////////////////// Jobs

    The Core K8s service is used to list and get a kubernetes object
    """

    @staticmethod
    def ListK8sSecrets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sSecrets',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListSecretsRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListSecretResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetK8sSecret(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sSecret',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetSecretRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetSecretResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListK8sServices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sServices',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListServicesRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListServicesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetK8sService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sService',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetServiceRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListK8sDeployments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sDeployments',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListDeploymentsRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListDeploymentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetK8sDeployment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sDeployment',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetDeploymentRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetDeploymentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListK8sPods(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sPods',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListPodsRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListPodsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetK8sPod(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sPod',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetPodRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetPodResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListK8sJobs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListK8sJobs',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListJobsRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListJobsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetK8sJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetK8sJob',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetJobRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetJobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEvents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/ListEvents',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListEventsRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.ListEventsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetContainerLog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/github.com.metaprov.modelaapi.services.k8score.v1.CoreK8sService/GetContainerLog',
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetContainerLogRequest.SerializeToString,
            github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_k8score_dot_v1_dot_k8score__pb2.GetContainerLogResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
