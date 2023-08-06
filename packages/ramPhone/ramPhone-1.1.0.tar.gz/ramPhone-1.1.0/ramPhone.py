import random


def toPhone() -> str:
    phone = f'1{random.choice([3, 5, 8, 9])}{random.randint(0, 9)}'+''.join(random.sample('0123456789', 8))
    return phone


def toPhoneSegment(Segment: list) -> str:
    phone = f'1{random.choice(Segment)}{random.randint(0, 9)}'+''.join(random.sample('0123456789', 8))
    return phone


def toPhoneAreaCode(AreaCode: str) -> str:
    phone = f'1{random.choice([3, 5, 8, 9])}{random.randint(0, 9)}{AreaCode}'+''.join(random.sample('0123456789', 4))
    return phone


def toPhoneSegmentAndAreaCode(Segment: list, AreaCode: str) -> str:
    phone = f'1{random.choice(Segment)}{random.randint(0, 9)}{AreaCode}'+''.join(random.sample('0123456789', 4))
    return phone