import pyhessio
import argparse
import sys
import collections
import numpy as np
from astropy.table import Table 

def parse_args():
    # Declare and parse command line option
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', dest='filename', required=True, help='simtelarray data file name')
    parser.add_argument('-l', dest='limit', type=int, required=False, default=0, help='Max number of events to read')
    parser.add_argument('--tel', type=int, nargs="+", required=True, help='telescope ids')
    return parser.parse_args()

class TelData():
    """docstring for TelData"""
    def __init__(self, tel_id):
        self.tel_id = tel_id

class SimtelReader(object):
   

    def __init__(self, file_name, tel_id, limit=0):
        assert(isinstance(tel_id, (list, tuple)))
        self.evtnum = list()
        self.ntrigtel = list()
        self.runnum = list()
        self.mcprim = list()
        self.mcevtnum = list()
        self.mcrunnum = list()
        self.e0 = list()
        self.zd = list()
        self.az = list()
        self.sh_zd = list()
        self.sh_az = list()  # shower azimuth (N->E)
        self.xcore = list()
        self.ycore = list()
        self.xscrpos = list()
        self.yscrpos = list()
        self.hint = list()

        self.teltrg_list = list()
        self.teltrg_time = list()
        # self.tel = collections.OrderedDict()
        self.file_name = file_name
        self.tel_id = tel_id
        self.limit = limit
        # for t in tel_id:
        #     self.tel[t] = TelData(t)
        #     self.tel[t].nevt = 0
        print("Reading file", file_name)
        assert pyhessio.file_open(file_name) == 0
        trg_events = 1
        # event independent info
        for run_id, event_id in pyhessio.move_to_next_event(limit=limit):
            tel_ids = pyhessio.get_teldata_list()
            # print(tel_ids)
            # if trg_events == 1:  # Only once per telescope
            #     for t in tel_id:
            #         self.tel[t].telx, self.tel[t].tely, self.tel[t].telz = pyhessio.get_telescope_position(t)
            #         self.tel[t].camflen = pyhessio.get_optical_foclen(t) * 1000.0
            #         self.tel[t].ntel = pyhessio.get_num_telescope()
            trg_events += 1
            # for t in tel_id:
            #     if t in tel_ids:
            #         self.tel[t].nevt += 1
        pyhessio.close_file()
        print("Overall triggered events =", trg_events)
        # Preallocating
        # for t in tel_id:
        #     print("tel %d: nevt = %d" % (t, self.tel[t].nevt))
        #     nevt = self.tel[t].nevt
        #     self.tel[t].evtnum = np.empty(nevt, dtype=np.int32)
        #     self.tel[t].ntrigtel = np.empty(nevt, dtype=np.int32)
        #     self.tel[t].runnum = np.empty(nevt, dtype=np.int32)
        #     self.tel[t].gps_time_s = np.empty(nevt, dtype=np.uint64)
        #     self.tel[t].gps_time_ns = np.empty(nevt, dtype=np.uint64)


    def read_data(self):
        assert pyhessio.file_open(self.file_name) == 0
        cter = {k: v for (k, v) in zip(self.tel_id, np.zeros_like(self.tel_id))}
        evt_counter = 1
        for run_id, event_id in pyhessio.move_to_next_event(limit=self.limit):
            print("Run ID: %s, Event ID: %s" % (run_id, event_id))
            print("  Number of simulated telescopes: %i" % pyhessio.get_num_telescope())
            # print("Number of telescope for which we have data: %i" % pyhessio.get_num_teldata())
            tel_ids = pyhessio.get_teldata_list()
            print("  Telescopes (%2i) for which we have data: %s" % (pyhessio.get_num_teldata(), tel_ids))

            evt_counter += 1
            if evt_counter % 100 == 0:  # Print only each 100 events
                print("--< Reading Event", evt_counter, ">--", end="\r")
            for t in self.tel_id:
                if t in tel_ids:
            #         self.tel[t].evtnum[cter[t]] = event_id
            #         self.tel[t].ntrigtel[cter[t]] = pyhessio.get_num_tel_trig()
            #         self.tel[t].runnum[cter[t]] = run_id
            #         self.tel[t].gps_time_s[cter[t]] = pyhessio.get_tel_event_gps_time(t)[0]
            #         self.tel[t].gps_time_ns[cter[t]] = pyhessio.get_tel_event_gps_time(t)[1]
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
            self.teltrg_time.append(pyhessio.get_central_event_teltrg_time())

        print("")
        for t in self.tel_id:
            print("Read %i events, of which triggered by tel %i: %i" %
                 (evt_counter, t, cter[t]), flush=True)
        pyhessio.close_file()


    def __iter__(self):
        # allow iterating over item names
        return (k for k in self.__dict__.keys() if not (k.startswith("_") or k is "tel"))

    # def as_dict(self):
    #     '''Creates a dictionary of Container items unrolling recursively
    #     nested containers.'''
    #     d = dict()
    #     for k, v in self.items():
    #         if isinstance(v, Container):
    #             d[k] = v.as_dict()
    #             continue
    #         d[k] = v
    #     return d

    def items(self):
        '''Iterate over pairs of key, value. Just like the dictionary method'''
        # allow iterating over item names
        return ((k, v) for k, v in self.__dict__.items()
                if not(k.startswith('_') or k is "tel"))

    def to_table(self):
        names = [i.upper() for i in self]
        # dtype = [v.dtype for _, v in self.items()]
        data = [v for _, v in self.items()]

        # It depends on chunking syntax:
        # data = [v for _, v.chunk in self.items()]

        print(len(names), names)
        print(len(data), data)
        return Table(data=data,
                     names=names)
                     # dtype=dtype,
                     # meta=self.meta.as_dict())
def main():
    args = parse_args()
    simtel = SimtelReader(args.filename, args.tel, args.limit)
    simtel.read_data()
    print(simtel.mcrunnum)
    print(simtel.teltrg_list)
    print(simtel.teltrg_time)

if __name__ == '__main__':
    sys.exit(main())
