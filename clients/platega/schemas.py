from dataclasses import dataclass
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'
    CONFIRMED = 'CONFIRMED'
    CHARGEBACKED = 'CHARGEBACKED'

@dataclass
class PaymentDetailsBody:
    amount: float
    currency: str

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'currency': self.currency
        }

@dataclass
class PaymentDetailsResponse:
    amount: float
    currency: str

    @classmethod
    def from_dict(cls, data: dict) -> 'PaymentDetailsResponse':
        return cls(
            amount=data.get('amount'),
            currency=data.get('currency')
        )
    
@dataclass
class CreateTransactionBody:
    payment_details: PaymentDetailsBody
    payload: str
    payment_method: int | None = None
    description: str | None = None
    return_url: str | None = None
    failed_url: str | None = None

    def to_dict(self) -> dict:
        return {
            'paymentMethod': self.payment_method,
            'paymentDetails': self.payment_details.to_dict(),
            'description': self.description,
            'return': self.return_url,
            'failed': self.failed_url,
            'payload': self.payload
        }
    
@dataclass
class CreateTransactionResponse:
    transaction_id: str
    status: PaymentStatus
    payment_details: PaymentDetailsResponse
    url: str
    payment_method: int | None = None
    description: str | None = None
    return_url: str | None = None
    failed_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'CreateTransactionResponse':
        return cls(
            transaction_id=data['transactionId'],
            status=PaymentStatus(data['status']),
            payment_details=PaymentDetailsResponse.from_dict(data['paymentDetails']),
            url=data['url'],
            payment_method=data.get('paymentMethod'),
            description=data.get('description'),
            return_url=data.get('return'),
            failed_url=data.get('failed')
        )
    
    @property
    def is_confirmed(self) -> bool:
        return self.status == PaymentStatus.CONFIRMED
    
    @property
    def is_pending(self) -> bool:
        return self.status == PaymentStatus.PENDING