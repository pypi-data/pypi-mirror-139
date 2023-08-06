import secrets
from sha3 import keccak_256
from coincurve import PublicKey
from dataclasses import dataclass, asdict

@dataclass
class BlockchainInfo:
  private_key: str
  public_key:  str
  address:     str
  def to_dict(self):
    return asdict(self)

def generate_blockchain_info():
  private_key =  keccak_256(secrets.token_bytes(32)).digest()
  public_key  =  PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
  address     =  keccak_256(public_key).digest()[-20:]

  return BlockchainInfo(
    private_key  =  private_key.hex(),
    public_key   =  public_key.hex(),
    address      =  '0x' + address.hex(),
  )