import logging
FvNow=bool
FvNof=hasattr
FvNoO=set
FvNoa=True
FvNon=False
FvNos=isinstance
FvNoE=dict
FvNoW=getattr
FvNoq=None
FvNoR=str
FvNot=Exception
FvNoj=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
KINESIS_DIR="kinesis"
DYNAMODB_DIR="dynamodb"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[FvNow,Set]:
 if FvNof(obj,"__dict__"):
  visited=visited or FvNoO()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return FvNoa,visited
  visited.add(wrapper)
 return FvNon,visited
def get_object_dict(obj):
 if FvNos(obj,FvNoE):
  return obj
 obj_dict=FvNoW(obj,"__dict__",FvNoq)
 return obj_dict
def is_composite_type(obj):
 return FvNos(obj,(FvNoE,OrderedDict))or FvNof(obj,"__dict__")
def api_states_traverse(api_states_path:FvNoR,side_effect:Callable[...,FvNoq],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    sub_dirs=os.path.normpath(dir_name).split(os.sep)
    region=sub_dirs[-1]
    service_name=sub_dirs[-2]
    account_id=sub_dirs[-3]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,account_id=account_id,mutables=mutables)
   except FvNot as e:
    msg=(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    LOG.warning(msg)
    if LOG.isEnabledFor(logging.DEBUG):
     LOG.exception(msg)
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with FvNoj(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except FvNot as e:
   LOG.debug("Unable to read pickled persistence file %s: %s",state_file,e)
def persist_object(obj,state_file):
 with FvNoj(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
