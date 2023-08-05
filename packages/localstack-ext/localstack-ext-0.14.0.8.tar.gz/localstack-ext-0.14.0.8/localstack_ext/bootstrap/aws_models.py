from localstack.utils.aws import aws_models
MOxsk=super
MOxsY=None
MOxst=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  MOxsk(LambdaLayer,self).__init__(arn)
  self.cwd=MOxsY
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.MOxst.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(RDSDatabase,self).__init__(MOxst,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(RDSCluster,self).__init__(MOxst,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(AppSyncAPI,self).__init__(MOxst,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(AmplifyApp,self).__init__(MOxst,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(ElastiCacheCluster,self).__init__(MOxst,env=env)
class TransferServer(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(TransferServer,self).__init__(MOxst,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(CloudFrontDistribution,self).__init__(MOxst,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,MOxst,env=MOxsY):
  MOxsk(CodeCommitRepository,self).__init__(MOxst,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
