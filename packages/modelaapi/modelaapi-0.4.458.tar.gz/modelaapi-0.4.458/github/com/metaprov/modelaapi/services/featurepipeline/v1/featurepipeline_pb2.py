# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: github.com/metaprov/modelaapi/services/featurepipeline/v1/featurepipeline.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1 import generated_pb2 as github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_data_dot_v1alpha1_dot_generated__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='github.com/metaprov/modelaapi/services/featurepipeline/v1/featurepipeline.proto',
  package='github.com.metaprov.modelaapi.services.featurepipeline.v1',
  syntax='proto3',
  serialized_options=b'Z9github.com/metaprov/modelaapi/services/featurepipeline/v1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nOgithub.com/metaprov/modelaapi/services/featurepipeline/v1/featurepipeline.proto\x12\x39github.com.metaprov.modelaapi.services.featurepipeline.v1\x1a google/protobuf/field_mask.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x44github.com/metaprov/modelaapi/pkg/apis/data/v1alpha1/generated.proto\"\x8a\x02\n\x1aListFeaturePipelineRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12q\n\x06labels\x18\x02 \x03(\x0b\x32\x61.github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.LabelsEntry\x12\x11\n\tpage_size\x18\x03 \x01(\x05\x12\x12\n\npage_token\x18\x04 \x01(\t\x12\x10\n\x08order_by\x18\x05 \x01(\t\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x9b\x01\n\x1bListFeaturePipelineResponse\x12\x63\n\x10\x66\x65\x61turepipelines\x18\x01 \x01(\x0b\x32I.github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.FeaturePipelineList\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"~\n\x1c\x43reateFeaturePipelineRequest\x12^\n\x0f\x66\x65\x61turepipeline\x18\x01 \x01(\x0b\x32\x45.github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.FeaturePipeline\"\x1f\n\x1d\x43reateFeaturePipelineResponse\"\xae\x01\n\x1cUpdateFeaturePipelineRequest\x12^\n\x0f\x66\x65\x61turepipeline\x18\x01 \x01(\x0b\x32\x45.github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.FeaturePipeline\x12.\n\nfield_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"\x1f\n\x1dUpdateFeaturePipelineResponse\"<\n\x19GetFeaturePipelineRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x8a\x01\n\x1aGetFeaturePipelineResponse\x12^\n\x0f\x66\x65\x61turepipeline\x18\x01 \x01(\x0b\x32\x45.github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.FeaturePipeline\x12\x0c\n\x04yaml\x18\x02 \x01(\t\"?\n\x1c\x44\x65leteFeaturePipelineRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x1f\n\x1d\x44\x65leteFeaturePipelineResponse\"\x1e\n\x1cPauseFeaturePipelineResponse\">\n\x1bPauseFeaturePipelineRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x1f\n\x1dResumeFeaturePipelineResponse\"?\n\x1cResumeFeaturePipelineRequest\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t2\xa3\x0e\n\x16\x46\x65\x61turePipelineService\x12\xef\x01\n\x14ListFeaturePipelines\x12U.github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest\x1aV.github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineResponse\"(\x82\xd3\xe4\x93\x02\"\x12 /v1/featurepipelines/{namespace}\x12\xeb\x01\n\x15\x43reateFeaturePipeline\x12W.github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineRequest\x1aX.github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineResponse\"\x1f\x82\xd3\xe4\x93\x02\x19\"\x14/v1/featurepipelines:\x01*\x12\xf2\x01\n\x12GetFeaturePipeline\x12T.github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineRequest\x1aU.github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineResponse\"/\x82\xd3\xe4\x93\x02)\x12\'/v1/featurepipelines/{namespace}/{name}\x12\xb0\x02\n\x15UpdateFeaturePipeline\x12W.github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineRequest\x1aX.github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineResponse\"d\x82\xd3\xe4\x93\x02^\x1aY/v1/featurepipelines/{featurepipeline.metadata.namespace}/{featurepipeline.metadata.name}:\x01*\x12\xfb\x01\n\x15\x44\x65leteFeaturePipeline\x12W.github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineRequest\x1aX.github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineResponse\"/\x82\xd3\xe4\x93\x02)*\'/v1/featurepipelines/{namespace}/{name}\x12\xfe\x01\n\x14PauseFeaturePipeline\x12V.github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineRequest\x1aW.github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineResponse\"5\x82\xd3\xe4\x93\x02/\"-/v1/featurepipelines/{namespace}/{name}:pause\x12\x81\x02\n\x15ResumeFeaturePipeline\x12W.github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineRequest\x1aX.github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineResponse\"5\x82\xd3\xe4\x93\x02/\"-/v1/featurepipelines/{namespace}/{name}:pauseB;Z9github.com/metaprov/modelaapi/services/featurepipeline/v1b\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_data_dot_v1alpha1_dot_generated__pb2.DESCRIPTOR,])




_LISTFEATUREPIPELINEREQUEST_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.LabelsEntry.value', index=1,
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
  serialized_start=498,
  serialized_end=543,
)

_LISTFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='ListFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.labels', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.page_size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.page_token', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order_by', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.order_by', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_LISTFEATUREPIPELINEREQUEST_LABELSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=277,
  serialized_end=543,
)


_LISTFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='ListFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='featurepipelines', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineResponse.featurepipelines', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineResponse.next_page_token', index=1,
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
  serialized_start=546,
  serialized_end=701,
)


_CREATEFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='CreateFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='featurepipeline', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineRequest.featurepipeline', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=703,
  serialized_end=829,
)


_CREATEFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='CreateFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineResponse',
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
  serialized_start=831,
  serialized_end=862,
)


_UPDATEFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='UpdateFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='featurepipeline', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineRequest.featurepipeline', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineRequest.field_mask', index=1,
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
  serialized_start=865,
  serialized_end=1039,
)


_UPDATEFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='UpdateFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineResponse',
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
  serialized_start=1041,
  serialized_end=1072,
)


_GETFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='GetFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineRequest.name', index=1,
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
  serialized_start=1074,
  serialized_end=1134,
)


_GETFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='GetFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='featurepipeline', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineResponse.featurepipeline', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yaml', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineResponse.yaml', index=1,
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
  serialized_start=1137,
  serialized_end=1275,
)


_DELETEFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='DeleteFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineRequest.name', index=1,
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
  serialized_start=1277,
  serialized_end=1340,
)


_DELETEFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='DeleteFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineResponse',
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
  serialized_start=1342,
  serialized_end=1373,
)


_PAUSEFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='PauseFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineResponse',
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
  serialized_start=1375,
  serialized_end=1405,
)


_PAUSEFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='PauseFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineRequest.name', index=1,
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
  serialized_start=1407,
  serialized_end=1469,
)


_RESUMEFEATUREPIPELINERESPONSE = _descriptor.Descriptor(
  name='ResumeFeaturePipelineResponse',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineResponse',
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
  serialized_start=1471,
  serialized_end=1502,
)


_RESUMEFEATUREPIPELINEREQUEST = _descriptor.Descriptor(
  name='ResumeFeaturePipelineRequest',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineRequest.name', index=1,
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
  serialized_start=1504,
  serialized_end=1567,
)

_LISTFEATUREPIPELINEREQUEST_LABELSENTRY.containing_type = _LISTFEATUREPIPELINEREQUEST
_LISTFEATUREPIPELINEREQUEST.fields_by_name['labels'].message_type = _LISTFEATUREPIPELINEREQUEST_LABELSENTRY
_LISTFEATUREPIPELINERESPONSE.fields_by_name['featurepipelines'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_data_dot_v1alpha1_dot_generated__pb2._FEATUREPIPELINELIST
_CREATEFEATUREPIPELINEREQUEST.fields_by_name['featurepipeline'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_data_dot_v1alpha1_dot_generated__pb2._FEATUREPIPELINE
_UPDATEFEATUREPIPELINEREQUEST.fields_by_name['featurepipeline'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_data_dot_v1alpha1_dot_generated__pb2._FEATUREPIPELINE
_UPDATEFEATUREPIPELINEREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_GETFEATUREPIPELINERESPONSE.fields_by_name['featurepipeline'].message_type = github_dot_com_dot_metaprov_dot_modelaapi_dot_pkg_dot_apis_dot_data_dot_v1alpha1_dot_generated__pb2._FEATUREPIPELINE
DESCRIPTOR.message_types_by_name['ListFeaturePipelineRequest'] = _LISTFEATUREPIPELINEREQUEST
DESCRIPTOR.message_types_by_name['ListFeaturePipelineResponse'] = _LISTFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['CreateFeaturePipelineRequest'] = _CREATEFEATUREPIPELINEREQUEST
DESCRIPTOR.message_types_by_name['CreateFeaturePipelineResponse'] = _CREATEFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['UpdateFeaturePipelineRequest'] = _UPDATEFEATUREPIPELINEREQUEST
DESCRIPTOR.message_types_by_name['UpdateFeaturePipelineResponse'] = _UPDATEFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['GetFeaturePipelineRequest'] = _GETFEATUREPIPELINEREQUEST
DESCRIPTOR.message_types_by_name['GetFeaturePipelineResponse'] = _GETFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['DeleteFeaturePipelineRequest'] = _DELETEFEATUREPIPELINEREQUEST
DESCRIPTOR.message_types_by_name['DeleteFeaturePipelineResponse'] = _DELETEFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['PauseFeaturePipelineResponse'] = _PAUSEFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['PauseFeaturePipelineRequest'] = _PAUSEFEATUREPIPELINEREQUEST
DESCRIPTOR.message_types_by_name['ResumeFeaturePipelineResponse'] = _RESUMEFEATUREPIPELINERESPONSE
DESCRIPTOR.message_types_by_name['ResumeFeaturePipelineRequest'] = _RESUMEFEATUREPIPELINEREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('ListFeaturePipelineRequest', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _LISTFEATUREPIPELINEREQUEST_LABELSENTRY,
    '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
    # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest.LabelsEntry)
    })
  ,
  'DESCRIPTOR' : _LISTFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(ListFeaturePipelineRequest)
_sym_db.RegisterMessage(ListFeaturePipelineRequest.LabelsEntry)

ListFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('ListFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.ListFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(ListFeaturePipelineResponse)

CreateFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('CreateFeaturePipelineRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(CreateFeaturePipelineRequest)

CreateFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('CreateFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.CreateFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(CreateFeaturePipelineResponse)

UpdateFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('UpdateFeaturePipelineRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(UpdateFeaturePipelineRequest)

UpdateFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('UpdateFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.UpdateFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(UpdateFeaturePipelineResponse)

GetFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('GetFeaturePipelineRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(GetFeaturePipelineRequest)

GetFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('GetFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.GetFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(GetFeaturePipelineResponse)

DeleteFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('DeleteFeaturePipelineRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(DeleteFeaturePipelineRequest)

DeleteFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('DeleteFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.DeleteFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(DeleteFeaturePipelineResponse)

PauseFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('PauseFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _PAUSEFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(PauseFeaturePipelineResponse)

PauseFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('PauseFeaturePipelineRequest', (_message.Message,), {
  'DESCRIPTOR' : _PAUSEFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.PauseFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(PauseFeaturePipelineRequest)

ResumeFeaturePipelineResponse = _reflection.GeneratedProtocolMessageType('ResumeFeaturePipelineResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESUMEFEATUREPIPELINERESPONSE,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineResponse)
  })
_sym_db.RegisterMessage(ResumeFeaturePipelineResponse)

ResumeFeaturePipelineRequest = _reflection.GeneratedProtocolMessageType('ResumeFeaturePipelineRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESUMEFEATUREPIPELINEREQUEST,
  '__module__' : 'github.com.metaprov.modelaapi.services.featurepipeline.v1.featurepipeline_pb2'
  # @@protoc_insertion_point(class_scope:github.com.metaprov.modelaapi.services.featurepipeline.v1.ResumeFeaturePipelineRequest)
  })
_sym_db.RegisterMessage(ResumeFeaturePipelineRequest)


DESCRIPTOR._options = None
_LISTFEATUREPIPELINEREQUEST_LABELSENTRY._options = None

_FEATUREPIPELINESERVICE = _descriptor.ServiceDescriptor(
  name='FeaturePipelineService',
  full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1570,
  serialized_end=3397,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListFeaturePipelines',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.ListFeaturePipelines',
    index=0,
    containing_service=None,
    input_type=_LISTFEATUREPIPELINEREQUEST,
    output_type=_LISTFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002\"\022 /v1/featurepipelines/{namespace}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateFeaturePipeline',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.CreateFeaturePipeline',
    index=1,
    containing_service=None,
    input_type=_CREATEFEATUREPIPELINEREQUEST,
    output_type=_CREATEFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002\031\"\024/v1/featurepipelines:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetFeaturePipeline',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.GetFeaturePipeline',
    index=2,
    containing_service=None,
    input_type=_GETFEATUREPIPELINEREQUEST,
    output_type=_GETFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002)\022\'/v1/featurepipelines/{namespace}/{name}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateFeaturePipeline',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.UpdateFeaturePipeline',
    index=3,
    containing_service=None,
    input_type=_UPDATEFEATUREPIPELINEREQUEST,
    output_type=_UPDATEFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002^\032Y/v1/featurepipelines/{featurepipeline.metadata.namespace}/{featurepipeline.metadata.name}:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteFeaturePipeline',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.DeleteFeaturePipeline',
    index=4,
    containing_service=None,
    input_type=_DELETEFEATUREPIPELINEREQUEST,
    output_type=_DELETEFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002)*\'/v1/featurepipelines/{namespace}/{name}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PauseFeaturePipeline',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.PauseFeaturePipeline',
    index=5,
    containing_service=None,
    input_type=_PAUSEFEATUREPIPELINEREQUEST,
    output_type=_PAUSEFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002/\"-/v1/featurepipelines/{namespace}/{name}:pause',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ResumeFeaturePipeline',
    full_name='github.com.metaprov.modelaapi.services.featurepipeline.v1.FeaturePipelineService.ResumeFeaturePipeline',
    index=6,
    containing_service=None,
    input_type=_RESUMEFEATUREPIPELINEREQUEST,
    output_type=_RESUMEFEATUREPIPELINERESPONSE,
    serialized_options=b'\202\323\344\223\002/\"-/v1/featurepipelines/{namespace}/{name}:pause',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FEATUREPIPELINESERVICE)

DESCRIPTOR.services_by_name['FeaturePipelineService'] = _FEATUREPIPELINESERVICE

# @@protoc_insertion_point(module_scope)
