from ci_BESS import BESS
from ci_rate_characterization import Rate
from ci_load_characterization import Load_Profile
from ci_calculator import Calculator
import csv
import requests
import json
import statistics

def retention(lifetime_list, yr0_value, lifetime, retention):
    lifetime_list.append(yr0_value)
    adjusted_value = yr0_value


    for i in range(lifetime):
        adjusted_value = adjusted_value * retention
        lifetime_list.append(adjusted_value)

    return lifetime_list

def outputs(sim):
    print("Demand Charge Value: ", sim.demand_charge_value())
    print("Energy Charge Value: ", sim.energy_charge_value())
    print("BTM Value: ", sim.btm_value())
    print("Pre-BESS Cost: ", sim.pre_BESS_cost())

def outputs_single_demand(sim, max_demand):
    print("Demand Charge Value: ", sim.demand_charge_value())
    print("Energy Charge Value: ", sim.energy_charge_value())
    print("BTM Value: ", sim.btm_value())
    print("Pre-BESS Cost: ", sim.pre_BESS_cost_single(max_demand))

#Rate Initialization
pge_bev2 = Rate("ci_rate_database/PGE_BEV2.json")

pge_b10 = Rate("ci_rate_database/PGE_B10.json")
pge_b19 = Rate("ci_rate_database/PGE_B19.json")
sce_tougs3 = Rate("ci_rate_database/SCE_TOUGS3.json")

sce_tou8D = Rate("ci_rate_database/SCE_TOU8D.json")
sce_tou8E = Rate("ci_rate_database/SCE_TOU8E.json")
sce_touev8 = Rate("ci_rate_database/SCE_TOU_EV8.json")
sce_touev9 = Rate("ci_rate_database/SCE_TOU_EV9.json")

sdge_evhp = Rate("ci_rate_database/SDGE_TOUEVHP.json")
sdge_al_tou = Rate("ci_rate_database/SDGE_AL_TOU.json")
sdge_evhp_cpp = Rate("ci_rate_database/SDGE_TOUEVHP_CPP.json")

dukefl_gsd1 = Rate("ci_rate_database/DukeFL_GSD1.json")
dukefl_gst1 = Rate("ci_rate_database/DukeFL_GST1.json")
dukefl_gsdt1 = Rate("ci_rate_database/DukeFL_GSDT1.json")

fpl_gsd1 = Rate("ci_rate_database/FPL_GSD1.json")
fpl_gsdt1 = Rate("ci_rate_database/FPL_GSDT1.json")
fpl_gsld1 = Rate("ci_rate_database/FPL_GSLD1.json")
fpl_gsldt1 = Rate("ci_rate_database/FPL_GSLDT1.json")

bge_gl = Rate("ci_rate_database/BGE_GL.json")
bge_glmtpii = Rate("ci_rate_database/BGE_GL_MTPII.json")

tep_lgstou = Rate("ci_rate_database/TEP_LGSTOU.json")
tep_lgstous = Rate("ci_rate_database/TEP_LGSTOUS.json")
tep_ev = Rate("ci_rate_database/TEP_EV.json")
tep_lgstour19 = Rate("ci_rate_database/TEP_LGSTOUR19.json")

aps_e32mtou = Rate("ci_rate_database/APS_E32MTOU.json")
aps_e32ltou400 = Rate("ci_rate_database/APS_E32LTOU400.json")
aps_e32ltou645 = Rate("ci_rate_database/APS_E32LTOU645.json")
aps_e32lsp = Rate("ci_rate_database/APS_E32LSP.json")
aps_e32dcfc400 = Rate("ci_rate_database/APS_E32DCFC400.json")
aps_e32mcppgs = Rate("ci_rate_database/APS_E32MCPPGS.json")
aps_e32lcppgs = Rate("ci_rate_database/APS_E32LCPPGS.json")

aps_e32lcppgs645 = Rate("ci_rate_database/APS_E32LCPPGS645.json")

epe_tod = Rate("ci_rate_database/EPE_TOD.json")
epe_lpsr = Rate("ci_rate_database/EPE_LPSR.json")
epe_eor = Rate("ci_rate_database/EPE_EOR.json")
epe_ev = Rate("ci_rate_database/EPE_EV.json")


#BESS Initialization
Tesla_MP2XL_4hr = BESS(3916, 979, 0.935, 4)
Sungrow_PowerStack_1070 = BESS(1070, 250, 0.92, 4)
Sungrow_PowerStack_1200 = BESS(1200, 300, 0.92, 4)
Sungrow_PowerStack_1450 = BESS(1450, 360, 0.92, 4)
Sungrow_PowerStack_900 = BESS(900, 225, 0.92, 4)
Sungrow_PowerStack_750 = BESS(750, 187.5, 0.92, 4)


#Load Profile Initialization (examples for TEP, APS included)

#TEP
Bay_4stall_150kW_tep_lgstou = Load_Profile("ci_load_database/Bay_4stall_150kW_7.9SSD.csv", tep_lgstou, Sungrow_PowerStack_750)
Bay_8stall_150kW_tep_lgstou = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", tep_lgstou, Sungrow_PowerStack_1200)
Bay_4stall_250kW_tep_lgstou = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", tep_lgstou, Sungrow_PowerStack_900)
Bay_8stall_250kW_tep_lgstou = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", tep_lgstou, Sungrow_PowerStack_1450)

Bay_4stall_150kW_tep_lgstous = Load_Profile("ci_load_database/Bay_4stall_150kW_7.9SSD.csv", tep_lgstous, Sungrow_PowerStack_750)
Bay_8stall_150kW_tep_lgstous = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", tep_lgstous, Sungrow_PowerStack_1200)
Bay_4stall_250kW_tep_lgstous = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", tep_lgstous, Sungrow_PowerStack_900)
Bay_8stall_250kW_tep_lgstous = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", tep_lgstous, Sungrow_PowerStack_1450)

Bay_4stall_150kW_tep_ev = Load_Profile("ci_load_database/Bay_4stall_150kW_7.9SSD.csv", tep_ev, Sungrow_PowerStack_750)
Bay_4stall_250kW_tep_ev = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", tep_ev, Sungrow_PowerStack_900)
Bay_8stall_150kW_tep_ev = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", tep_ev, Sungrow_PowerStack_1200)
Bay_8stall_250kW_tep_ev = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", tep_ev, Sungrow_PowerStack_1450)

Bay_8stall_250kW_tep_lgstour19 = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", tep_lgstour19, Sungrow_PowerStack_1450)
Bay_4stall_150kW_tep_lgstour19 = Load_Profile("ci_load_database/Bay_4stall_150kW_7.9SSD.csv", tep_lgstour19, Sungrow_PowerStack_750)
Bay_4stall_250kW_tep_lgstour19 = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", tep_lgstour19, Sungrow_PowerStack_900)
Bay_8stall_150kW_tep_lgstour19 = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", tep_lgstour19, Sungrow_PowerStack_1200)



#APS
Bay_4stall_150kW_aps_e32mtou = Load_Profile("ci_load_database/Bay_4stall_150kW_7.9SSD.csv", aps_e32mtou, Sungrow_PowerStack_750)

Bay_4stall_250kW_aps_e32ltou400 = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", aps_e32ltou400, Sungrow_PowerStack_900)
Bay_8stall_150kW_aps_e32ltou400 = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", aps_e32ltou400, Sungrow_PowerStack_1200)

Bay_8stall_250kW_aps_e32ltou645 = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", aps_e32ltou645, Sungrow_PowerStack_1450)

Bay_4stall_250kW_aps_e32lsp = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", aps_e32lsp, Sungrow_PowerStack_900)
Bay_8stall_150kW_aps_e32lsp = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", aps_e32lsp, Sungrow_PowerStack_1200)
Bay_8stall_250kW_aps_e32lsp = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", aps_e32lsp, Sungrow_PowerStack_1450)

Bay_4stall_250kW_aps_e32dcfc400 = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", aps_e32dcfc400, Sungrow_PowerStack_900)
Bay_8stall_250kW_aps_e32dcfc400 = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", aps_e32dcfc400, Sungrow_PowerStack_1450)

Bay_4stall_150kW_aps_e32mcppgs = Load_Profile("ci_load_database/Bay_4stall_150kW_7.9SSD.csv", aps_e32mcppgs, Sungrow_PowerStack_750)

Bay_4stall_250kW_aps_e32lcppgs = Load_Profile("ci_load_database/Bay_4stall_250kW_7.9SSD.csv", aps_e32lcppgs, Sungrow_PowerStack_900)
Bay_8stall_150kW_aps_e32lcppgs = Load_Profile("ci_load_database/Bay_8stall_150kW_5.9SSD.csv", aps_e32lcppgs, Sungrow_PowerStack_1200)

Bay_8stall_250kW_aps_e32lcppgs645 = Load_Profile("ci_load_database/Bay_8stall_250kW_5.9SSD.csv", aps_e32lcppgs645, Sungrow_PowerStack_1450)


#Sim Initialization (examples for TEP, APS included)

#TEP
sim_tep_lgstou_Bay_4stall_150kW = Calculator(tep_lgstou, Sungrow_PowerStack_750, Bay_4stall_150kW_tep_lgstou)
sim_tep_lgstou_Bay_8stall_150kW = Calculator(tep_lgstou, Sungrow_PowerStack_1200, Bay_8stall_150kW_tep_lgstou)
sim_tep_lgstou_Bay_4stall_250kW = Calculator(tep_lgstou, Sungrow_PowerStack_900, Bay_4stall_250kW_tep_lgstou)
sim_tep_lgstou_Bay_8stall_250kW = Calculator(tep_lgstou, Sungrow_PowerStack_1450, Bay_8stall_250kW_tep_lgstou)

sim_tep_lgstous_Bay_4stall_150kW = Calculator(tep_lgstous, Sungrow_PowerStack_750, Bay_4stall_150kW_tep_lgstous)
sim_tep_lgstous_Bay_8stall_150kW = Calculator(tep_lgstous, Sungrow_PowerStack_1200, Bay_8stall_150kW_tep_lgstous)
sim_tep_lgstous_Bay_4stall_250kW = Calculator(tep_lgstous, Sungrow_PowerStack_900, Bay_4stall_250kW_tep_lgstous)
sim_tep_lgstous_Bay_8stall_250kW = Calculator(tep_lgstous, Sungrow_PowerStack_1450, Bay_8stall_250kW_tep_lgstous)

sim_tep_ev_Bay_4stall_150kW = Calculator(tep_ev, Sungrow_PowerStack_750, Bay_4stall_150kW_tep_ev)
sim_tep_ev_Bay_4stall_250kW = Calculator(tep_ev, Sungrow_PowerStack_900, Bay_4stall_250kW_tep_ev)
sim_tep_ev_Bay_8stall_150kW = Calculator(tep_ev, Sungrow_PowerStack_1200, Bay_8stall_150kW_tep_ev)
sim_tep_ev_Bay_8stall_250kW = Calculator(tep_ev, Sungrow_PowerStack_1450, Bay_8stall_250kW_tep_ev)

sim_tep_lgstour19_Bay_8stall_250kW = Calculator(tep_lgstour19, Sungrow_PowerStack_1450, Bay_8stall_250kW_tep_lgstour19)
sim_tep_lgstour19_Bay_4stall_150kW = Calculator(tep_lgstour19, Sungrow_PowerStack_750, Bay_4stall_150kW_tep_lgstour19)
sim_tep_lgstour19_Bay_4stall_250kW = Calculator(tep_lgstour19, Sungrow_PowerStack_900, Bay_4stall_250kW_tep_lgstour19)
sim_tep_lgstour19_Bay_8stall_150kW = Calculator(tep_lgstour19, Sungrow_PowerStack_1200, Bay_8stall_150kW_tep_lgstour19)

#APS
sim_aps_e32mtou_Bay_4stall_150kW = Calculator(aps_e32mtou, Sungrow_PowerStack_750, Bay_4stall_150kW_aps_e32mtou)

sim_aps_e32ltou400_Bay_4stall_250kW = Calculator(aps_e32ltou400, Sungrow_PowerStack_900, Bay_4stall_250kW_aps_e32ltou400)
sim_aps_e32ltou400_Bay_8stall_150kW = Calculator(aps_e32ltou400, Sungrow_PowerStack_1200, Bay_8stall_150kW_aps_e32ltou400)

sim_aps_e32ltou645_Bay_8stall_250kW = Calculator(aps_e32ltou645, Sungrow_PowerStack_1450, Bay_8stall_250kW_aps_e32ltou645)

sim_aps_e32lsp_Bay_4stall_250kW = Calculator(aps_e32lsp, Sungrow_PowerStack_900, Bay_4stall_250kW_aps_e32lsp)
sim_aps_e32lsp_Bay_8stall_150kW = Calculator(aps_e32lsp, Sungrow_PowerStack_1200, Bay_8stall_150kW_aps_e32lsp)
sim_aps_e32lsp_Bay_8stall_250kW = Calculator(aps_e32lsp, Sungrow_PowerStack_1450, Bay_8stall_250kW_aps_e32lsp)

sim_aps_e32dcfc400_Bay_4stall_250kW = Calculator(aps_e32dcfc400, Sungrow_PowerStack_900, Bay_4stall_250kW_aps_e32dcfc400)
sim_aps_e32dcfc400_Bay_8stall_250kW = Calculator(aps_e32dcfc400, Sungrow_PowerStack_1450, Bay_8stall_250kW_aps_e32dcfc400)

sim_aps_e32mcppgs_Bay_4stall_150kW = Calculator(aps_e32mcppgs, Sungrow_PowerStack_750, Bay_4stall_150kW_aps_e32mcppgs)

sim_aps_e32lcppgs_Bay_4stall_250kW = Calculator(aps_e32lcppgs, Sungrow_PowerStack_900, Bay_4stall_250kW_aps_e32lcppgs)
sim_aps_e32lcppgs_Bay_8stall_150kW = Calculator(aps_e32lcppgs, Sungrow_PowerStack_1200, Bay_8stall_150kW_aps_e32lcppgs)

sim_aps_e32lcppgs645_Bay_8stall_250kW = Calculator(aps_e32lcppgs645, Sungrow_PowerStack_1450, Bay_8stall_250kW_aps_e32lcppgs645)


#Outputs - include the sim you want to analyze. Will generate print statements for each output
outputs(sim_aps_e32mtou_Bay_4stall_150kW)



