import json
import csv
import statistics


class Rate:

    def __init__(self, rate_json_filepath):

        rate_json = open(rate_json_filepath)
        rate_dict = json.load(rate_json)

        self.rate_dict = rate_dict
        self.utility = rate_dict['utility']
        self.name = rate_dict['name']
        self.demand_charges = rate_dict['demand_charges']
        self.energy_charges = rate_dict['energy_charges']
        self.seasons = rate_dict['seasons']
        self.summer = rate_dict["seasons"]["Summer"]
        self.winter = rate_dict["seasons"]["Winter"]
        self.summer_tou_periods = self.summer["tou_periods"]
        self.winter_tou_periods = self.winter["tou_periods"]

        self.summer_start_day = self.summer["fromDay"]
        self.summer_end_day = self.summer["toDay"]
        self.summer_start_month = self.summer["fromMonth"]
        self.summer_end_month = self.summer["toMonth"]

        self.winter_start_day = self.winter["fromDay"]
        self.winter_end_day = self.winter["toDay"]
        self.winter_start_month = self.winter["fromMonth"]
        self.winter_end_month = self.winter["toMonth"]


    def window_length(self, season_tou_periods):

        peak_list = season_tou_periods["ON_PEAK"]
        partial_list = season_tou_periods["PARTIAL_PEAK"]
        off_list = season_tou_periods["OFF_PEAK"]

        peak_duratiom = 0
        partial_duration = 0
        off_duration = 0

        for i in peak_list:

            if i["toHour"] > i["fromHour"]:
                window = (i["toHour"] - i["fromHour"]) * (i["toDayOfWeek"]-i["fromDayOfWeek"] + 1)

            elif i["toHour"] < i["fromHour"]:
                window = ((24 - i["fromHour"] + i["toHour"])) * (i["toDayOfWeek"]-i["fromDayOfWeek"] + 1)

            else:
                window = 24 * (i["toDayOfWeek"]-i["fromDayOfWeek"] + 1)

            peak_duratiom += window

        for j in partial_list:

                if j["toHour"] > j["fromHour"]:
                    window = (j["toHour"] - j["fromHour"]) * (j["toDayOfWeek"]-j["fromDayOfWeek"] + 1)

                elif j["toHour"] < j["fromHour"]:
                    window = ((24 - j["fromHour"] + j["toHour"])) * (j["toDayOfWeek"]-j["fromDayOfWeek"] + 1)

                else:
                    window = 24 * (j["toDayOfWeek"]-j["fromDayOfWeek"] + 1)

                partial_duration += window


        for k in off_list:

                if k["toHour"] > k["fromHour"]:
                    window = (k["toHour"] - k["fromHour"]) * (k["toDayOfWeek"]-k["fromDayOfWeek"] + 1)

                elif k["toHour"] < k["fromHour"]:
                    window = ((24 - k["fromHour"] + k["toHour"])) * (k["toDayOfWeek"]-k["fromDayOfWeek"] + 1)

                else:
                    window = 24 * (k["toDayOfWeek"]-k["fromDayOfWeek"] + 1)

                off_duration += window

        return[peak_duratiom, partial_duration, off_duration]


    def season_length(self):

        if self.summer_start_day == self.summer_end_day:
           summer_season_length = self.summer_end_month - self.summer_start_month

        elif self.summer_start_day > self.summer_end_day:
            summer_season_length = self.summer_end_month - self.summer_start_month - 1

        else:
            summer_season_length = self.summer_end_month - self.summer_start_month + 1

        return [abs(summer_season_length), 12 - abs(summer_season_length)]


    def energy_cost_split(self, energy_charges):

        summer_charges = energy_charges["Summer"]
        winter_charges = energy_charges["Winter"]

        summer_season_length = self.season_length()[0]
        winter_season_length = self.season_length()[1]

        summer_ECS = summer_charges["ON_PEAK"] - summer_charges["OFF_PEAK"]
        winter_ECS = winter_charges["ON_PEAK"] - winter_charges["OFF_PEAK"]

        total_ECS = summer_ECS * (summer_season_length/(summer_season_length + winter_season_length)) + winter_ECS * (winter_season_length/(summer_season_length + winter_season_length))

        return total_ECS


    def demand_cost_split(self, demand_charges):

        summer_charges = demand_charges["Summer"]
        winter_charges = demand_charges["Winter"]

        summer_season_length = self.season_length()[0]
        winter_season_length = self.season_length()[1]

        summer_DCS = summer_charges["ON_PEAK"] - summer_charges["OFF_PEAK"]
        winter_DCS = winter_charges["ON_PEAK"] - winter_charges["OFF_PEAK"]

        total_DCS = summer_DCS * (summer_season_length/(summer_season_length + winter_season_length)) + winter_DCS * (winter_season_length/(summer_season_length + winter_season_length))

        return total_DCS


    def avg_peak_demand_charges(self):
        summer_demand = self.demand_charges["Summer"]
        winter_demand = self.demand_charges["Winter"]
        all_demand = self.demand_charges["ALL"]

        if float(all_demand["ALL"]) > 0:
            return float(all_demand["ALL"])

        if float(summer_demand["ALL"]) > 0:
            avg_summer_demand_charge = float(summer_demand["ALL"])

        if float(summer_demand["ALL"]) == 0:
            avg_summer_demand_charge = float(summer_demand["ON_PEAK"])

        if float(winter_demand["ALL"]) > 0:
            avg_winter_demand_charge = float(winter_demand["ALL"])

        if float(winter_demand["ALL"]) == 0:
            avg_winter_demand_charge = float(winter_demand["ON_PEAK"])

        return (avg_summer_demand_charge * self.season_length()[0] +avg_winter_demand_charge * self.season_length()[1]) / 12


    def avg_part_peak_demand_charges(self):
        summer_demand = self.demand_charges["Summer"]
        winter_demand = self.demand_charges["Winter"]
        all_demand = self.demand_charges["ALL"]

        if float(all_demand["ALL"]) > 0:
            return float(all_demand["ALL"])

        if float(summer_demand["ALL"]) > 0:
            avg_summer_demand_charge = float(summer_demand["ALL"])

        if float(summer_demand["ALL"]) == 0:
            avg_summer_demand_charge = float(summer_demand["PARTIAL_PEAK"])

        if float(winter_demand["ALL"]) > 0:
            avg_winter_demand_charge = float(winter_demand["ALL"])

        if float(winter_demand["ALL"]) == 0:
            avg_winter_demand_charge = float(winter_demand["PARTIAL_PEAK"])

        return (avg_summer_demand_charge * self.season_length()[0] +avg_winter_demand_charge * self.season_length()[1]) / 12



    def avg_off_peak_demand_charges(self):
        summer_demand = self.demand_charges["Summer"]
        winter_demand = self.demand_charges["Winter"]
        all_demand = self.demand_charges["ALL"]

        if float(all_demand["ALL"]) > 0:
            return float(all_demand["ALL"])

        if float(summer_demand["ALL"]) > 0:
            avg_summer_demand_charge = float(summer_demand["ALL"])

        if float(summer_demand["ALL"]) == 0:
            avg_summer_demand_charge = float(summer_demand["OFF_PEAK"])

        if float(winter_demand["ALL"]) > 0:
            avg_winter_demand_charge = float(winter_demand["ALL"])

        if float(winter_demand["ALL"]) == 0:
            avg_winter_demand_charge = float(winter_demand["OFF_PEAK"])

        return (avg_summer_demand_charge * self.season_length()[0] +avg_winter_demand_charge * self.season_length()[1]) / 12



    def avg_energy_charges(self):
        summer_peak = self.energy_charges["Summer"]["ON_PEAK"]
        winter_peak = self.energy_charges["Winter"]["ON_PEAK"]
        summer_off = self.energy_charges["Summer"]["OFF_PEAK"]
        winter_off = self.energy_charges["Winter"]["OFF_PEAK"]
        summer_part_peak = self.energy_charges["Summer"]["PARTIAL_PEAK"]
        winter_part_peak = self.energy_charges["Winter"]["PARTIAL_PEAK"]

        avg_peak = (summer_peak * self.season_length()[0] + winter_peak * self.season_length()[1])/12
        avg_part_peak = (summer_part_peak * self.season_length()[0] + winter_part_peak * self.season_length()[1])/12
        avg_off = (summer_off * self.season_length()[0] + winter_off * self.season_length()[1])/12

        return [avg_peak, avg_part_peak, avg_off]



    def __str__(self):
        return f"Utility: {self.utility}, Rate Name: {self.name}"


