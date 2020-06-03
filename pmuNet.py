from synchrophasor.frame import *
from synchrophasor.pmu import Pmu
from synchrophasor.pdc import Pdc
from synchrophasor.frame import DataFrame


def runPMU():
    pmu = Pmu(ip="127.0.0.1", port=1410)

    pmu.set_configuration()  # This will load default PMU configuration specified in IEEE C37.118.2 -Annex D (Table D.2)
    pmu.set_header()  # This will load default header message "Hello I'm tinyPMU!"

    pmu.run()  # PMU starts listening for incoming connections

    while True:
        if pmu.clients:  # Check if there is any connected PDCs
            pmu.send(pmu.ieee_data_sample)  # Sending sample data frame specified in IEEE C37.118.2 -Annex D (Table D.1)

    pmu.join()


def runPDC(pdcID, ip, port):
    pdc = Pdc(pdc_id=pdcID, pmu_ip=ip, pmu_port=port)
    pdc.logger.setLevel("DEBUG")
    pdc.run()  # Connect to PMU

    header = pdc.get_header()  # Get header message from PMU
    config = pdc.get_config()  # Get configuration from PMU

    pdc.start()  # Request to start sending measurements

    while True:
        data = pdc.get()  # Keep receiving data

        if type(data) == DataFrame:
            print(data.get_measurements())

        if not data:
            pdc.quit()  # Close connection
            break
