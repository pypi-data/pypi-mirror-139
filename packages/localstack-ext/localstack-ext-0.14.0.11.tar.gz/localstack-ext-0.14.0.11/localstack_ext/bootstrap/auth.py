import getpass
lLYgq=object
lLYgU=staticmethod
lLYgH=False
lLYgn=Exception
lLYgI=None
lLYgj=input
lLYgP=list
import json
import logging
import os
import sys
from localstack.config import dirs
from localstack.constants import API_ENDPOINT
from localstack.utils.common import FileMappedDocument,call_safe,safe_requests,to_str
LOG=logging.getLogger(__name__)
AUTH_CACHE_FILE="auth.json"
class AuthProvider(lLYgq):
 @lLYgU
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @lLYgU
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @lLYgU
 def get(provider,raise_error=lLYgH):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise lLYgn(msg)
   return lLYgI
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @lLYgU
 def name():
  return "internal"
 def get_or_create_token(self,username,password,headers):
  data={"username":username,"password":password}
  response=safe_requests.post("%s/user/signin"%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or "{}"))
   return result["token"]
  except lLYgn:
   pass
 def read_credentials(self,username):
  print("Please provide your login credentials below")
  if not username:
   sys.stdout.write("Username: ")
   sys.stdout.flush()
   username=lLYgj()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise lLYgn("Not implemented")
def get_auth_cache()->FileMappedDocument:
 return FileMappedDocument(os.path.join(dirs.cache,AUTH_CACHE_FILE),mode=0o600)
def login(provider,username=lLYgI):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=lLYgP(AuthProvider.providers().keys())
  raise lLYgn('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print("Verifying credentials ... (this may take a few moments)")
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise lLYgn("Unable to verify login credentials - please try again")
 cache=get_auth_cache()
 cache.update({"provider":provider,"username":username,"token":token})
 call_safe(cache.save,exception_message="error saving authentication information")
def logout():
 cache=get_auth_cache()
 cache.clear()
 cache.save()
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
