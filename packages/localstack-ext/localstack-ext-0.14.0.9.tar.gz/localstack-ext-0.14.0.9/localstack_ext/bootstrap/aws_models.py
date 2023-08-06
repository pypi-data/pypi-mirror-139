from localstack.utils.aws import aws_models
YFgUr=super
YFgUt=None
YFgUV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YFgUr(LambdaLayer,self).__init__(arn)
  self.cwd=YFgUt
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YFgUV.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(RDSDatabase,self).__init__(YFgUV,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(RDSCluster,self).__init__(YFgUV,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(AppSyncAPI,self).__init__(YFgUV,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(AmplifyApp,self).__init__(YFgUV,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(ElastiCacheCluster,self).__init__(YFgUV,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(TransferServer,self).__init__(YFgUV,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(CloudFrontDistribution,self).__init__(YFgUV,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YFgUV,env=YFgUt):
  YFgUr(CodeCommitRepository,self).__init__(YFgUV,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
