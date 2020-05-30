from matplotlib import pyplot as plt
from getvariables import PSCADVar, OMEditVar


# Check help(PSCADVar)  if necessary
# Check help(OMEditVar) if necessary


# Provide the .inf path. It is a good practise to add the 'r' before the path itself, to avoid problems
#  with the backslashes '\'

# PSCAD PATH: Defines the path of .INF file
INF_path = r"C:\Users\Luis Arthur\Desktop\Controle_macro\00_Example 1\Example_1.gf42\Channels.inf"
p  = PSCADVar(INF_path, writecsv = False) 


# OMEdit PATH: Defines the path of .CSV file
# CSV_path = r"C:\Users\Luis Arthur\Desktop\Modelica\LUIS\moFiles\WECSlibrary_OMedit.Examples.Example1\omedit.csv"
CSV_path = r"C:\Users\Luis Arthur\Desktop\Modelica\LUIS\moFiles\WECSlibrary_OMedit.Examples.Example1\omedit.mat"
m   = OMEditVar(CSV_path, interp = p.time)


############################################################################
# Treat the data
############################################################################

e = type('error', (object,), {})()

# Error Betas:
e.beta_atual = m.pitchControl1_beta_atual - p.beta_atual
e.beta_ref   = m.pitchControl1_beta_ref   - p.beta_ref

# Error Speeds:
e.wrm  = m.mechanicalCoupling1_wrm - p.wrm
# e.wtur = m.
 

# Error Tem 
e.Te = m.ctrl_Tem_commanded - p.Te

############################################################################
# PLOT variables
############################################################################


plotPSCAD = False
# plotPSCAD = True

plotOMEdit = False
# plotOMEdit = True

comp = False

sub = True



if comp == True:

    # Wind comparison
    plt.figure()
    plt.plot(p.time,m.add1_y ,label='OMEdit wind_speed')
    plt.plot(p.time,m.firstOrder1_y ,label='OMEdit wind_speed_tf')
    plt.plot(p.time,p.wind_speed,'xk',markevery = 100,mew=0.5,label='PSCAD wind_speed')
    plt.plot(p.time,p.wind_speed_tf,'xk',markevery = 100,mew=0.5,label='PSCAD wind_speed_tf')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Beta_atual comparison
    plt.figure()
    plt.plot(p.time,m.pitchControl1_beta_atual ,label='OMEdit beta_atual')
    plt.plot(p.time,p.beta_atual,'xk',markevery = 100,mew=0.5,label='PSCAD beta_atual')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Beta_ref comparison
    plt.figure()
    plt.plot(p.time,m.pitchControl1_beta_ref ,label='OMEdit beta_ref')
    plt.plot(p.time,p.beta_ref,'xk',markevery = 100,mew=0.5,label='PSCAD beta_ref')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Comparison CP
    plt.figure()
    plt.plot(m.time,m.turbine_Cp,label='OMEdit Power Coefficient')
    plt.plot(m.time,p.cp,'xk',markevery = 100,mew=0.5, label='PSCAD Power Coefficient')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Comparison Turbine Torque
    plt.figure()
    plt.plot(p.time,m.turbine_T_tur,label='OMEdit Ttur')
    plt.plot(p.time,p.T_turb,'xk',markevery = 100,mew=0.5,label='PSCAD Ttur')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Comparison Turbine Power
    plt.figure()
    plt.plot(p.time,m.turbine_P_tur,label='OMEdit Ptur')
    plt.plot(p.time,p.P_turb,'xk',markevery = 100,mew=0.5,label='PSCAD Ptur')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Comparison Electromagnetic Torque
    plt.figure()
    plt.plot(p.time,m.ctrl_Tem_commanded ,label='OMEdit beta_atual')
    plt.plot(p.time,p.Te,'xk',markevery = 100,mew=0.5,label='PSCAD beta_atual')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Comparison Wrm
    plt.figure()
    plt.plot(p.time,m.mechanicalCoupling1_wrm,label='OMEdit Wrm')
    plt.plot(p.time,p.wrm,'xk',markevery = 100,mew=0.5,label='PSCAD Wrm')
    plt.legend(loc='best')
    plt.grid(ls=':')
    # plt.show()

    # Comparison Wtur
    plt.figure()
    plt.plot(p.time,m.mechanicalCoupling1_wtur,label='OMEdit Wtur')
    plt.plot(p.time,p.w_turb_br,'xk',markevery = 100,mew=0.5,label='PSCAD Wtur')
    plt.legend(loc='best')
    plt.grid(ls=':')
    plt.show()


    # # Zonas Modelica + chaveamento INI
    # plt.figure()
    # plt.plot(p.time,m.ctrl_zone1,label='zona 1')
    # plt.plot(p.time,m.ctrl_zone2,label='zona 2')
    # plt.plot(p.time,m.ctrl_zone3,label='zona 3')
    # plt.plot(p.time,m.ctrl_zone4,label='zona 4')
    # plt.plot(p.time,p.ctrl_mode,'xk',markevery = 100,mew=0.5,label='zonas PSCAD')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # plt.show()

    # # WRM_ref
    # plt.figure()
    # plt.plot(p.time,m.ctrl_velocityControl_u_ref,label='OMEdit wrm_ref')
    # plt.plot(p.time,p.wrm_ref,'xk',markevery = 100,mew=0.5,label='PSCAD wrm_ref')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # plt.show()

    # # INTEGRADOR TE
    # plt.figure()
    # plt.plot(p.time,m.ctrl_velocityControl_integrator_y,label='OMEdit saida INT Te')
    # plt.plot(p.time,p.Int_Te,'xk',markevery = 100,mew=0.5,label='PSCAD saida INT Te')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # # plt.show()
    
    # # PROPORCIONAL TE
    # plt.figure()
    # plt.plot(p.time,m.ctrl_velocityControl_gain_y,label='OMEdit saida PROP Te')
    # plt.plot(p.time,p.Prop_Te,'xk',markevery = 100,mew=0.5,label='PSCAD saida PROP Te')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # # plt.show()

    # # PI do TE
    # plt.figure()
    # plt.plot(p.time,m.ctrl_velocityControl_y,label='OMEdit saida PI Te')
    # plt.plot(p.time,p.Te_calc,'xk',markevery = 100,mew=0.5,label='PSCAD saida PI Te')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # # plt.show()

    # # INT do BETA
    # plt.figure()
    # plt.plot(p.time,m.ctrl_pitchControl_integrator_y,label='OMEdit saida INT Beta')
    # plt.plot(p.time,p.Int_beta,'xk',markevery = 100,mew=0.5,label='PSCAD saida INT Beta')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # # plt.show()
    
    # plt.figure()
    # plt.plot(p.time,m.ctrl_pitchControl_gain_y,label='OMEdit saida PROP Beta')
    # plt.plot(p.time,p.Prop_beta,'xk',markevery = 100,mew=0.5,label='PSCAD saida PROP Beta')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # # plt.show()

    # plt.figure()
    # plt.plot(p.time,m.ctrl_pitchControl_y,label='OMEdit saida PI Beta')
    # plt.plot(p.time,p.beta_calc,'xk',markevery = 100,mew=0.5,label='PSCAD saida PI Beta')
    # plt.legend(loc='best')
    #plt.grid(ls=':')
    # plt.show()

if sub == True:
    
    plt.figure()
    plt.subplot(211)
    plt.plot(p.time,m.pitchControl1_beta_atual ,label='OMEdit beta_atual')
    plt.plot(p.time,p.beta_atual,'xk',markevery = 100,mew=0.5,label='PSCAD beta_atual')
    plt.legend(loc='best')
    plt.title('Comparison  Beta')
    plt.ylabel('Actual Beta')
    plt.grid(ls=':')

    plt.subplot(212)
    plt.plot(p.time,e.beta_atual)
    plt.xlabel('Time')
    plt.ylabel('Error')
    plt.grid(ls=':')
    plt.show()

    # Beta reference
    plt.figure()
    plt.subplot(311)
    plt.axvline(x=4.4075, linewidth = 1, color='r', ls = '--' )
    plt.plot(p.time,m.pitchControl1_beta_ref ,label='OMEdit beta_ref')
    plt.plot(p.time,p.beta_ref,'xk',markevery = 100,mew=0.5,label='PSCAD beta_ref')
    plt.legend(loc='best')
    plt.title('Comparison Reference Beta')
    plt.ylabel('Reference Beta')
    plt.grid(ls=':')

    plt.subplot(312)
    plt.axvline(x=4.4075, linewidth = 1, color='r', ls = '--' )
    plt.plot(p.time,e.beta_ref)
    plt.ylabel('Error')
    plt.grid(ls=':')

    plt.subplot(313)
    plt.axvline(x=4.4075, linewidth = 1, color='r', ls = '--' )
    plt.plot(p.time,p.control)
    plt.xlabel('Time')
    plt.ylabel('Zone of Control')
    plt.grid(ls=':')
    plt.show()



    # Wrm
    plt.figure()
    plt.subplot(211)
    plt.plot(p.time,m.mechanicalCoupling1_wrm,label='OMEdit Wrm')
    plt.plot(p.time,p.wrm,'xk',markevery = 100,mew=0.5,label='PSCAD Wrm')
    plt.legend(loc='best')
    plt.title('Comparison Machine\'s Speed')
    plt.ylabel('Wrm')
    plt.grid(ls=':')

    plt.subplot(212)
    plt.plot(p.time,e.wrm)
    plt.xlabel('Time')
    plt.ylabel('Error')
    plt.grid(ls=':')
    # plt.show()

    # Electromagnetic Torque
    plt.figure()
    plt.subplot(211)
    plt.axvline(x=4.4075, linewidth = 1, color='r', ls = '--' )
    plt.plot(p.time[30:],m.ctrl_Tem_commanded[30:],label='OMEdit Wrm')
    plt.plot(p.time[30:],p.Te[30:],'xk',markevery = 100,mew=0.5,label='PSCAD Wrm')
    plt.legend(loc='best')
    plt.title('Comparison Eletromagnetic Torque')
    plt.ylabel('Te')
    plt.grid(ls=':')

    plt.subplot(212)
    plt.axvline(x=4.4075, linewidth = 1, color='r', ls = '--' )
    plt.plot(p.time[30:],e.Te[30:])
    plt.xlabel('Time')
    plt.ylabel('Error')
    plt.grid(ls=':')
    plt.show()



if plotOMEdit == True:
    
    # Beta_ref and atual - Modelica
    plt.figure()
    plt.plot(m.time,m.pitchControl1_beta_ref,label='OMEdit beta_ref')
    plt.plot(m.time,m.pitchControl1_beta_atual,label='OMEdit beta_atual')
    plt.grid(ls=':')
    plt.show()







if (plotPSCAD == True):
    plt.figure()
    plt.plot(p.time,p.wrm)
    plt.title("Wrm")
    plt.xlabel("time")
    plt.ylabel("wrm")
    plt.grid(ls=':')
    # plt.show()

    plt.figure()
    plt.plot(p.time,p.cp)
    plt.title("Power Coefficient")
    plt.xlabel("time")
    plt.ylabel("cp")
    plt.grid(ls=':')
    # plt.show()

    plt.figure()
    plt.plot(p.time,p.T_tur_pu)
    plt.title("Variable Plot")
    plt.xlabel("time")
    plt.ylabel("T_tur_Pu")
    plt.grid(ls=':')
    # plt.show()

    plt.figure()
    plt.plot(p.time,p.beta,p.time,p.beta_atual,p.time,p.beta_ref)
    plt.grid(ls=':')
    plt.show()

    plt.figure()
    plt.plot(p.time,p.beta_atual)
    plt.grid(ls=':')
    plt.show()

    plt.figure()
    plt.plot(p.time,p.beta_ref)
    plt.grid(ls=':')
    plt.show()

    plt.figure()
    plt.plot(p.time,p.beta)
    plt.grid(ls=':')
    plt.show()



aaaa = 1
