from dataclasses import dataclass

@dataclass
class VpnClient:
    id: int
    email: str
    sub_id: str
    uuid: str
    expiry_time: int
    enable: bool
    created_at: int

    @classmethod
    def from_dict(cls, data: dict) -> 'VpnClient':
        client = data.get('client', data)
        return cls(
            id=client.get('id', 0),
            email=client.get('email', ''),
            sub_id=client.get('subId', ''),
            uuid=client.get('uuid', ''),
            expiry_time=client.get('expiryTime', 0),
            enable=client.get('enable', True),
            created_at=client.get('createdAt', 0)
        )