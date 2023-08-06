from datetime import datetime
VfaRv=str
VfaRG=int
VfaRq=super
VfaRH=False
VfaRz=isinstance
VfaRj=hash
VfaRK=bool
VfaRW=True
VfaRk=list
VfaRd=map
VfaRS=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:VfaRv):
  self.hash_ref:VfaRv=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={VfaRv(MAIN):API_STATES_DIR,VfaRv(DDB):DYNAMODB_DIR,VfaRv(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:VfaRv,rel_path:VfaRv,file_name:VfaRv,size:VfaRG,service:VfaRv,region:VfaRv,account_id:VfaRv,serialization:Serialization):
  VfaRq(StateFileRef,self).__init__(hash_ref)
  self.rel_path:VfaRv=rel_path
  self.file_name:VfaRv=file_name
  self.size:VfaRG=size
  self.service:VfaRv=service
  self.region:VfaRv=region
  self.account_id:VfaRv=account_id
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,account_id=self.account_id,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return VfaRH
  if not VfaRz(other,StateFileRef):
   return VfaRH
  return(self.hash_ref==other.hash_ref and self.account_id==other.account_id and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return VfaRj((self.hash_ref,self.account_id,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->VfaRK:
  if not other:
   return VfaRH
  if not VfaRz(other,StateFileRef):
   return VfaRH
  return(self.region==other.region and self.account_id==self.account_id and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->VfaRK:
  for other in others:
   if self.congruent(other):
    return VfaRW
  return VfaRH
 def metadata(self)->VfaRv:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:VfaRv,state_files:Set[StateFileRef],parent_ptr:VfaRv):
  VfaRq(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:VfaRv=parent_ptr
 def state_files_info(self)->VfaRv:
  return "\n".join(VfaRk(VfaRd(lambda state_file:VfaRv(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:VfaRv,head_ptr:VfaRv,message:VfaRv,timestamp:VfaRv=VfaRv(datetime.now().timestamp()),delta_log_ptr:VfaRv=VfaRS):
  self.tail_ptr:VfaRv=tail_ptr
  self.head_ptr:VfaRv=head_ptr
  self.message:VfaRv=message
  self.timestamp:VfaRv=timestamp
  self.delta_log_ptr:VfaRv=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:VfaRv,to_node:VfaRv)->VfaRv:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:VfaRv,state_files:Set[StateFileRef],parent_ptr:VfaRv,creator:VfaRv,rid:VfaRv,revision_number:VfaRG,assoc_commit:Commit=VfaRS):
  VfaRq(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:VfaRv=creator
  self.rid:VfaRv=rid
  self.revision_number:VfaRG=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(VfaRd(lambda state_file:VfaRv(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:VfaRv,state_files:Set[StateFileRef],parent_ptr:VfaRv,creator:VfaRv,comment:VfaRv,active_revision_ptr:VfaRv,outgoing_revision_ptrs:Set[VfaRv],incoming_revision_ptr:VfaRv,version_number:VfaRG):
  VfaRq(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(VfaRd(lambda stat_file:VfaRv(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
