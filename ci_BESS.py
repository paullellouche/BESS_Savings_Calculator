import statistics
from ci_rate_characterization import Rate

class BESS:

    def __init__(self, energy_capacity, power_rating, rte, discharge_duraion):

        self.energy_capacity = energy_capacity
        self.power_rating = power_rating
        self.rte = rte
        self.discharge_duration = discharge_duraion