from aws_cdk import (
    CustomResource,
    Duration,
    RemovalPolicy,
    Stack,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    custom_resources as _custom
)

from constructs import Construct

class RemedyDeleteDefaultVpcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = _iam.Role(
            self, 'role', 
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )
        
        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )
        
        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'ec2:DescribeRegions',
                    'ec2:DescribeVpcs',
                    'ec2:DeleteVpc',
                    'ec2:DescribeInternetGateways',
                    'ec2:DetachInternetGateway',
                    'ec2:DeleteInternetGateway',
                    'ec2:DescribeSubnets',
                    'ec2:DeleteSubnet'
                ],
                resources = ['*']
            )
        )

        remedy = _lambda.Function(
            self, 'remedy',
            code = _lambda.Code.from_asset('remedy'),
            handler = 'remedy.handler',
            runtime = _lambda.Runtime.PYTHON_3_9,
            architecture = _lambda.Architecture.ARM_64,
            timeout = Duration.seconds(30),
            memory_size = 128,
            role = role
        )
       
        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+remedy.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        provider = _custom.Provider(
            self, 'provider',
            on_event_handler = remedy
        )

        resource = CustomResource(
            self, 'resource',
            service_token = provider.service_token
        )
