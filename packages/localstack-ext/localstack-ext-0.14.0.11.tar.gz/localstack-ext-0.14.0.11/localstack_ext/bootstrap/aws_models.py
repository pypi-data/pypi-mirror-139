from localstack.utils.aws import aws_models
UPHFK=super
UPHFl=None
UPHFf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UPHFK(LambdaLayer,self).__init__(arn)
  self.cwd=UPHFl
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.UPHFf.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(RDSDatabase,self).__init__(UPHFf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(RDSCluster,self).__init__(UPHFf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(AppSyncAPI,self).__init__(UPHFf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(AmplifyApp,self).__init__(UPHFf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(ElastiCacheCluster,self).__init__(UPHFf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(TransferServer,self).__init__(UPHFf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(CloudFrontDistribution,self).__init__(UPHFf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,UPHFf,env=UPHFl):
  UPHFK(CodeCommitRepository,self).__init__(UPHFf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
