import base64
import configparser
import logging
import os
from Crypto.Cipher import AES
from hashlib import md5

CONFIG_FOLDER = os.getenv('OS_CONFIG_FOLDER', '/etc')
CONFIG_FN = os.getenv('OS_CONFIG_FILENAME')

DEFAULT_CONFIG_FN = 'defaultAssetConfig.ini'
DEFAULT_CONFIG_KY = None
ASSET_CONFIGS = {}


def get_key(agentcore_uuid):
    flipped = 'tt{0}'.format(agentcore_uuid[::-1]).encode('utf-8')
    return md5(flipped).hexdigest().encode('utf-8')


def unpad(s):
    return s[0:-bytearray(s)[-1]]


def decrypt(key, data):
    enc = base64.b64decode(data)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = cipher.decrypt(enc[AES.block_size:])
    return unpad(dec).decode('utf-8')


def get_asset_config(asset_id, ip4, agentcore_uuid, func) -> dict:
    cred = ASSET_CONFIGS.get(asset_id)
    if cred:
        return cred
    fn = os.path.join(CONFIG_FOLDER, f'{asset_id}.ini')
    if os.path.exists(fn):
        key = get_key(agentcore_uuid)
        config = configparser.ConfigParser()
        config.read(fn)
        try:
            ASSET_CONFIGS[asset_id] = cred = func(config, key, decrypt)
        except Exception as e:
            logging.error(f'Credentials [{ip4}] {e}')
        return cred

    cred = ASSET_CONFIGS.get(ip4)
    if cred:
        # make sure next time this will be found for asset_id
        ASSET_CONFIGS[asset_id] = cred
        return cred
    fn = os.path.join(CONFIG_FOLDER, f'{ip4}.ini')
    if os.path.exists(fn):
        key = get_key(agentcore_uuid)
        config = configparser.ConfigParser()
        config.read(fn)
        try:
            ASSET_CONFIGS[ip4] = cred = func(config, key, decrypt)
        except Exception as e:
            logging.error(f'Credentials [{ip4}] {e}')
        return cred

    cred = ASSET_CONFIGS.get(DEFAULT_CONFIG_KY)
    if cred:
        # make sure next time this will be found for asset_id
        ASSET_CONFIGS[asset_id] = cred
        return cred

    fn = os.path.join(CONFIG_FOLDER, DEFAULT_CONFIG_FN)
    if os.path.exists(fn):
        key = get_key(agentcore_uuid)
        config = configparser.ConfigParser()
        config.read(fn)
        try:
            ASSET_CONFIGS[DEFAULT_CONFIG_KY] = cred = \
                func(config, key, decrypt)
        except Exception as e:
            logging.error(f'Credentials [{ip4}] {e}')
        else:
            return cred

    logging.warning(f'Credentials [{ip4}] missing')
