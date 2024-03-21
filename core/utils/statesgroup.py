from aiogram.fsm.state import State, StatesGroup

class MenuStatesGroup(StatesGroup):
    start = State()
    #Switch to ...
    instruction = State()
    test_sub = State()

class SubscriptionsStatesGroup(StatesGroup):
    subscribe = State() # Select subcription
    info = State() # Getting information of subcription
    month = State() # Select count month of subscription
    buy = State() # Select payment method, then buy subscription

class ProfileStatesGroup(StatesGroup):
    main_page = State()

class PaymentStatesGroup(StatesGroup):
    wait = State()
    
class ScannerStatesGroup(StatesGroup):
    start = State()
    
class ScannerStatesGroup(StatesGroup):
    menu = State()
    positions = State()
    markets = State()
    token = State()
    fiat = State()
    type_order = State()
    limits = State()
    payment_method = State()