from localstack.utils.aws import aws_models
yYJed=super
yYJeq=None
yYJeg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yYJed(LambdaLayer,self).__init__(arn)
  self.cwd=yYJeq
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.yYJeg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(RDSDatabase,self).__init__(yYJeg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(RDSCluster,self).__init__(yYJeg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(AppSyncAPI,self).__init__(yYJeg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(AmplifyApp,self).__init__(yYJeg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(ElastiCacheCluster,self).__init__(yYJeg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(TransferServer,self).__init__(yYJeg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(CloudFrontDistribution,self).__init__(yYJeg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,yYJeg,env=yYJeq):
  yYJed(CodeCommitRepository,self).__init__(yYJeg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
