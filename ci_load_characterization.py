import json
import csv
import statistics
from ci_rate_characterization import Rate


class Load_Profile:

    def __init__(self, load_profile_filepath, rate, BESS):

        with open(load_profile_filepath, mode='r') as load_profile_raw:
            load_profile = csv.reader(load_profile_raw)
            load_profile = list(load_profile)
            lp_temp = []
            lp_temp.append(["timestamp", "hour", "month", "day", "adjusted_power"])

            for i in range(1, len(load_profile), 1):
                lp_temp.append([[load_profile[i][0]], float(load_profile[i][1]), float(load_profile[i][2]), float(load_profile[i][3]), float(load_profile[i][4])])

            self.load_profile = lp_temp

        self.rate = rate
        self.name = load_profile_filepath
        self.BESS = BESS
        self.power_rating = BESS.power_rating


    def isolate_load_lists(self):

        timestamp_list = []
        hour_list = []
        month_list = []
        day_list = []
        adjusted_power_list = []

        for window in self.load_profile:
            timestamp_list.append(window[0])
            hour_list.append(window[1])
            month_list.append(window[2])
            day_list.append(window[3])
            adjusted_power_list.append(window[4])

        return [timestamp_list, hour_list, month_list, day_list, adjusted_power_list]


    def build_load_dict(self):

        load_lists = self.isolate_load_lists()

        load_profile_dict = {
            "timestamp": load_lists[0],
            "hour": load_lists[1],
            "month": load_lists[2],
            "day": load_lists[3],
            "adjusted_power": load_lists[4],
            "rate": self.rate.rate_dict,
            "rate_seasons": self.rate.seasons
        }

        return load_profile_dict


    def max_load_year(self):
        return max(self.isolate_load_lists()[4][1:len(self.isolate_load_lists()[4])])

    def avg_load_year(self):
        return statistics.mean(self.isolate_load_lists()[4][1:len(self.isolate_load_lists()[4])])

    def load_factor(self):
        return self.avg_load_year() / self.max_load_year()

    def total_load_year(self):
        return sum(self.isolate_load_lists()[4][1:len(self.isolate_load_lists()[4])])


    def is_in_summer(self, load_instance):
        rate = self.rate
        seasons = rate.seasons

        if int(seasons["Summer"]["fromMonth"]) < int(seasons["Summer"]["toMonth"]):
            if load_instance[2] + 1 >= int(seasons["Summer"]["fromMonth"]) and load_instance[2] + 1 <= int(seasons["Summer"]["toMonth"]):
                return True

        elif int(seasons["Summer"]["fromMonth"]) > int(seasons["Summer"]["toMonth"]):
            if load_instance[2] + 1 >= int(seasons["Summer"]["fromMonth"]) or load_instance[2] + 1 <= int(seasons["Summer"]["toMonth"]):
                return True

        else:
            return False


    def is_in_winter(self, load_instance):
        rate = self.rate
        seasons = rate.seasons

        if int(seasons["Winter"]["fromMonth"]) < int(seasons["Winter"]["toMonth"]):
            if load_instance[2] + 1 >= int(seasons["Winter"]["fromMonth"]) and load_instance[2] + 1 <= int(seasons["Winter"]["toMonth"]):
                return True

        elif int(seasons["Winter"]["fromMonth"]) > int(seasons["Winter"]["toMonth"]):
            if load_instance[2] + 1 >= int(seasons["Winter"]["fromMonth"]) or load_instance[2] + 1 <= int(seasons["Winter"]["toMonth"]):
                return True

        else:
            return False



    def is_in_peak_window(self, load_instance):

        seasons = self.rate.seasons
        peak_windows_summer = seasons["Summer"]["tou_periods"]["ON_PEAK"]
        peak_windows_winter = seasons["Winter"]["tou_periods"]["ON_PEAK"]

        if self.is_in_summer(load_instance):

            for i in peak_windows_summer:
                if (i["toHour"]>i["fromHour"]
                    and i["fromDayOfWeek"] <= load_instance[3] <= i["toDayOfWeek"]
                    and i["fromHour"] <= load_instance[1] < i["toHour"]):
                    return True

                elif (i["toHour"] < i["fromHour"]
                    and i["fromDayOfWeek"] <= load_instance[3 <= i["toDayOfWeek"]]
                    and (i["fromHour"] <= load_instance[1]
                    or load_instance[1] <= i["toHour"])): # might have to change condition for bounds

                    return True

            return False


        elif self.is_in_winter(load_instance):

            for j in peak_windows_winter:
                if (j["toHour"]>j["fromHour"]
                    and j["fromDayOfWeek"] <= load_instance[3] <= j["toDayOfWeek"]
                    and j["fromHour"] <= load_instance[1] < j["toHour"]):
                    return True

                elif (j["toHour"] < j["fromHour"]
                    and j["fromDayOfWeek"] <= load_instance[3] <= j["toDayOfWeek"]
                    and (j["fromHour"] <= load_instance[1]
                    or load_instance[1] <= j["toHour"])):

                    return True

            return False



    def is_in_part_peak_window(self, load_instance):

        seasons = self.rate.seasons
        part_peak_windows_summer = seasons["Summer"]["tou_periods"]["PARTIAL_PEAK"]
        part_peak_windows_winter = seasons["Winter"]["tou_periods"]["PARTIAL_PEAK"]

        if self.is_in_summer(load_instance):

            for i in part_peak_windows_summer:
                if (i["toHour"]>i["fromHour"]
                    and i["fromDayOfWeek"] <= load_instance[3] <= i["toDayOfWeek"]
                    and i["fromHour"] <= load_instance[1] < i["toHour"]):
                    return True

                elif (i["toHour"] < i["fromHour"]
                    and i["fromDayOfWeek"] <= load_instance[3] <= i["toDayOfWeek"]
                    and (i["fromHour"] <= load_instance[1]
                    or load_instance[1] <= i["toHour"])):

                    return True

            return False


        elif self.is_in_winter(load_instance):

            for j in part_peak_windows_winter:
                if (j["toHour"]>j["fromHour"]
                    and j["fromDayOfWeek"] <= load_instance[3] <= j["toDayOfWeek"]
                    and j["fromHour"] <= load_instance[1] < j["toHour"]):
                    return True

                elif (j["toHour"] < j["fromHour"]
                    and j["fromDayOfWeek"] <= load_instance[3] <= j["toDayOfWeek"]
                    and (j["fromHour"] <= load_instance[1]
                    or load_instance[1] <= j["toHour"])):

                    return True

            return False


    def is_in_off_peak_window(self, load_instance):

        seasons = self.rate.seasons
        off_peak_windows_summer = seasons["Summer"]["tou_periods"]["OFF_PEAK"]
        off_peak_windows_winter = seasons["Winter"]["tou_periods"]["OFF_PEAK"]

        if self.is_in_summer(load_instance):

            for i in off_peak_windows_summer:
                if (i["toHour"]>i["fromHour"]
                    and i["fromDayOfWeek"] <= load_instance[3] <= i["toDayOfWeek"]
                    and i["fromHour"] <= load_instance[1] < i["toHour"]):
                    return True

                elif (i["toHour"] < i["fromHour"]
                    and i["fromDayOfWeek"] <= load_instance[3] <= i["toDayOfWeek"]
                    and (i["fromHour"] <= load_instance[1]
                    or load_instance[1] <= i["toHour"])):

                    return True

            return False


        elif self.is_in_winter(load_instance):

            for j in off_peak_windows_winter:
                if (j["toHour"]>j["fromHour"]
                    and j["fromDayOfWeek"] <= load_instance[3] <= j["toDayOfWeek"]
                    and j["fromHour"] <= load_instance[1] < j["toHour"]):
                    return True

                elif (j["toHour"] < j["fromHour"]
                    and j["fromDayOfWeek"] <= load_instance[3] <= j["toDayOfWeek"]
                    and (j["fromHour"] <= load_instance[1]
                    or load_instance[1] <= j["toHour"])):

                        return True

            return False


    def load_in_windows(self, window):

        load_instance_list = self.load_profile
        window_load = []

        if window == "peak":
            for i in range(1, len(load_instance_list), 1):
                if self.is_in_peak_window(load_instance_list[i]):
                    window_load.append(load_instance_list[i][4])

        elif window == "partial_peak":
            for i in range(1, len(load_instance_list), 1):
                if self.is_in_part_peak_window(load_instance_list[i]):
                    window_load.append(load_instance_list[i][4])

        elif window == "off_peak":
            for i in range(1, len(load_instance_list), 1):
                if self.is_in_off_peak_window(load_instance_list[i]):
                    window_load.append(load_instance_list[i][4])

        return window_load


    def load_in_windows_power(self, window):

        load_instance_list = self.load_profile
        window_load = []
        power_rating = self.power_rating

        if window == "peak":
            for i in range(1, len(load_instance_list), 1):
                if self.is_in_peak_window(load_instance_list[i]) and load_instance_list[i][4] < power_rating:
                    window_load.append(load_instance_list[i][4])

                elif self.is_in_peak_window(load_instance_list[i]) and load_instance_list[i][4] >= power_rating:
                    window_load.append(power_rating)

        elif window == "partial_peak":
            if self.is_in_part_peak_window(load_instance_list[i]) and load_instance_list[i][4] < power_rating:
                    window_load.append(load_instance_list[i][4])

            elif self.is_in_part_peak_window(load_instance_list[i]) and load_instance_list[i][4] >= power_rating:
                    window_load.append(power_rating)

        elif window == "off_peak":
            if self.is_in_off_peak_window(load_instance_list[i]) and load_instance_list[i][4] < power_rating:
                    window_load.append(load_instance_list[i][4])

            elif self.is_in_off_peak_window(load_instance_list[i]) and load_instance_list[i][4] >= power_rating:
                    window_load.append(power_rating)

        return window_load



    def max_load_in_window(self, window):
        return max(self.load_in_windows(window))

    def avg_load_in_window(self, window):
        return statistics.mean(self.load_in_windows(window))
    
    def monthly_avg_peak_demand(self):
        peak_list = []
        max_list = []
        avg_max = 0

        monthly_dict = {"0": [],
                        "1": [],
                        "2": [],
                        "3": [],
                        "4": [],
                        "5": [],
                        "6": [],
                        "7": [],
                        "8": [],
                        "9": [],
                        "10": [],
                        "11": []}
        
        for i in range(1, len(self.load_profile)):
            if self.is_in_peak_window(self.load_profile[i]):
                peak_list.append(self.load_profile[i])

        for load_instance in peak_list:
            for key, val in monthly_dict.items():
                if float(key) == float(load_instance[2]):
                    val.append(load_instance[4])
                    monthly_dict[key] = val

        for key, val in monthly_dict.items():
            max_list.append(max(val))

        return statistics.mean(max_list)
    
    def __str__(self):
        return f"LP Path: {self.build_load_dict()}, Max Load: {self.max_load_year()}, Avg Load: {self.avg_load_year()}, Load Factor: {self.load_factor()}"