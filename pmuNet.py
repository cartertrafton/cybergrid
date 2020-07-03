from synchrophasor.frame import *
from synchrophasor.pmu import Pmu
from synchrophasor.pdc import Pdc
from synchrophasor.frame import DataFrame
import sys

exec_type, pmuID, pmu_ip, port, buffer_size, setTS = sys.argv[1:7]

if exec_type == "PMU":
    pmu = Pmu(pmu_id=int(pmuID), port=int(port), ip=pmu_ip, buffer_size=int(buffer_size), set_timestamp=setTS)

    pmu.set_configuration()  # This will load default PMU configuration specified in IEEE C37.118.2 -Annex D (Table D.2)
    pmu.set_header()

    pmu.run()  # PMU starts listening for incoming connections
    # setPDC(pmuID,pmu_ip,port)
    while True:
        if pmu.clients:  # Check if there is any connected PDCs
            pmu.send_data(pmu.dynamic_data_sample)  # Sending sample data frame specified in IEEE C37.118.2 -Annex D (Table D.1)

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
