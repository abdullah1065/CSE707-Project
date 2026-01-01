import json
from hashlib import sha256


class Transaction:
    def __init__(self, sender_id: int, receiver_id: int, amount: float, timestamp: str, sender_logic_clock: int, status: str) -> None:
        # Main component of transaction is sender_id, receiver_id, amount
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.timestamp = timestamp
        self.sender_logic_clock = sender_logic_clock
        self.status = status

    def to_tuple(self) -> dict:
        # Convert transaction into a tuple
        return (self.sender_id, self.receiver_id, self.amount)
    
    def to_json(self) -> str:
        # Convert transaction into a json
        return json.dumps(self.__dict__, sort_keys=True)
    
    def __eq__(self, value) -> bool:
        return self.sender_id == value.sender_id and self.recipient_id == value.recipient_id and self.amount == value.amount and self.sender_logic_clock == value.sender_logic_clock and self.timestamp == value.timestamp


class Account:
    def __init__(self, id: int, balance: float) -> None:
        self.id = id
        self.balance = balance


class Block:
    def __init__(self, transaction: Transaction,  previous_hash = None) -> None:
        # Each block contains hash of the previous block and one transaction
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.next_block = None
    
    def hash(self) -> str:
        # Generate hash of the block
        return sha256(str(self.to_dict()).encode()).hexdigest()

    def to_dict(self) -> dict:
        # Convert block into a dictionary
        return {
            "transaction": self.transaction.to_tuple(),
            "previous_hash": self.previous_hash
        }


class Blockchain:
    def __init__(self) -> None:
        self.chain = list()
    
    def add_transaction(self, transaction) -> None:
        # Add new block
        self.chain.append(Block(transaction=transaction))
        # Resort blockchain
        self.resort_chain()

    def resort_chain(self) -> None:
        self.chain.sort(key= lambda block: (block.transaction.timestamp, block.transaction.sender_id))
        self.chain[0].previous_hash = sha256("".encode()).hexdigest()
        for i, block in enumerate(self.chain[:-1]):
            block.next_block = self.chain[i+1]
            block.next_block.previous_hash = block.hash()
        self.chain[-1].next_block = None
