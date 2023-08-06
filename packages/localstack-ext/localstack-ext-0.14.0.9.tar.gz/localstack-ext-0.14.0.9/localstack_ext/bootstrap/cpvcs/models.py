from datetime import datetime
kVGxK=str
kVGxA=int
kVGxX=super
kVGxb=False
kVGxu=isinstance
kVGxQ=hash
kVGxY=bool
kVGxt=True
kVGxL=list
kVGxW=map
kVGxS=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:kVGxK):
  self.hash_ref:kVGxK=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={kVGxK(MAIN):API_STATES_DIR,kVGxK(DDB):DYNAMODB_DIR,kVGxK(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:kVGxK,rel_path:kVGxK,file_name:kVGxK,size:kVGxA,service:kVGxK,region:kVGxK,account_id:kVGxK,serialization:Serialization):
  kVGxX(StateFileRef,self).__init__(hash_ref)
  self.rel_path:kVGxK=rel_path
  self.file_name:kVGxK=file_name
  self.size:kVGxA=size
  self.service:kVGxK=service
  self.region:kVGxK=region
  self.account_id:kVGxK=account_id
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,account_id=self.account_id,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return kVGxb
  if not kVGxu(other,StateFileRef):
   return kVGxb
  return(self.hash_ref==other.hash_ref and self.account_id==other.account_id and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return kVGxQ((self.hash_ref,self.account_id,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->kVGxY:
  if not other:
   return kVGxb
  if not kVGxu(other,StateFileRef):
   return kVGxb
  return(self.region==other.region and self.account_id==self.account_id and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->kVGxY:
  for other in others:
   if self.congruent(other):
    return kVGxt
  return kVGxb
 def metadata(self)->kVGxK:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:kVGxK,state_files:Set[StateFileRef],parent_ptr:kVGxK):
  kVGxX(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:kVGxK=parent_ptr
 def state_files_info(self)->kVGxK:
  return "\n".join(kVGxL(kVGxW(lambda state_file:kVGxK(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:kVGxK,head_ptr:kVGxK,message:kVGxK,timestamp:kVGxK=kVGxK(datetime.now().timestamp()),delta_log_ptr:kVGxK=kVGxS):
  self.tail_ptr:kVGxK=tail_ptr
  self.head_ptr:kVGxK=head_ptr
  self.message:kVGxK=message
  self.timestamp:kVGxK=timestamp
  self.delta_log_ptr:kVGxK=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:kVGxK,to_node:kVGxK)->kVGxK:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:kVGxK,state_files:Set[StateFileRef],parent_ptr:kVGxK,creator:kVGxK,rid:kVGxK,revision_number:kVGxA,assoc_commit:Commit=kVGxS):
  kVGxX(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:kVGxK=creator
  self.rid:kVGxK=rid
  self.revision_number:kVGxA=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(kVGxW(lambda state_file:kVGxK(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:kVGxK,state_files:Set[StateFileRef],parent_ptr:kVGxK,creator:kVGxK,comment:kVGxK,active_revision_ptr:kVGxK,outgoing_revision_ptrs:Set[kVGxK],incoming_revision_ptr:kVGxK,version_number:kVGxA):
  kVGxX(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(kVGxW(lambda stat_file:kVGxK(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
