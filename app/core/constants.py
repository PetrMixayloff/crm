from enum import Enum


class RawRemainsActions(Enum):
    invoice = 'Приход'
    cancel = 'Списание'
    inventory = 'Инвентаризация'
    sale = 'Продажа'
