import json

import eth_account
import eth_account.messages
import requests
import web3

import config
import log_utils

from web3 import Web3

class FlashBotsUtil:
    RELAY_URL = 'https://relay.flashbots.net/'

    @staticmethod
    def send_bundle(bundle, block_number, private_key):
        headers = {
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'eth_sendBundle',
            'params': [
                {
                    'txs': bundle,
                    'blockNumber': block_number
                }
            ]
        })

        headers['X-Flashbots-Signature'] = FlashBotsUtil._get_flashbots_signature(private_key, payload)

        response = requests.post(FlashBotsUtil.RELAY_URL, data=payload, headers=headers)
        log_utils.log_info(f'Bundle sent to FlashBots. Response: {response.text}')

    @staticmethod
    def simulate(bundle, block_number, private_key):
        headers = {
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'eth_callBundle',
            'params': [
                {
                    'txs': bundle,
                    'blockNumber': block_number,
                    'stateBlockNumer': 'latest'
                }
            ]
        })

        headers['X-Flashbots-Signature'] = FlashBotsUtil._get_flashbots_signature(private_key, payload)

        response = requests.post(FlashBotsUtil.RELAY_URL, data=payload, headers=headers)
        log_utils.log_info(f'Called for bundle simulation. Response: {response.text}')

    @staticmethod
    def _get_flashbots_signature(private_key, payload_json):
        message = eth_account.messages.encode_defunct(text=web3.Web3.keccak(text=payload_json).hex())
        return eth_account.Account.from_key(private_key).address + ':' + web3.Web3.toHex(
            eth_account.Account.sign_message(message, private_key).signature)

if __name__ == '__main__':
    PRIVATE_KEY = 'b267c35becff0f91c60f31afb208c98eb5ef58fd93be1f951cca477a5486e670'
    ETH_RPC_URL = 'https://mainnet.infura.io/v3/429fd200dc28407292a9809c9153db09'

    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))

    wallet_address = w3.eth.account.from_key(PRIVATE_KEY).address

    latest_block = w3.eth.get_block('latest')

    tx = {
        'nonce': w3.eth.getTransactionCount(wallet_address),
        'to': wallet_address,
        'type': 2,
        'maxFeePerGas': 1000000000,
        'maxPriorityFeePerGas': 1000000000,
        'chainId': 1,
        'data': '0x',
        'gas': 300000,
    }

    signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
    bundle = [w3.toHex(signed_tx.rawTransaction)]

    FlashBotsUtil.simulate(bundle, Web3.toHex(w3.eth.block_number), PRIVATE_KEY)