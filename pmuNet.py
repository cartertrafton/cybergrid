from synchrophasor.frame import *
from synchrophasor.pmu import Pmu
from synchrophasor.pdc import Pdc
from synchrophasor.frame import DataFrame
import random
import sys
from time import sleep
exec_type, pmuID, pmu_ip, port, buffer_size, setTS = sys.argv[1:7]

cybergridCfg = ConfigFrame2(1410,  # PMU_ID
                       1000000,  # TIME_BASE
                       1,  # Number of PMUs included in data frame
                       "Microgrid Station",  # Station name
                       1410,  # Data-stream ID(s)
                       (True, True, True, True),  # Data format - POLAR; PH - REAL; AN - REAL; FREQ - REAL;
                       3,  # Number of phasors
                       1,  # Number of analog values
                       1,  # Number of digital status words
                       ["VA", "VB", "VC", "ANALOG1", "BREAKER 1 STATUS",
                        "BREAKER 2 STATUS", "BREAKER 3 STATUS", "BREAKER 4 STATUS", "BREAKER 5 STATUS",
                        "BREAKER 6 STATUS", "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",
                        "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS", "BREAKER D STATUS",
                        "BREAKER E STATUS", "BREAKER F STATUS", "BREAKER G STATUS"],  # Channel Names
                       [(0, "v"), (0, "v"),
                        (0, "v")],  # Conversion factor for phasor channels - (float representation, not important)
                       [(1, "pow")],  # Conversion factor for analog channels
                       [(0x0000, 0xffff)],  # Mask words for digital status words
                       60,  # Nominal frequency
                       1,  # Configuration change count
                       60)  # Rate of phasor data transmission)


def phaseIncrem(lastAng): # increments phase angle value (in radians)
    lowerB = -3.142
    upperB = 3.142
    radDiff = 0.10466666667

    if lastAng + radDiff >= upperB:
        lastAng = lastAng + radDiff + lowerB - upperB
    elif lastAng + radDiff >= lowerB:
        lastAng = lastAng + radDiff

    return lastAng


cybergrid_data_sample = DataFrame(1, ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
                                          [(14635, 0), (-7318, -3.14), (-7318, 3.14)], 30, 0,
                                          [100], [0x3c12], cybergridCfg)

if exec_type == "PMU":
    pmu = Pmu(pmu_id=int(pmuID), port=int(port), ip=pmu_ip, buffer_size=int(buffer_size), set_timestamp=setTS)

    pmu.set_configuration(cybergridCfg)  # This will load PMU configuration specified in IEEE C37.118.2 -Annex D (Table D.2)
    phaseAng1 = -1.13
    phaseAng2 = 3.14/2
    phaseAng3 = -3.14
    pmu.run()  # PMU starts listening for incoming connections
    # setPDC(pmuID,pmu_ip,port)
    while True:
        try:
            if pmu.clients:
                if pmu.listener:  # Check if there is any connected PDCs
                    sleep(1/pmu.cfg2.get_data_rate())
                    print(phaseAng1, phaseAng2, phaseAng3)

                    cybergrid_data_sample.set_phasors([(120.0, phaseAng1), (120.0, phaseAng2), (120.0, phaseAng3)])
                    # pmu.send_data(phasors=[(120.0, 3.14),
                    #                        (120.0, 3.14),
                    #                        (120.0, 3.14)],
                    #               analog=[9.91],
                    #               digital=[0x0001])
                    pmu.send(cybergrid_data_sample)  # Sending sample data frame specified in IEEE C37.118.2 - Annex D (Table D.1)
                    phaseAng1 = phaseIncrem(phaseAng1)
                    phaseAng2 = phaseIncrem(phaseAng2)
                    phaseAng3 = phaseIncrem(phaseAng3)

        except EnvironmentError as e:
            print(e)
            sys.exit()

    pmu.join()

if exec_type == "PDC":
    pdc = Pdc(pdc_id=int(pmuID), pmu_ip=pmu_ip, pmu_port=int(port))
    pdc.logger.setLevel("DEBUG")
    pdc.run()  # Connect to PMU
    try:
        header = pdc.get_header()  # Get header message from PMU
        config = pdc.get_config()  # Get configuration from PMU
    except BrokenPipeError as e:
        pdc.quit()
        sys.exit()

    pdc.start()  # Request to start sending measurements

    while True:

        data = pdc.get()  # Keep receiving data

        if type(data) == DataFrame:
            print(data.get_measurements())

        if not data:
            pdc.quit()  # Close connection
            break
