from aws_cdk import (
    core as cdk,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_ssm as _ssm,
)


class RemedyDeleteDefaultVpcsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
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
                    'ec2:DeleteSubnet',
                    'events:DisableRule',
                    'ssm:GetParameter'
                ],
                resources = ['*']
            )
        )

        remedy = _lambda.Function(
            self, 'remedy',
            code = _lambda.Code.from_asset('remedy'),
            handler = 'remedy.handler',
            runtime = _lambda.Runtime.PYTHON_3_9,
            timeout = cdk.Duration.seconds(30),
            role = role,
            environment = dict(
                RULE = 'delete-default-vpcs'
            ),
            architecture = _lambda.Architecture.ARM_64,
            memory_size = 128
        )
       
        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+remedy.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = cdk.RemovalPolicy.DESTROY
        )

        rule = _events.Rule(
            self, 'rule',
            schedule = _events.Schedule.cron(
                minute = '*',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )
        rule.add_target(_targets.LambdaFunction(remedy))

        parameter = _ssm.StringParameter(
            self, 'parameter',
            description = 'Delete Default VPCs',
            parameter_name = 'delete-default-vpcs',
            string_value = rule.rule_name,
            tier = _ssm.ParameterTier.STANDARD
        )
