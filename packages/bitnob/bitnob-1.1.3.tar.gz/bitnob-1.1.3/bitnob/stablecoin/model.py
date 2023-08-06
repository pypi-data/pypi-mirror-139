class Receipt:
    def __init__(self, id, reference, description, amount, centAmount, fees, centFees, action, type, status) -> None:
        self.reference =reference
        self.description = description
        self.amount = amount
        self.centAmount = centAmount
        self.fees = fees
        self.centFees = centFees
        self.action = action
        self.type = type
        self.status = status
        self.id=id
    
    @property
    def total_amount(self):
        """
        Total amount debited from user
        """
        return self.amount + self.fees
    
    @property
    def total_cents(self):
        """
        Total cents debited from user
        """
        return self.centAmount + self.centFees