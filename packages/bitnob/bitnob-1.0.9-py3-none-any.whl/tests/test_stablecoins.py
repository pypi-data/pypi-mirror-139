from bitnob import USDT, USDC

def test_generate_usdc_address():
    usdc = USDC()
    body = {
        "chain": "BSC",
        "customerEmail": "precious@bitnob.com"
        }
    data = usdc.generate_address(body=body)
    assert data.address_type == "BSC"