import boto3
import json
import sys

from cerberus import Validator
from botocore.exceptions import ClientError
from deepdiff import DeepDiff
from loguru import logger


class ECS_DevOps_Utils:
    
    __client = None
    __session = None

    def __init__(self, session):
        self.__session = session
        self.__client = session.client('ecs')

    @property
    def client(self):
        self.__client

    def deploy(self, user_config):

        config_schema = {
            
            'name': {

                'type'      : 'string',
                'required'  : True,
                'empty'     : False
            },

            'clusterName': {

                'type'      : 'string',
                'required'  : True,
                'empty'     : False
            },

            'volumes': {
                
                'type': 'list',
                'default': [],
                'schema': {

                    'type': 'dict'
                }
            },
            
            'loadBalancer': {

                'type': 'dict',
                'required': True,
                'schema': {

                    'name': {

                        'type'      : 'string',
                        'required'  : True,
                        'empty'     : False
                    },

                    'listenerPort': {

                        'type'      : 'integer',
                        'required'  : True,
                        'default'   : 443,
                        'empty'     : False
                    },

                    'conditions': {

                        'type': 'dict',
                        'default': {

                            'pathPattern'       : [],
                            'hostHeader'        : [],
                            'httpHeader'        : {},
                            'httpRequestMethod' : [],
                            'sourceIp'          : []
                        },
                        'schema': {

                            'pathPattern': {
                                
                                'type': 'list',
                                'default': [],
                                'schema': {
                                    'type': 'string'
                                }
                            },

                            'hostHeader': {
                                
                                'type': 'list',
                                'default': [],
                                'schema': {
                                    'type': 'string'
                                }
                            },

                            'httpHeader': {
                                
                                'type': 'dict',
                                'default': {},
                                'schema': {
                                    
                                    'name': {
                                        
                                        'rename'    : 'HttpHeaderName', 
                                    },

                                    'HttpHeaderName': {
                                        
                                        'type'      : 'string',
                                        'required'  : True,
                                        'empty'     : False
                                    },

                                    'values': {

                                        'rename'    : 'Values'
                                    },

                                    'Values': {
                                        
                                        'type'      : 'list',
                                        'required'  : True,
                                        'minlength' : 1,
                                        'schema': {
                                            'type': 'string'
                                        }
                                    },
                                }
                            },

                            'httpRequestMethod': {
                                
                                'type': 'list',
                                'default': [],
                                'schema': {
                                    'type': 'string'
                                }
                            },

                            'sourceIps': {
                                
                                'type': 'list',
                                'default': [],
                                'schema': {
                                    'type': 'string'
                                }
                            },
                        }
                    },

                    'healthCheck': {

                        'type': 'dict',
                        'default': {

                            'intervalSeconds'       : 30,
                            'checkPath'             : '/',
                            'checkPort'             : 'traffic-port',
                            'checkProtocol'         : 'HTTP',
                            'checkTimeoutSeconds'   : 5,
                            'port'                  : 80,
                            'protocol'              : 'HTTP',
                            'healthyThreshold'      : 5,
                            'unhealthyThreshold'    : 2
                        },

                        'schema': {

                            'intervalSeconds': {
                                'type'      : 'integer',
                                'default'   : 30,
                                'empty'     : False
                            },

                            'checkPath': {
                                'type'      : 'string',
                                'default'   : '/'
                            },

                            'checkPort': {
                                'type'      : 'string',
                                'default'   : 'traffic-port',
                                'empty'     : False
                            },

                            'checkProtocol': {
                                'type'      : 'string',
                                'default'   : 'HTTP',
                                'empty'     : False
                            },

                            'checkTimeoutSeconds': {
                                'type'      : 'integer',
                                'default'   : 5,
                                'empty'     : False
                            },

                            'port': {
                                'type'      : 'integer',
                                'default'   : 80,
                                'empty'     : False
                            },

                            'protocol': {
                                'type'      : 'string',
                                'default'   : 'HTTP',
                                'empty'     : False
                            },

                            'healthyThreshold': {
                                'type'      : 'integer',
                                'default'   : 5,
                                'empty'     : False
                            },

                            'unhealthyThreshold': {
                                'type'      : 'integer',
                                'default'   : 2,
                                'empty'     : False
                            }
                        }
                    }
                }
            },

            'deployment': {
                
                'type': 'dict',
                'default': {
                    'desiredTasks'  : 2,
                    'maximumPercent': 100,
                    'minimumPercent': 50,
                    'launchType'    : 'EC2'
                },
                'schema': {

                    'desiredTasks': {
                        
                        'type'      : 'integer',
                        'default'   : 2
                    },

                    'maximumPercent': {
                        
                        'type': 'integer',
                        'default': 100
                    },

                    'minimumPercent': {
                        
                        'type': 'integer',
                        'default': 50
                    },

                    'launchType': {

                        'type'      : 'string',
                        'default'   : 'EC2',
                        'empty'     : False
                    }
                }
            },

            'containers': {

                'type'      : 'list',
                'required'  : True,
                'minlength' : 1,
                'schema'    : {

                    'type'          : 'dict',
                    'allow_unknown' : True,
                    'schema': {

                        'name': {

                            'type'      : 'string',
                            'required'  : True,
                            'empty'     : False
                        },

                        'image': {
                            
                            'type'      : 'string',
                            'required'  : True,
                            'empty'     : False
                        },

                        'memory': {
                            
                            'type'      : 'integer',
                            'empty'     : False,
                            'default'   : 128
                        },

                        'memoryReservation': {

                            'type'      : 'integer',
                            'empty'     : False,
                            'default'   : 64
                        },

                        'portMappings': {

                            'type'      : 'list',
                            'minlength' : 1,
                            
                            'default'   : [
                                {
                                    'hostPort'      : 0,
                                    'containerPort' : 80
                                }
                            ], 

                            'schema': {

                                'type' : 'dict',
                                'schema': {

                                    'hostPort': {

                                        'type'      : 'integer',
                                        'required'  : True,
                                        'empty'     : False,
                                        'default'   : 0
                                    },

                                    'containerPort': {

                                        'type'      : 'integer',
                                        'required'  : True,
                                        'empty'     : False,
                                        'default'   : 80
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        logger.info('Starting deployment process...')
        
        v = Validator(config_schema)
        config = v.normalized(user_config)
        
        if v.validate(config, update=True):
            logger.debug(json.dumps(config, indent=4, default=str))

        else:
            logger.error('Invalid configuration parameters: {}', v.errors)
            sys.exit(1)

        elbv2 = self.__session.client('elbv2')

        # AWS Task Definition Parameters
        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html
        task_definition = {
            'family'                : config['name'],
            'volumes'               : config['volumes'],
            'containerDefinitions'  : config['containers']
        }

        logger.info('Creating Task Definition...')

        # Register Task Definition
        try:
            res = self.__client.register_task_definition(**task_definition)
            task_definition_arn = res['taskDefinition']['taskDefinitionArn']
            logger.debug(json.dumps(res, indent=4, default=str))
            
            logger.opt(colors=True).info('<green><b>New Task Definition successfully created!</b></green>')
            logger.opt(colors=True).info('Task Definition ARN: <blue><b>{}</b></blue>', task_definition_arn)

        except:
            logger.exception('What is going on?')
            sys.exit(1)

        # Getting load balancer information
        logger.opt(colors=True).info('Let me find information about your <b>"{}"</b> AWS/ALB...', config['loadBalancer']['name'])
        
        try:
            res = elbv2.describe_load_balancers(Names=[config['loadBalancer']['name']])
            
            VPC_ID = res['LoadBalancers'][0]['VpcId']
            ALB_ARN = res['LoadBalancers'][0]['LoadBalancerArn']

        except ClientError as e:
            if e.response['Error']['Code'] == 'LoadBalancerNotFound':
                logger.opt(colors=True).error('<b>It\'s not a valid AWS/ALB name. Please, provide a valid one!</b>')
                sys.exit(1)
            else:
                logger.exception('What is going on?')
                sys.exit(1)

        except:
            
            logger.exception('What is going on?')
            sys.exit(1)

        # Getting ALB listener information
        try:
            res = elbv2.describe_listeners(LoadBalancerArn=ALB_ARN)
            logger.debug(json.dumps(res, indent=4, default=str))

            valid_listeners = list(filter(lambda x: x['Port'] == config['loadBalancer']['listenerPort'], res['Listeners']))
            if not len(valid_listeners):
                logger.error('The provided listener port is not associated with a valid ALB listener. Please, check your configuration!')
                sys.exit(1)

            ALB_LISTENER_ARN = valid_listeners[0]['ListenerArn']

            logger.opt(colors=True).info('<b>VPC_ID:</b> <cyan><b>{}</b></cyan>', VPC_ID)
            logger.opt(colors=True).info('<b>ALB_ARN:</b> <magenta><b>{}</b></magenta>', ALB_ARN)
            logger.opt(colors=True).info('<b>ALB_LISTENER_ARN:</b> <magenta><b>{}</b></magenta>', ALB_LISTENER_ARN)

        except ClientError as e:
            logger.error('The provided listener port is not associated with a valid ALB listener. Please, check your configuration!')
            logger.debug(json.dumps(e.response, indent=4, default=str))
            sys.exit(1)

        except:
            logger.exception('What is going on?')
            sys.exit(1)


        # Creating target group
        logger.opt(colors=True).info('Trying to create <b>"{}"</b> Target Group...', config['name'])
        try:
            res = elbv2.describe_target_groups(Names=[config['name']])
            logger.opt(colors=True).info('<yellow><b>This Target Group already exists.</b></yellow> I\'m gonna use it!')
            
            TARGET_GROUP_ARN=res['TargetGroups'][0]['TargetGroupArn']

        except ClientError as e:
            health_check = config['loadBalancer']['healthCheck']
            if e.response['Error']['Code'] == 'TargetGroupNotFound':
                
                res = elbv2.create_target_group(
                    Name=config['name'],
                    Protocol=health_check['protocol'],
                    Port=health_check['port'],
                    VpcId=VPC_ID,
                    HealthCheckProtocol=health_check['checkProtocol'],
                    HealthCheckPort=health_check['checkPort'],
                    HealthCheckEnabled=True,
                    HealthCheckPath=health_check['checkPath'],
                    HealthCheckIntervalSeconds=health_check['intervalSeconds'],
                    HealthCheckTimeoutSeconds=health_check['checkTimeoutSeconds'],
                    HealthyThresholdCount=health_check['healthyThreshold'],
                    UnhealthyThresholdCount=health_check['unhealthyThreshold']
                )

                logger.debug(json.dumps(res, indent=4, default=str))
                logger.opt(colors=True).info('<green><b>Target group successfully created!</b></green>')
                
                TARGET_GROUP_ARN=res['TargetGroups'][0]['TargetGroupArn']
            else:
                logger.exception('What is going on?')
                sys.exit(1)

        except:
            logger.exception('What is going on?')
            sys.exit(1)

        # Gettings ALB listener rules information
        logger.info('Checking AWS/ALB listener rules configuration...')
        try:
            res = elbv2.describe_rules(ListenerArn=ALB_LISTENER_ARN, PageSize=101)
            # logger.debug(json.dumps(res, indent=4, default=str))

            PRIORITIES = set([int(x['Priority']) for x in res['Rules'] if x['Priority'] != 'default'])

            for n, x in enumerate(PRIORITIES, 1):
                if n not in PRIORITIES:
                    RULE_PRIORITY = n
                    logger.debug('RULE_PRIORITY: {}', RULE_PRIORITY)
                    break
            
            conditions = []
            field_map = {

                'httpHeader'        : 'http-header',
                'httpRequestMethod' : 'http-request-method',
                'hostHeader'        : 'host-header',
                'pathPattern'       : 'path-pattern',
                'sourceIps'         : 'source-ip'
            }

            for k, v in config['loadBalancer']['conditions'].items():

                if len(v) > 0:
                    condition = {
                        'Field': field_map[k]
                    }

                    if k == 'hostHeader':
                        condition.update({
                            'HostHeaderConfig': {
                                'Values': v
                            } 
                        })
                    elif k == 'pathPattern':
                        condition.update({
                            'PathPatternConfig': {
                                'Values': v
                            }
                        })
                    elif k == 'httpRequestMethod':
                        condition.update({
                            'HttpRequestMethodConfig': {
                                'Values': v
                            }
                        })
                    elif k == 'sourceIps':
                        condition.update({
                            'SourceIpConfig': {
                                'Values': v
                            }
                        })
                    elif k == 'httpHeader':
                        condition.update({
                            'HttpHeaderConfig': v
                        })

                    conditions.append(condition)

            possible_listener_info = self.__get_possible_alb_listener_rule_info(conditions, TARGET_GROUP_ARN, res['Rules'])
            logger.debug(possible_listener_info)
            
            if not possible_listener_info['exists']:
                
                logger.info('There\'s no AWS/ALB Listener Rule created for this service. I will create one...')
                res = elbv2.create_rule(
                    ListenerArn=ALB_LISTENER_ARN,
                    Conditions=conditions,
                    Priority=RULE_PRIORITY,
                    Actions=[{ 'Type': 'forward', 'TargetGroupArn': TARGET_GROUP_ARN }]
                )
                logger.debug(json.dumps(res, indent=4, default=str))
                logger.opt(colors=True).info('<green><b>AWS/ALB listener rule successfully created!</b></green>')
                logger.opt(colors=True).info('AWS/ALB Listener Rule ARN: <magenta><b>{}</b></magenta>', res['Rules'][0]['RuleArn'])
            else:
                if possible_listener_info['needs_update']:
                    logger.opt(colors=True).info('<yellow><b>Your AWS/ALB Listener Rule needs to be updated...</b></yellow>')
                    res = elbv2.modify_rule(
                        RuleArn=possible_listener_info['rule_arn'],
                        Conditions=conditions,
                        Actions=[{ 'Type': 'forward', 'TargetGroupArn': TARGET_GROUP_ARN }]
                    )
                    logger.opt(colors=True).info('<green><b>Everything works fine!</b></green> Now, your AWS/ALB Listener Rule configuration is updated.')
                else:
                    logger.opt(colors=True).info('<yellow><b>Nothing to update here!</b></yellow> Keeping going...')
        except:
            logger.exception('What is going on?')
            sys.exit(1)


        # Creating services
        logger.opt(colors=True).info('Trying to create <b>"{}"</b> service...', config['name'])
        try:

            res = self.__client.describe_services(
                services=[config['name']],
                cluster=config['clusterName']
            )

            container_config = config['containers'][0]

            service_definition = {
            
                'cluster'       : config['clusterName'],
                'serviceName'   : config['name'],
                'taskDefinition': task_definition_arn,
                'desiredCount'  : config['deployment']['desiredTasks'],
                'launchType'    : config['deployment']['launchType'],
                
                'loadBalancers': [
                    {
                        'targetGroupArn'    : TARGET_GROUP_ARN,
                        'containerName'     : container_config['name'],
                        'containerPort'     : container_config['portMappings'][0]['containerPort']
                    }
                ],

                'deploymentConfiguration': {
                    'deploymentCircuitBreaker': {
                        
                        'enable'    : True,
                        'rollback'  : True
                    },

                    'maximumPercent'        : config['deployment']['maximumPercent'],
                    'minimumHealthyPercent' : config['deployment']['minimumPercent']
                },

                'placementStrategy': [
                    {
                        'type'  : 'spread',
                        'field' : 'attribute:ecs.availability-zone'
                    },
                    {
                        'type'  : 'binpack',
                        'field' : 'memory'
                    }
                ]
            }

            services = list(filter(lambda x: x['status'] == 'ACTIVE', res['services']))

            # logger.debug(json.dumps(res, indent=4, default=str))
            if len(services) > 0:
                
                logger.info('This service already exists! I will just update it...')
                service_definition['service'] = config['name']

                del service_definition['launchType']
                del service_definition['loadBalancers']
                del service_definition['serviceName']

                res = self.__client.update_service(**service_definition)
            else:
                
                # 
                res = self.__client.create_service(**service_definition)
                logger.opt(colors=True).info('<green><b>The service was successfully created!</b></green>')

            # logger.debug(json.dumps(res, indent=4, default=str))
        
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
        except:
            logger.exception('What is going on?')


    def __get_possible_alb_listener_rule_info(
        self, 
        new_conditions, 
        target_group_arn, 
        available_rules
        ):
        
        data = {
            'exists'        : False,
            'rule_arn'      : None,
            'needs_update'  : True
        }

        for x in available_rules:
            if 'Actions' in x:
                for action in x['Actions']:
                    if action['Type'] == 'forward'\
                        and action['TargetGroupArn'] == target_group_arn:
                        data.update({
                            'exists'    : True,
                            'rule_arn'  : x['RuleArn']
                        })

                        if len(
                            DeepDiff(
                                new_conditions, 
                                x['Conditions'], 
                                ignore_order=True, 
                                exclude_regex_paths=r'root\[\d+\]\[\'Values\'\]'
                            )
                        ) < 1:
                            data.update({
                                'needs_update': False
                            })
        return data

