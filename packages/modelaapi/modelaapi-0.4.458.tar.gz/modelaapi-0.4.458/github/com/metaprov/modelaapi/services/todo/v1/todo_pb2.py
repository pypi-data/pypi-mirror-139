# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: github.com/metaprov/modelaapi/services/todo/v1/todo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from github.com.metaprov.modelaapi.pkg.apis.team.v1alpha1 import generated_pb2 as github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_team_dot_v1alpha1_dot_generated__pb2
from github.com.metaprov.modelaapi.services.common.v1 import common_pb2 as github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_common_dot_v1_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='github.com/metaprov/modelaapi/services/todo/v1/todo.proto',
  package='github.com.metaprov.modelaapi.services.todo.v1',
  syntax='proto3',
  serialized_options=b'Z.github.com/metaprov/modelaapi/services/todo/v1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n9github.com/metaprov/modelaapi/services/todo/v1/todo.proto\x12.github.com.metaprov.modelaapi.services.todo.v1\x1a google/protobuf/field_mask.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x44github.com/metaprov/modelaapi/pkg/apis/team/v1alpha1/generated.proto\x1a=github.com/metaprov/modelaapi/services/common/v1/common.proto\"\xb2\x01\n\x10ListTodosRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\\\n\x06labels\x18\x02 \x03(\x0b\x32L.github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.LabelsEntry\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"{\n\x11ListTodosResponse\x12M\n\x05todos\x18\x01 \x01(\x0b\x32>.github.com.metaprov.modelaapi.pkg.apis.team.v1alpha1.TodoList\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"o\n\x11\x43reateTodoRequest\x12H\n\x04todo\x18\x01 \x01(\x0b\x32:.github.com.metaprov.modelaapi.pkg.apis.team.v1alpha1.Todo\x12\x10\n\x08password\x18\x02 \x01(\t\"\x14\n\x12\x43reateTodoResponse\"\x8d\x01\n\x11UpdateTodoRequest\x12H\n\x04todo\x18\x01 \x01(\x0b\x32:.github.com.metaprov.modelaapi.pkg.apis.team.v1alpha1.Todo\x12.\n\nfield_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"\x14\n\x12UpdateTodoResponse\"1\n\x0eGetTodoRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"i\n\x0fGetTodoResponse\x12H\n\x04todo\x18\x01 \x01(\x0b\x32:.github.com.metaprov.modelaapi.pkg.apis.team.v1alpha1.Todo\x12\x0c\n\x04yaml\x18\x02 \x01(\t\"4\n\x11\x44\x65leteTodoRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x14\n\x12\x44\x65leteTodoResponse2\xb5\x07\n\x0bTodoService\x12\xaf\x01\n\tListTodos\x12@.github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest\x1a\x41.github.com.metaprov.modelaapi.services.todo.v1.ListTodosResponse\"\x1d\x82\xd3\xe4\x93\x02\x17\x12\x15/v1/todos/{namespace}\x12\xa9\x01\n\nCreateTodo\x12\x41.github.com.metaprov.modelaapi.services.todo.v1.CreateTodoRequest\x1a\x42.github.com.metaprov.modelaapi.services.todo.v1.CreateTodoResponse\"\x14\x82\xd3\xe4\x93\x02\x0e\"\t/v1/todos:\x01*\x12\xb0\x01\n\x07GetTodo\x12>.github.com.metaprov.modelaapi.services.todo.v1.GetTodoRequest\x1a?.github.com.metaprov.modelaapi.services.todo.v1.GetTodoResponse\"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v1/todos/{namespace}/{name}\x12\xd8\x01\n\nUpdateTodo\x12\x41.github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoRequest\x1a\x42.github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoResponse\"C\x82\xd3\xe4\x93\x02=\x1a\x38/v1/todos/{todo.metadata.namespace}/{todo.metadata.name}:\x01*\x12\xb9\x01\n\nDeleteTodo\x12\x41.github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoRequest\x1a\x42.github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoResponse\"$\x82\xd3\xe4\x93\x02\x1e*\x1c/v1/todos/{namespace}/{name}B0Z.github.com/metaprov/modelaapi/services/todo/v1b\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_team_dot_v1alpha1_dot_generated__pb2.DESCRIPTOR,github_dot_com_dot_metaprov_dot_modelaapi_dot_services_dot_common_dot_v1_dot_common__pb2.DESCRIPTOR,])




_LISTTODOSREQUEST_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.LabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=440,
  serialized_end=485,
)

_LISTTODOSREQUEST = _descriptor.Descriptor(
  name='ListTodosRequest',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.labels', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_LISTTODOSREQUEST_LABELSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=307,
  serialized_end=485,
)


_LISTTODOSRESPONSE = _descriptor.Descriptor(
  name='ListTodosResponse',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='todos', full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosResponse.todos', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='github.com.metaprov.modelaapi.services.todo.v1.ListTodosResponse.next_page_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=487,
  serialized_end=610,
)


_CREATETODOREQUEST = _descriptor.Descriptor(
  name='CreateTodoRequest',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.CreateTodoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='todo', full_name='github.com.metaprov.modelaapi.services.todo.v1.CreateTodoRequest.todo', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='github.com.metaprov.modelaapi.services.todo.v1.CreateTodoRequest.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=612,
  serialized_end=723,
)


_CREATETODORESPONSE = _descriptor.Descriptor(
  name='CreateTodoResponse',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.CreateTodoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=725,
  serialized_end=745,
)


_UPDATETODOREQUEST = _descriptor.Descriptor(
  name='UpdateTodoRequest',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='todo', full_name='github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoRequest.todo', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoRequest.field_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=748,
  serialized_end=889,
)


_UPDATETODORESPONSE = _descriptor.Descriptor(
  name='UpdateTodoResponse',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=891,
  serialized_end=911,
)


_GETTODOREQUEST = _descriptor.Descriptor(
  name='GetTodoRequest',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.GetTodoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.todo.v1.GetTodoRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='github.com.metaprov.modelaapi.services.todo.v1.GetTodoRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=913,
  serialized_end=962,
)


_GETTODORESPONSE = _descriptor.Descriptor(
  name='GetTodoResponse',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.GetTodoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='todo', full_name='github.com.metaprov.modelaapi.services.todo.v1.GetTodoResponse.todo', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yaml', full_name='github.com.metaprov.modelaapi.services.todo.v1.GetTodoResponse.yaml', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=964,
  serialized_end=1069,
)


_DELETETODOREQUEST = _descriptor.Descriptor(
  name='DeleteTodoRequest',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1071,
  serialized_end=1123,
)


_DELETETODORESPONSE = _descriptor.Descriptor(
  name='DeleteTodoResponse',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1125,
  serialized_end=1145,
)

_LISTTODOSREQUEST_LABELSENTRY.containing_type = _LISTTODOSREQUEST
_LISTTODOSREQUEST.fields_by_name['labels'].message_type = _LISTTODOSREQUEST_LABELSENTRY
_LISTTODOSRESPONSE.fields_by_name['todos'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_team_dot_v1alpha1_dot_generated__pb2._TODOLIST
_CREATETODOREQUEST.fields_by_name['todo'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_team_dot_v1alpha1_dot_generated__pb2._TODO
_UPDATETODOREQUEST.fields_by_name['todo'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_team_dot_v1alpha1_dot_generated__pb2._TODO
_UPDATETODOREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_GETTODORESPONSE.fields_by_name['todo'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_team_dot_v1alpha1_dot_generated__pb2._TODO
DESCRIPTOR.message_types_by_name['ListTodosRequest'] = _LISTTODOSREQUEST
DESCRIPTOR.message_types_by_name['ListTodosResponse'] = _LISTTODOSRESPONSE
DESCRIPTOR.message_types_by_name['CreateTodoRequest'] = _CREATETODOREQUEST
DESCRIPTOR.message_types_by_name['CreateTodoResponse'] = _CREATETODORESPONSE
DESCRIPTOR.message_types_by_name['UpdateTodoRequest'] = _UPDATETODOREQUEST
DESCRIPTOR.message_types_by_name['UpdateTodoResponse'] = _UPDATETODORESPONSE
DESCRIPTOR.message_types_by_name['GetTodoRequest'] = _GETTODOREQUEST
DESCRIPTOR.message_types_by_name['GetTodoResponse'] = _GETTODORESPONSE
DESCRIPTOR.message_types_by_name['DeleteTodoRequest'] = _DELETETODOREQUEST
DESCRIPTOR.message_types_by_name['DeleteTodoResponse'] = _DELETETODORESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListTodosRequest = _reflection.GeneratedProtocolMessageType('ListTodosRequest', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _LISTTODOSREQUEST_LABELSENTRY,
    '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
    # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest.LabelsEntry)
    })
  ,
  'DESCRIPTOR' : _LISTTODOSREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.ListTodosRequest)
  })
_sym_db.RegisterMessage(ListTodosRequest)
_sym_db.RegisterMessage(ListTodosRequest.LabelsEntry)

ListTodosResponse = _reflection.GeneratedProtocolMessageType('ListTodosResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTTODOSRESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.ListTodosResponse)
  })
_sym_db.RegisterMessage(ListTodosResponse)

CreateTodoRequest = _reflection.GeneratedProtocolMessageType('CreateTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATETODOREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.CreateTodoRequest)
  })
_sym_db.RegisterMessage(CreateTodoRequest)

CreateTodoResponse = _reflection.GeneratedProtocolMessageType('CreateTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATETODORESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.CreateTodoResponse)
  })
_sym_db.RegisterMessage(CreateTodoResponse)

UpdateTodoRequest = _reflection.GeneratedProtocolMessageType('UpdateTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATETODOREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoRequest)
  })
_sym_db.RegisterMessage(UpdateTodoRequest)

UpdateTodoResponse = _reflection.GeneratedProtocolMessageType('UpdateTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATETODORESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.UpdateTodoResponse)
  })
_sym_db.RegisterMessage(UpdateTodoResponse)

GetTodoRequest = _reflection.GeneratedProtocolMessageType('GetTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETTODOREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.GetTodoRequest)
  })
_sym_db.RegisterMessage(GetTodoRequest)

GetTodoResponse = _reflection.GeneratedProtocolMessageType('GetTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTODORESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.GetTodoResponse)
  })
_sym_db.RegisterMessage(GetTodoResponse)

DeleteTodoRequest = _reflection.GeneratedProtocolMessageType('DeleteTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETETODOREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoRequest)
  })
_sym_db.RegisterMessage(DeleteTodoRequest)

DeleteTodoResponse = _reflection.GeneratedProtocolMessageType('DeleteTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETETODORESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.todo.v1.todo_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.todo.v1.DeleteTodoResponse)
  })
_sym_db.RegisterMessage(DeleteTodoResponse)


DESCRIPTOR._options = None
_LISTTODOSREQUEST_LABELSENTRY._options = None

_TODOSERVICE = _descriptor.ServiceDescriptor(
  name='TodoService',
  full_name='github.com.metaprov.modelaapi.services.todo.v1.TodoService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1148,
  serialized_end=2097,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListTodos',
    full_name='github.com.metaprov.modelaapi.services.todo.v1.TodoService.ListTodos',
    index=0,
    containing_service=None,
    input_type=_LISTTODOSREQUEST,
    output_type=_LISTTODOSRESPONSE,
    serialized_options=b'\202\323\344\223\002\027\022\025/v1/todos/{namespace}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateTodo',
    full_name='github.com.metaprov.modelaapi.services.todo.v1.TodoService.CreateTodo',
    index=1,
    containing_service=None,
    input_type=_CREATETODOREQUEST,
    output_type=_CREATETODORESPONSE,
    serialized_options=b'\202\323\344\223\002\016\"\t/v1/todos:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetTodo',
    full_name='github.com.metaprov.modelaapi.services.todo.v1.TodoService.GetTodo',
    index=2,
    containing_service=None,
    input_type=_GETTODOREQUEST,
    output_type=_GETTODORESPONSE,
    serialized_options=b'\202\323\344\223\002\036\022\034/v1/todos/{namespace}/{name}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateTodo',
    full_name='github.com.metaprov.modelaapi.services.todo.v1.TodoService.UpdateTodo',
    index=3,
    containing_service=None,
    input_type=_UPDATETODOREQUEST,
    output_type=_UPDATETODORESPONSE,
    serialized_options=b'\202\323\344\223\002=\0328/v1/todos/{todo.metadata.namespace}/{todo.metadata.name}:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteTodo',
    full_name='github.com.metaprov.modelaapi.services.todo.v1.TodoService.DeleteTodo',
    index=4,
    containing_service=None,
    input_type=_DELETETODOREQUEST,
    output_type=_DELETETODORESPONSE,
    serialized_options=b'\202\323\344\223\002\036*\034/v1/todos/{namespace}/{name}',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TODOSERVICE)

DESCRIPTOR.services_by_name['TodoService'] = _TODOSERVICE

# @@protoc_insertion_point(module_scope)
