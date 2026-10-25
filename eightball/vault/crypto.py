"""Maintained AES-GCM envelope primitives; injected local keys are not managed KMS."""
import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class LocalKeyWrapper:
    """Fictional/local deployment adapter. Caller persists/protects keys separately."""

    def __init__(self, keys: dict[str, bytes], *, active_key_id: str):
        if active_key_id not in keys or any(len(key) != 32 for key in keys.values()):
            raise ValueError('Explicit 256-bit wrapping keys required')
        self.keys, self.active_key_id = dict(keys), active_key_id

    def wrap(self, key, *, context):
        nonce = os.urandom(12)
        encrypted = AESGCM(self.keys[self.active_key_id]).encrypt(nonce, key, context)
        return {'key_id': self.active_key_id, 'nonce': base64.b64encode(nonce).decode('ascii'),
                'wrapped_key': base64.b64encode(encrypted).decode('ascii')}

    def unwrap(self, envelope, *, context):
        return AESGCM(self.keys[envelope['key_id']]).decrypt(
            base64.b64decode(envelope['nonce'], validate=True),
            base64.b64decode(envelope['wrapped_key'], validate=True), context)


def encrypt(content, wrapper, *, context):
    key, nonce = AESGCM.generate_key(bit_length=256), os.urandom(12)
    return nonce, AESGCM(key).encrypt(nonce, content, context), wrapper.wrap(key, context=context)


def decrypt(nonce, content, envelope, wrapper, *, context):
    return AESGCM(wrapper.unwrap(envelope, context=context)).decrypt(nonce, content, context)
