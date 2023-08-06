from bitnob.base import Bitnob
from abc import ABC, abstractmethod

class StableCoin(ABC):

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def generate_address(self):
        pass

class USDC(StableCoin, Bitnob): 
    
    def send(self, body:dict):
        """
        Sending USDC

        body = {
            amount: 3000,
            address: "tb1q9h0yjdupyfpxfjg24rpx755xrplvzd9hz2nj7v",
            chain: "BSC"
            description: "lorem ipsum",
        } 

        - POST Request
        """
        required_data = ["amount", "address", "chain"]
        self.check_required_datas(required_data, body)

        return self.send_request("POST", "/wallets/send-usdc", json=body)

    def generate_address(self, body:dict):
        """
        Generate Address for Customer

        body = {
            "label": "purchase xbox",
            "customerEmail": "customer@gmail.com",
            "chain": "BSC"
        }

        - POST Request
        """
        required_data = ["customerEmail", "chain"]
        self.check_required_datas(required_data, body)

        return self.send_request("POST", "/addresses/generate/usdc", json=body)

class USDT(StableCoin, Bitnob): 
    
    def send(self, body:dict):
        """
        Sending USDC

        body = {
            amount: 3000,
            address: "tb1q9h0yjdupyfpxfjg24rpx755xrplvzd9hz2nj7v",
            chain: "BSC",
            description: "lorem ipsum",
        } 

        - POST Request
        """
        required_data = ["amount", "address", "chain"]
        self.check_required_datas(required_data, body)

        return self.send_request("POST", "/wallets/send-usdt", json=body)

    def generate_address(self, body:dict):
        """
        Generate Address for Customer

        body = {
            "label": "purchase xbox",
            "customerEmail": "customer@gmail.com"
            "chain": "BSC"
        }

        - POST Request
        """
        required_data = ["customerEmail", "chain"]
        self.check_required_datas(required_data, body)

        return self.send_request("POST", "/addresses/generate/usdt", json=body)