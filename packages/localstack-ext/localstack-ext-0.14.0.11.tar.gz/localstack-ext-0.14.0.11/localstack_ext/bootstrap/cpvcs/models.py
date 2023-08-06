from datetime import datetime
kBXHU=str
kBXHK=int
kBXHq=super
kBXHd=False
kBXHP=isinstance
kBXHF=hash
kBXHr=bool
kBXHQ=True
kBXHj=list
kBXHt=map
kBXHb=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:kBXHU):
  self.hash_ref:kBXHU=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={kBXHU(MAIN):API_STATES_DIR,kBXHU(DDB):DYNAMODB_DIR,kBXHU(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:kBXHU,rel_path:kBXHU,file_name:kBXHU,size:kBXHK,service:kBXHU,region:kBXHU,account_id:kBXHU,serialization:Serialization):
  kBXHq(StateFileRef,self).__init__(hash_ref)
  self.rel_path:kBXHU=rel_path
  self.file_name:kBXHU=file_name
  self.size:kBXHK=size
  self.service:kBXHU=service
  self.region:kBXHU=region
  self.account_id:kBXHU=account_id
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,account_id=self.account_id,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return kBXHd
  if not kBXHP(other,StateFileRef):
   return kBXHd
  return(self.hash_ref==other.hash_ref and self.account_id==other.account_id and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return kBXHF((self.hash_ref,self.account_id,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->kBXHr:
  if not other:
   return kBXHd
  if not kBXHP(other,StateFileRef):
   return kBXHd
  return(self.region==other.region and self.account_id==self.account_id and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->kBXHr:
  for other in others:
   if self.congruent(other):
    return kBXHQ
  return kBXHd
 def metadata(self)->kBXHU:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:kBXHU,state_files:Set[StateFileRef],parent_ptr:kBXHU):
  kBXHq(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:kBXHU=parent_ptr
 def state_files_info(self)->kBXHU:
  return "\n".join(kBXHj(kBXHt(lambda state_file:kBXHU(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:kBXHU,head_ptr:kBXHU,message:kBXHU,timestamp:kBXHU=kBXHU(datetime.now().timestamp()),delta_log_ptr:kBXHU=kBXHb):
  self.tail_ptr:kBXHU=tail_ptr
  self.head_ptr:kBXHU=head_ptr
  self.message:kBXHU=message
  self.timestamp:kBXHU=timestamp
  self.delta_log_ptr:kBXHU=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:kBXHU,to_node:kBXHU)->kBXHU:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:kBXHU,state_files:Set[StateFileRef],parent_ptr:kBXHU,creator:kBXHU,rid:kBXHU,revision_number:kBXHK,assoc_commit:Commit=kBXHb):
  kBXHq(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:kBXHU=creator
  self.rid:kBXHU=rid
  self.revision_number:kBXHK=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(kBXHt(lambda state_file:kBXHU(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:kBXHU,state_files:Set[StateFileRef],parent_ptr:kBXHU,creator:kBXHU,comment:kBXHU,active_revision_ptr:kBXHU,outgoing_revision_ptrs:Set[kBXHU],incoming_revision_ptr:kBXHU,version_number:kBXHK):
  kBXHq(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(kBXHt(lambda stat_file:kBXHU(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
