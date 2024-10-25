from ci_BESS import BESS
from ci_rate_characterization import Rate
from ci_load_characterization import Load_Profile
import csv
import statistics
import json

class Calculator:

    def __init__(self, rate: Rate, bess: BESS, load_profile: Load_Profile):

        self.rate = rate
        self.bess = bess
        self.load_profile = load_profile
        self.utility = rate.utility


    def energy_charge_value(self, cycles=365):
        rated_power = self.bess.power_rating
        energy_capacity = self.bess.energy_capacity
        rte = self.bess.rte
        discharge_duration = self.bess.discharge_duration

        energy_ecs = self.rate.energy_cost_split(self.rate.energy_charges)
        window_duration_summer = self.rate.window_length(self.rate.summer_tou_periods)
        window_duration_winter = self.rate.window_length(self.rate.winter_tou_periods)

        avg_peak_window_duration = (window_duration_summer[0]*self.rate.season_length()[0] + window_duration_winter[0]*self.rate.season_length()[1])/(7*12)

        if (sum(self.load_profile.load_in_windows_power("peak")))/4 > energy_capacity*rte*cycles:
            return (energy_ecs*rte*cycles*energy_capacity)

        else:
            return (energy_ecs*rte*(sum(self.load_profile.load_in_windows_power("peak")))/4)


    def demand_charge_value(self, cycles=365):

        rated_power = self.bess.power_rating
        energy_capacity = self.bess.energy_capacity
        rte = self.bess.rte
        discharge_duration = self.bess.discharge_duration

        avg_peak_demand = statistics.mean(self.load_profile.load_in_windows_power("peak"))
        peak_demand_charge = self.rate.avg_peak_demand_charges()
        max_peak_demand = max(self.load_profile.load_in_windows_power("peak"))
        window_duration_summer = self.rate.window_length(self.rate.summer_tou_periods)
        window_duration_winter = self.rate.window_length(self.rate.winter_tou_periods)

        avg_peak_window_duration = (window_duration_summer[0] + window_duration_winter[0])/(7*2)
        shift_ratio = (avg_peak_window_duration*avg_peak_demand)/(energy_capacity*rte)

        if shift_ratio > 1:
            if avg_peak_window_duration >= discharge_duration:
                avg_pk_demand_reduction = (energy_capacity*rte)/avg_peak_window_duration

            else:
                avg_pk_demand_reduction = rated_power

        else:

            if max_peak_demand < rated_power:
                avg_pk_demand_reduction = max_peak_demand

            else:
                avg_pk_demand_reduction = rated_power

        return (avg_pk_demand_reduction*peak_demand_charge*12)


    def btm_value(self, cycles=365):
        demand_value = self.demand_charge_value(cycles)
        energy_value = self.energy_charge_value(cycles)

        return demand_value + energy_value

    def pre_BESS_cost(self):


        peak_load = self.load_profile.load_in_windows("peak")
        off_peak_load = self.load_profile.load_in_windows("partial_peak")
        part_peak_load = self.load_profile.load_in_windows("off_peak")

        peak_max_load = self.load_profile.max_load_in_window("peak")
        part_peak_max_load = self.load_profile.max_load_in_window("partial_peak")
        off_peak_max_load = self.load_profile.max_load_in_window("off_peak")

        window_max_loads = [peak_max_load, part_peak_max_load, off_peak_max_load]
        max_load = max(window_max_loads)


        demand_component = self.rate.avg_peak_demand_charges()*peak_max_load*12 + self.rate.avg_part_peak_demand_charges()*part_peak_max_load*12 + self.rate.avg_off_peak_demand_charges()*off_peak_max_load*12
        energy_charges = self.rate.avg_energy_charges()

        energy_component = (sum(peak_load)/4*energy_charges[0] + sum(part_peak_load)/4*energy_charges[1] + sum(off_peak_load)/4*energy_charges[2])
        print(f"Energy component: {energy_component}")

        return demand_component + energy_component


def pre_BESS_cost_single(self, max_load_charge):


        peak_load = self.load_profile.load_in_windows("peak")
        off_peak_load = self.load_profile.load_in_windows("partial_peak")
        part_peak_load = self.load_profile.load_in_windows("off_peak")

        peak_max_load = self.load_profile.max_load_in_window("peak")
        off_peak_max_load = self.load_profile.max_load_in_window("partial_peak")
        part_peak_max_load = self.load_profile.max_load_in_window("off_peak")

        window_max_loads = [peak_max_load, part_peak_max_load, off_peak_max_load]

        max_load = max(window_max_loads)

        demand_component = max_load_charge*max_load*12

        energy_charges = self.rate.avg_energy_charges()

        energy_component = (sum(peak_load)/4*energy_charges[0] + sum(part_peak_load)/4*energy_charges[1] + sum(off_peak_load)/4*energy_charges[2])
        print(f"Energy component: {energy_component}")
        return demand_component + energy_component




