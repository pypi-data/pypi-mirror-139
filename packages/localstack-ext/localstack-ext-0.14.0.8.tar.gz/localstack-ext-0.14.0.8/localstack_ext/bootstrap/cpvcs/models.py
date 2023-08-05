from datetime import datetime
nbgBA=str
nbgBa=int
nbgBx=super
nbgBS=False
nbgBd=isinstance
nbgBv=hash
nbgBp=bool
nbgBD=True
nbgBw=list
nbgBW=map
nbgBe=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:nbgBA):
  self.hash_ref:nbgBA=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={nbgBA(MAIN):API_STATES_DIR,nbgBA(DDB):DYNAMODB_DIR,nbgBA(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:nbgBA,rel_path:nbgBA,file_name:nbgBA,size:nbgBa,service:nbgBA,region:nbgBA,account_id:nbgBA,serialization:Serialization):
  nbgBx(StateFileRef,self).__init__(hash_ref)
  self.rel_path:nbgBA=rel_path
  self.file_name:nbgBA=file_name
  self.size:nbgBa=size
  self.service:nbgBA=service
  self.region:nbgBA=region
  self.account_id:nbgBA=account_id
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,account_id=self.account_id,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return nbgBS
  if not nbgBd(other,StateFileRef):
   return nbgBS
  return(self.hash_ref==other.hash_ref and self.account_id==other.account_id and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return nbgBv((self.hash_ref,self.account_id,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->nbgBp:
  if not other:
   return nbgBS
  if not nbgBd(other,StateFileRef):
   return nbgBS
  return(self.region==other.region and self.account_id==self.account_id and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->nbgBp:
  for other in others:
   if self.congruent(other):
    return nbgBD
  return nbgBS
 def metadata(self)->nbgBA:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:nbgBA,state_files:Set[StateFileRef],parent_ptr:nbgBA):
  nbgBx(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:nbgBA=parent_ptr
 def state_files_info(self)->nbgBA:
  return "\n".join(nbgBw(nbgBW(lambda state_file:nbgBA(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:nbgBA,head_ptr:nbgBA,message:nbgBA,timestamp:nbgBA=nbgBA(datetime.now().timestamp()),delta_log_ptr:nbgBA=nbgBe):
  self.tail_ptr:nbgBA=tail_ptr
  self.head_ptr:nbgBA=head_ptr
  self.message:nbgBA=message
  self.timestamp:nbgBA=timestamp
  self.delta_log_ptr:nbgBA=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:nbgBA,to_node:nbgBA)->nbgBA:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:nbgBA,state_files:Set[StateFileRef],parent_ptr:nbgBA,creator:nbgBA,rid:nbgBA,revision_number:nbgBa,assoc_commit:Commit=nbgBe):
  nbgBx(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:nbgBA=creator
  self.rid:nbgBA=rid
  self.revision_number:nbgBa=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(nbgBW(lambda state_file:nbgBA(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:nbgBA,state_files:Set[StateFileRef],parent_ptr:nbgBA,creator:nbgBA,comment:nbgBA,active_revision_ptr:nbgBA,outgoing_revision_ptrs:Set[nbgBA],incoming_revision_ptr:nbgBA,version_number:nbgBa):
  nbgBx(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(nbgBW(lambda stat_file:nbgBA(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
