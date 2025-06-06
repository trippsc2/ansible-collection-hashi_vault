#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
module: vault_pki_generate_intermediate_csr
version_added: 1.5.0
author:
  - Jim Tarpley (@trippsc2)
short_description: Generates an certificate signing request (CSR) for a PKI secret engine
description:
  - >-
    Generates an L(certificate signing request (CSR),https://hvac.readthedocs.io/en/stable/usage/secrets_engines/pki.html#generate-intermediate)
    for a PKI secret engine.
  - This module is not idempotent, as it generates a new CSR (and possibly private key) each time it is run.
  - If the CSR is successfully generated, the CSR is returned.
extends_documentation_fragment:
  - trippsc2.hashi_vault.auth
  - trippsc2.hashi_vault.connection
  - trippsc2.hashi_vault.action_group
  - trippsc2.hashi_vault.check_mode_none
  - trippsc2.hashi_vault.engine_mount
  - trippsc2.hashi_vault.requirements
options:
  type:
    type: str
    required: false
    default: internal
    choices:
      - internal
      - existing
    description:
      - The private key type to use for generating the certificate signing request (CSR).
      - If set to V(internal), the private key will be generated by HashiCorp Vault and stored.
      - If set to V(existing), the O(key_ref) option is required and the private key with that identifier will be used.
      - KMS-backed keys are not supported with this module.
  key_ref:
    type: str
    required: false
    description:
      - The identifier of the existing private key to use for generating the certificate signing request (CSR).
      - Should only be provided if O(type=existing).
      - If a private key with this identifier does not exist, the module will fail.
  common_name:
    type: str
    required: true
    description:
      - The requested common name (CN) attribute for the certificate signing request (CSR).
  alt_names:
    type: list
    required: false
    elements: str
    description:
      - The list of Subject Alternative Names (SANs) to include in the certificate signing request (CSR).
      - Each element should be a hostname (DNS name) or an email address.
      - >-
        If this does not include the common name and O(exclude_cn_from_sans=false), the common name will be
        added to the list of SANs.
      - If not provided, an empty list will be used.
  ip_sans:
    type: list
    required: false
    elements: str
    description:
      - The list of IP Subject Alternative Names (IP SANs) to include in the certificate signing request (CSR).
      - Each element should be a valid IP address.
      - If not provided, an empty list will be used.
  uri_sans:
    type: list
    required: false
    elements: str
    description:
      - The list of URI Subject Alternative Names (URI SANs) to include in the certificate signing request (CSR).
      - Each element should be a valid URI.
      - If not provided, an empty list will be used.
  other_sans:
    type: list
    required: false
    elements: dict
    description:
      - The list of custom OID/UTF8-string SANs.
      - If not provided, an empty list will be used.
    suboptions:
      oid:
        type: str
        required: true
        description:
          - The OID for the custom SAN.
      type:
        type: str
        required: false
        default: utf8
        choices:
          - utf8
        description:
          - The type of the custom SAN.
      value:
        type: str
        required: true
        description:
          - The value of the custom SAN.
  format:
    type: str
    required: false
    choices:
      - pem
      - der
      - pem_bundle
    description:
      - The format of the returned certificate data.
      - If V(pem_bundle), the certificate will contain the private key and certificate concatenated.
      - If not provided, the certificate will be returned in PEM format.
  private_key_format:
    type: str
    required: false
    default: der
    choices:
      - der
      - pkcs8
    description:
      - The format for marshaling the private key.
      - >-
        If set to V(der) and O(format=pem) or O(format=pem_bundle), the private key will be
        returned in PEM-encoded DER format.
      - If set to V(der) and O(format=der), the private key will be returned in base64-encoded DER format.
      - If set to V(pkcs8), the private key will be returned in PEM-encoded PKCS8 format.
  key_type:
    type: str
    required: false
    choices:
      - rsa
      - ed25519
      - ec
    description:
      - The type of private key to generate.
      - Should only be defined if O(type=internal).
      - >-
        If HashiCorp Vault is running in FIPS mode, using the V(ed25519) value will cause the
        module to fail, as it is not a certified algorithm.
      - If not provided, the private key will be generated using the RSA algorithm.
  key_bits:
    type: int
    required: false
    choices:
      - 224
      - 256
      - 384
      - 521
      - 2048
      - 3072
      - 4096
      - 8192
    description:
      - The number of bits to use for generated keys.
      - If O(key_type=rsa), the allowed values are V(2048), V(3072), V(4096), and V(8192).
      - If not provided and O(key_type=rsa), this defaults to V(2048) on new roles.
      - If O(key_type=ec), the allowed values are V(224), V(256), V(384), and V(521).
      - If not provided and O(key_type=ec), this defaults to V(256) on new roles.
      - If O(key_type=ed25519), this should not be provided.
  key_name:
    type: str
    required: false
    description:
      - The name of the private key to store in the storage backend.
      - Should only be defined if O(type=internal).
      - If set to V(default), the private key will be stored as the default key.
      - If not provided, the private key will not be stored as the default key.
  signature_bits:
    type: int
    required: false
    choices:
      - 256
      - 384
      - 512
    description:
      - The signature algorithm bit length for the signed certificates.
      - Should only be provided when O(key_type=rsa).
      - If not provided and O(key_type=rsa), this defaults to V(2048).
  exclude_cn_from_sans:
    type: bool
    required: false
    description:
      - Whether to exclude the common name from the Subject Alternate Names (SANs).
      - If set to V(true), the given O(common_name) will not be added to the list of SANs.
      - >-
        If set to V(false), the given O(common_name) will be added to the list of SANs and parsed
        as a DNS name or email address.
      - If not provided, the common name will not be excluded.
  ou:
    type: list
    required: false
    elements: str
    description:
      - The Organizational Unit (OU) values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  organization:
    type: list
    required: false
    elements: str
    description:
      - The Organization (O) values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  country:
    type: list
    required: false
    elements: str
    description:
      - The Country (C) values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  locality:
    type: list
    required: false
    elements: str
    description:
      - The Locality (L) values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  province:
    type: list
    required: false
    elements: str
    description:
      - The Province or State (ST) values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  street_address:
    type: list
    required: false
    elements: str
    description:
      - The Street Address values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  postal_code:
    type: list
    required: false
    elements: str
    description:
      - The Postal Code values to include in the CA certificate.
      - If not provided, this defaults to an empty list on new roles.
  serial_number:
    type: str
    required: false
    description:
      - The serial number of the CA certificate.
      - If you want more than one, specify alternative names in the alt_names map using OID 2.5.4.5.
      - If not provided, HashiCorp Vault will generate a random serial number for the certificate.
  add_basic_constraints:
    type: bool
    required: false
    description:
      - Whether to include the basic constraints extension in the certificate signing request (CSR).
      - If set to V(true), the CSR will include the basic constraints extension.
      - If not provided, the CSR will not include the basic constraints extension.
      - >-
        This option is only needed for compatibility with certain systems, such as Active Directory
        Certificate Services as the signing CA.
  key_usage:
    type: list
    required: false
    default:
      - CertSign
      - CRLSign
    elements: str
    choices:
      - DigitalSignature
      - ContentCommitment
      - KeyEncipherment
      - DataEncipherment
      - KeyAgreement
      - CertSign
      - CRLSign
      - EncipherOnly
      - DecipherOnly
    description:
      - The list of key usage constraints to include in the certificate signing request (CSR).
      - If not provided, no key usage constraints will be included in the CSR.
"""

EXAMPLES = r"""
- name: Generate an intermediate CA CSR
  trippsc2.hashi_vault.vault_pki_generate_intermediate_csr:
    url: https://vault:8201
    auth_method: userpass
    username: '{{ user }}'
    password: '{{ passwd }}'
    engine_mount_point: pki
    common_name: Intermediate CA
"""

RETURN = r"""
csr:
  type: str
  returned: success
  description:
    - The certificate signing request (CSR) generated by the module.
key_id:
  type: str
  returned: success
  description:
    - The identifier of the private key used to generate the certificate signing request (CSR).
"""

import traceback

from ansible.module_utils.basic import missing_required_lib

from typing import List, Optional

try:
    import hvac
except ImportError:
    HAS_HVAC: bool = False
    HVAC_IMPORT_ERROR: Optional[str] = traceback.format_exc()
else:
    HAS_HVAC: bool = True
    HVAC_IMPORT_ERROR: Optional[str] = None

from ..module_utils._vault_cert import other_sans_to_list_of_str
from ..module_utils._vault_module import VaultModule
from ..module_utils._vault_module_error import VaultModuleError


class VaultPKIGenerateIntermediateCSRModule(VaultModule):
    """
    Vault PKI Generate Intermediate CA CSR Module
    """

    ARGSPEC: dict = dict(
        engine_mount_point=dict(type='str', required=True),
        type=dict(type='str', required=False, default='internal', choices=['internal', 'existing']),
        key_ref=dict(type='str', required=False),
        common_name=dict(type='str', required=True),
        alt_names=dict(type='list', required=False, elements='str'),
        ip_sans=dict(type='list', required=False, elements='str'),
        uri_sans=dict(type='list', required=False, elements='str'),
        other_sans=dict(
            type='list',
            required=False,
            elements='dict',
            options=dict(
                oid=dict(type='str', required=True),
                type=dict(type='str', required=False, default='utf8', choices=['utf8']),
                value=dict(type='str', required=True)
            )
        ),
        format=dict(type='str', required=False, choices=['pem', 'der', 'pem_bundle']),
        private_key_format=dict(
            type='str',
            required=False,
            choices=['der', 'pkcs8'],
            default='der'
        ),
        key_type=dict(type='str', required=False, choices=['rsa', 'ed25519', 'ec']),
        key_bits=dict(
            type='int',
            required=False,
            choices=[
                224,
                256,
                384,
                521,
                2048,
                3072,
                4096,
                8192
            ]
        ),
        key_name=dict(type='str', required=False),
        signature_bits=dict(type='int', required=False, choices=[256, 384, 512]),
        exclude_cn_from_sans=dict(type='bool', required=False),
        ou=dict(type='list', required=False, elements='str'),
        organization=dict(type='list', required=False, elements='str'),
        country=dict(type='list', required=False, elements='str'),
        locality=dict(type='list', required=False, elements='str'),
        province=dict(type='list', required=False, elements='str'),
        street_address=dict(type='list', required=False, elements='str'),
        postal_code=dict(type='list', required=False, elements='str'),
        serial_number=dict(type='str', required=False),
        add_basic_constraints=dict(type='bool', required=False),
        key_usage=dict(
            type='list',
            required=False,
            default=['CertSign', 'CRLSign'],
            elements='str',
            choices=[
                'DigitalSignature',
                'ContentCommitment',
                'KeyEncipherment',
                'DataEncipherment',
                'KeyAgreement',
                'CertSign',
                'CRLSign',
                'EncipherOnly',
                'DecipherOnly'
            ]
        )
    )

    LIST_PARAMS_TO_JOIN: List[str] = ['alt_names']

    def __init__(self, *args, **kwargs) -> None:

        argspec: dict = self.ARGSPEC.copy()

        super(VaultPKIGenerateIntermediateCSRModule, self).__init__(
            *args,
            argument_spec=argspec,
            supports_check_mode=False,
            **kwargs
        )

    def build_request_payload(self) -> dict:
        """
        Build the request payload for the module.

        Returns:
            dict: The request payload.
        """

        engine_mount_point: str = self.params['engine_mount_point']
        type: str = self.params['type']
        common_name: str = self.params['common_name']

        extra_params: dict = {}

        for key, value in self.params.items():
            if key not in self.ARGSPEC:
                continue

            if key in ['engine_mount_point', 'type', 'common_name']:
                continue

            if value is None:
                continue

            if key == 'other_sans':
                extra_params[key] = other_sans_to_list_of_str(value)
                continue

            if key in self.LIST_PARAMS_TO_JOIN:
                extra_params[key] = self.convert_list_to_comma_separated_string(value)
                continue

            extra_params[key] = value

        payload: dict = dict(
            type=type,
            mount_point=engine_mount_point,
            common_name=common_name,
            extra_params=extra_params
        )

        return payload


def run_module() -> None:

    module: VaultPKIGenerateIntermediateCSRModule = VaultPKIGenerateIntermediateCSRModule()

    if not HAS_HVAC:
        module.fail_json(
            msg=missing_required_lib('hvac'),
            exception=HVAC_IMPORT_ERROR)

    module.initialize_client()

    try:
        payload: dict = module.build_request_payload()
        response: dict = module.client.secrets.pki.generate_intermediate(**payload)
    except Exception:
        module.handle_error(
            VaultModuleError(
                message='Failed to generate intermediate CA CSR',
                details=traceback.format_exc()
            )
        )

    if response.get("warnings") is not None and len(response["warnings"]) > 0:
        warnings: List[str] = response["warnings"]

        for warning in warnings:
            module.warn(warning)

    result: dict = dict(changed=True)

    for key, value in response["data"].items():
        result[key] = value

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == '__main__':
    main()
