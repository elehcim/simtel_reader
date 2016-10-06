import pyhessio
import argparse
import sys
import numpy as np
np.set_printoptions(formatter={'float_kind':lambda x: "%.2f" % x})

def parse_args():
    # Declare and parse command line option
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', dest='filename', required=True, help='simtelarray data file name')
    parser.add_argument('-l', dest='limit', type=int, required=False, default=0, help='Max number of events to read')
    parser.add_argument('--tel', type=int, nargs="+", required=True, help='telescope ids')
    return parser.parse_args()

class SimtelReader(object):
   

    def __init__(self, file_name, tel_id, limit=0):
        assert(isinstance(tel_id, (list, tuple)))
        self.evtnum = list()
        self.ntrigtel = list()
        self.runnum = list()
        self.mcevtnum = list()
        self.mcrunnum = list()
        self.e0 = list()
        self.zd = list()
        self.az = list()
        self.sh_zd = list()
        self.sh_az = list()  # shower azimuth (N->E)
        self.xcore = list()
        self.ycore = list()

        self.teltrg_list = list()
        self.teltrg_time = list()

        self.file_name = file_name
        self.tel_id = tel_id
        self.limit = limit

    def read_data(self):
        print("Reading file", self.file_name)
        assert pyhessio.file_open(self.file_name) == 0
        cter = {k: v for (k, v) in zip(self.tel_id, np.zeros_like(self.tel_id))}
        evt_counter = 1
        for run_id, event_id in pyhessio.move_to_next_event(limit=self.limit):
            if evt_counter == 1:  # only the first time
                print("Number of simulated telescopes: %i" % pyhessio.get_num_telescope())
            print("Run ID: %s, Event ID: %s" % (run_id, event_id))
            tel_ids = pyhessio.get_teldata_list()
            print("  Telescopes (%2i) for which we have data: %s" % (pyhessio.get_num_teldata(), tel_ids))
            # print("  teltrg_list:                            %s" % (pyhessio.get_central_event_teltrg_list()))  # same as get_num_teldata
            print("  teltrg_time (ns):                       %s" % (pyhessio.get_central_event_teltrg_time()))  # Comment if https://github.com/cta-observatory/pyhessio/pull/36 not merged 
            
            evt_counter += 1
            if evt_counter % 100 == 0:  # Print only each 100 events
                print("--< Reading Event", evt_counter, ">--", end="\r")
            for t in self.tel_id:
                if t in tel_ids:
                    cter[t] += 1

            self.ntrigtel.append(pyhessio.get_num_tel_trig())
            self.mcevtnum.append(event_id)
            self.mcrunnum.append(run_id)
            self.e0.append(pyhessio.get_mc_shower_energy())
            shower_ze = float(90)-np.rad2deg(pyhessio.get_mc_shower_altitude())
            shower_az = np.rad2deg(pyhessio.get_mc_shower_azimuth())
            self.sh_zd.append(shower_ze)
            self.sh_az.append(shower_az)

            # tel_az, tel_el = pyhessio.get_pointing()
            # float(90)-np.rad2deg(tel_el)
            tel_ze = 20  # HARDCODED
            tel_az = 0   # HARDCODED
            self.zd.append(tel_ze)
            self.az.append(tel_az)
            self.xcore.append(pyhessio.get_mc_event_xcore())
            self.ycore.append(pyhessio.get_mc_event_ycore())

            self.xcore.append(pyhessio.get_mc_event_xcore())
            self.teltrg_list.append(pyhessio.get_central_event_teltrg_list())
            self.teltrg_time.append(pyhessio.get_central_event_teltrg_time())  # Comment if https://github.com/cta-observatory/pyhessio/pull/36 not merged 

        print("")
        for t in self.tel_id:
            print("Read %i events, of which triggered by tel %i: %i" %
                 (evt_counter, t, cter[t]), flush=True)
        pyhessio.close_file()


def main():
    args = parse_args()
    simtel = SimtelReader(args.filename, args.tel, args.limit)
    simtel.read_data()
    # print(simtel.teltrg_list)
    # print(simtel.teltrg_time)

if __name__ == '__main__':
    sys.exit(main())
