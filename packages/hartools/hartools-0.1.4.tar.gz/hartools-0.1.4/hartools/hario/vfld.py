# Class that defines the vfld data from an Harmonie-lite model like:
# tasii
# sgl40h11
# nuuk750
# qaan40h11 (runs at 00, 06, 12, 18)
#
import logging
import pandas as pd
import os
import sys
import glob
import fileinput
import datetime
import numpy as np
from collections import OrderedDict
import csv
import subprocess
import re
import csv
import logging

from typing import Tuple

logger = logging.getLogger(__name__)

class vfld(object):
    def __init__(self,  model=None, period=None, 
                 flen=None, datadir=None, stream='CARRA'):
        self.stream = stream
        self.model = model
        self.period = period.split('-')
        self.flen= flen
        self.fhours = list(range(0,flen))
        self.datadir=datadir
        ifiles_model,dates_model = self._locate_files(self.datadir,self.model,self.period,self.flen)
        self.ifiles_model=ifiles_model
        self.dates = dates_model
        #self.dates=self._get_dates_from_files(self.ifiles_model)
        data_synop, data_temp, accum_synop = self._get_data(self.ifiles_model)
        self.data_synop = data_synop
        self.data_temp = data_temp
        self.temp_stations = self._get_temp_station_list(self.data_temp)
        self.accum_synop = accum_synop

    def _get_temp_station_list(self,data_temp) -> dict:
        ''' Extract the temp stations from the first row of data
            of the temp data section of the vfld file,
            which contains: stationId lat lon height
        '''
        # check if temp data is actually there
        #
        tempStations=OrderedDict()
        for date in data_temp.keys():
            if isinstance(data_temp[date], pd.DataFrame):
                tempStations[date] = [data_temp[date].iloc[0][0],data_temp[date].iloc[0][1],
                                      data_temp[date].iloc[0][2], data_temp[date].iloc[0][3]]
            else:
                tempStations[date] = [np.nan,np.nan,np.nan,np.nan]
        return tempStations

    def _get_data(self,ifiles): -> Tuple[dict,dict,dict]
    # do something
        '''
        Extract the data from all ifiles in a df for SYNOP and TEMP data
        '''
        data_synop=OrderedDict()
        data_temp=OrderedDict()
        accum_synop =OrderedDict()
        for i,ifile in enumerate(ifiles):
            date=self.dates[i]
            data_synop[date], data_temp[date], accum_synop[date] = self._split_data(ifile)
            # print a warning if synop data is not there:
            # TODO: if no synop, don't include model!
            if len(data_synop[date]) == 0:
                logger.info("WARNING: synop data for %s[%s] is empty!"%(self.model,date))
                data_synop[date] = 'None'
            if len(data_temp[date]) == 0:
                logger.info("WARNING: temp data for %s[%s] is empty!"%(self.model,date))
                data_temp[date] = 'None'
        return data_synop, data_temp, accum_synop

    def _dtg_expected_carra(self,flen,dates) -> list:
        '''
           return dates expected to be found in the carra streams
        '''
        #init times: 00 and 12. Forecast hours expected from 0-30. Every 1h until 6, then every 3 h
        #init times: 03,06,09,15,18,21. Forecast hours expected from 0-3. Every 1h.
        fhours_long=[str(i).zfill(2) for i in range(0,7)] + [str(i).zfill(2) for i in range(9,flen,3)]
        fhours_short=[str(i).zfill(2) for i in range(0,4)]
        init_expected = [str(i).zfill(2) for i in range(0,22,3)]
        dtg_expected=[]
        for date in dates:
            for init in init_expected:
                if init in ['00', '12']:
                    for hour in fhours_long:
                        dtg_expected.append(''.join([date,init,str(hour).zfill(2)]))
                else:
                    for hour in fhours_short:
                        dtg_expected.append(''.join([date,init,str(hour).zfill(2)]))
        return dtg_expected

    def _dtg_expected_dmi(self,model,flen,dates) -> list:
        '''
           return dates expected to be found in the carra streams
        '''
        fhours=[str(i).zfill(2) for i in range(0,flen+1)]
        init_expected = [str(i).zfill(2) for i in range(0,22,3)]
        init_reduced = ['03','09','15','21']
        special_models=['tasii','db_ondemand','nk_ondemand']
        dtg_expected=[]
        for date in dates:
            if model in special_models:
                logger.info("Using tasii-like model %s for calculating expected dtgs"%model)
                for init in init_reduced:
                    for hour in fhours:
                        dtg_expected.append(''.join([date,init,str(hour).zfill(2)]))
            else:    
                logger.info("Using standard on-demand model %s for calculating expected dtgs"%model)
                for init in init_expected:
                    for hour in fhours:
                        dtg_expected.append(''.join([date,init,str(hour).zfill(2)]))
        return dtg_expected

    def _locate_files(self,datadir,model,period,flen):
        '''
        Locate the files to process from each model.
        period = YYYYMMDD_beg-YYYYMMDD_end
        Shift the file name by -3 h if the model is tasii
        '''
        date_ini=datetime.datetime.strptime(period[0],'%Y%m%d')
        date_end=datetime.datetime.strptime(period[1],'%Y%m%d')
        dates = [date_ini + datetime.timedelta(days=x) for x in range(0, (date_end-date_ini).days + 1)]
        model_dates=[datetime.datetime.strftime(date,'%Y%m%d') for date in dates]
        ifiles_model = []
        if self.stream=='CARRA':
            dtgs=self._dtg_expected_carra(flen,model_dates)
        elif self.stream=='DMI':
            dtgs=self._dtg_expected_dmi(model,flen,model_dates)
        else:
            logger.error("Stream %s unknown!"%self.stream)
            logger.error("Exiting program...")
            sys.exit()
        for dtg in dtgs:
            fname=''.join(['vfld',model,dtg])
            fdir='/'.join([datadir,model])
            ifile=os.path.join(fdir,fname)
            if os.path.exists(ifile):
                ifiles_model.append(ifile)
            else:
                ifiles_model.append('None')
        if (len(ifiles_model) == 0) or (len(set(ifiles_model)) == 1): # if all elements equal all None!
            logger.info("WARNING: no %s data found for dates %s"%(model,model_dates))
            logger.info(ifiles_model)
        logger.debug("first file for model %s: %s"%(self.model,ifiles_model[0]))
        logger.debug("last file for model %s: %s"%(self.model,ifiles_model[-1]))
        return ifiles_model, dtgs

    def _get_synop_vars(self,ifile):
        '''
        Extract information about the SYNOP variables in vfld file
        '''
        #Read this file to determine number of variables in file:
        first_two=[]
        try:
            with open(ifile,'r') as f:
                logger.debug("File %s readable"%ifile)
        except IOError:
            logger.error("ERROR: File %s exists, but I cannot read it!"%ifile)
            logger.error("I am out!")
            logger.error("TODO: Fix this")
            sys.exit()
        with open(ifile,'r') as f:
            first_two.extend(str(f.readline()).rstrip() for i in range(2))
        nsynop_vars=int(first_two[-1]) # number of variables in synop data
        ntemp_stations=int(first_two[-1]) # number of temp stations in file
        nsynop_stations,ntemp_stations,ver_file =  first_two[0].split() # number of synop stations in file
        nsynop_stations=int(nsynop_stations)
        ntemp_stations = int(ntemp_stations)
    
        lines_header =[]
        with open(ifile) as f:
                lines_header.extend(f.readline().rstrip() for i in range(nsynop_vars+2))
        lines_clean =  [re.sub('\s+',' ',i).strip() for i in lines_header]        
        vars_synop=[i.split(' ')[0] for i in lines_clean[2:]]
        accum_synop=[i.split(' ')[1] for i in lines_clean[2:]] #accumulation times. Needed to write the data at the end
        if 'FI' in vars_synop:
            colnames= ['stationId','lat','lon'] + vars_synop
            start_col_replace = 3
        else:
            colnames=['stationId','lat','lon','HH'] + vars_synop
            start_col_replace = 4
        ignore_rows = 2 + nsynop_vars # number of rows to ignore before reading the actual synop data
        return colnames, nsynop_stations, ignore_rows, ntemp_stations, accum_synop

    def _split_data(self,ifile):
        '''
        Split the data from ifile into SYNOP and TEMP
        in two data frames
        '''
        cols_temp = ['PP','FI','TT','RH','DD','FF','QQ','TD'] #this set of temp variables is constant
        header_temp=OrderedDict()
        if ifile != 'None':
            colnames, nsynop_stations, ignore_rows, ntemp_stations, accum_synop = self._get_synop_vars(ifile)
            data_synop = pd.read_csv(ifile,sep=r"\s+",engine='python',header=None,index_col=None,
                    dtype=str,skiprows=ignore_rows,nrows=nsynop_stations)
            #NOTE: will name the columns as VariableName+AccumulationTime. To be split afterwards 
            #when writing the data in vfld format for monitor in vfld_monitor
            #data_synop.columns=colnames
            if 'FI' in colnames:
                data_synop.columns=colnames[0:3]+[' '.join(str(i) for i in col) for col in zip(colnames[3:],accum_synop)]
            else:
                data_synop.columns=colnames[0:4]+[' '.join(str(i) for i in col) for col in zip(colnames[4:],accum_synop)]
            ignore_temp=ignore_rows+data_synop.shape[0]+10
            data_temp =  pd.read_csv(ifile,sep=r"\s+",engine='python',header=None,index_col=None,names=cols_temp,
                                      dtype=str,skiprows=ignore_temp)
        else:
            data_synop = 'None'
            data_temp = 'None'
            accum_synop = 'None'
        return data_synop, data_temp, accum_synop

class vfld_monitor(object):
    '''
        Take dataframe with vfld data and format the
        rows and columns to write the whole thing to 
        a standard vfld ascii file that monitor can read
    '''

    def __init__(self, model=None, date=None,df_synop=None, df_temp=None, outdir=None):
        self.model = model #model to name the vfld file
        self.date=date
        self.df_synop = df_synop # pandas dataframe with synop data
        self.df_temp = df_temp # pandas dataframe with temp data
        self.outdir = outdir
        self.synop_cols = self.df_synop.columns
        self.df_out = self._format_data(df_synop,df_temp)
        
    def _format_data(self,df_synop,df_temp):
        '''
        Format the data to write in monitor vfld format.
        First create a dummy set of column names with the 
        same length as the length of the synop data.
        Then put below the info about
        ns_synop ns_temp version_4
        number_of_vars_synop
        list of vars from synop
        synopdata
        header temp
        temp data
        '''
        colst = df_temp.columns
        colss = df_synop.columns
        ns_synop = df_synop.shape[0]
        #to figure out the number of stations in the concat temp dataframe,
        # get the rows with index == 0, since only on the first line of the 
        # original temp dataframes this information existed
        # Each new set of data will start at 0. 
        # NOTE: This seems to work only with non overlappping data sets!
        #ns_temp = len(df_temp[df_temp.index.values == 0])

        #alternative: since I read all in string format, only the 
        #strings not containing a . will be station names in the PP column
        temp_stations_PP=[st for st in df_temp['PP'].values if '.' not in st]
        ns_temp = len(temp_stations_PP)

        #declaring these values for header as strings is the only way I can ensure these numbers are written as non-float
        header_synop=[str(ns_synop), str(ns_temp), str(4)]
        df_out=pd.DataFrame(columns=colss) 
        if 'FI 0' in colss:
            nvars_synop = df_synop.shape[1]-3 # subtract: stationId,lat,lon
            varlist_synop=colss[3:]  
            nvars=len(colss[3:])
        else:
            nvars_synop = df_synop.shape[1]-4 #subtract stationId,lat,lon,hh
            varlist_synop=colss[4:]  
            nvars=len(colss[4:])
        #write first line of file:    
        df_out=df_out.append({'stationId':header_synop[0],'lat':header_synop[1],'lon':header_synop[2]},ignore_index=True)
        df_out=df_out.append({'lat':str(nvars)},ignore_index=True)
        for var in varlist_synop:
            df_out = df_out.append({'stationId':var},ignore_index=True)
        df_out = df_out.append(df_synop,ignore_index=True)    
        if self.model in ['carra','carra_beta1','carra_beta2','carra_rc1']:
            logger.debug("carra or carra branch (%s): Setting pressure levels to 10"%self.model)
            df_out = df_out.append({'stationId':str(10)},ignore_index=True) #10 pressure levels for carra (constant)
        else:
            df_out = df_out.append({'stationId':str(11)},ignore_index=True) #11 pressure levels (constant)
        df_out = df_out.append({'stationId':str(8)},ignore_index=True) #8 variables for temp profiles (constant)
        for var in colst:
            df_out = df_out.append({'stationId':var+' 0'},ignore_index=True) #include accumulation time for temp vars
        #fill_these = ['stationId', 'lat', 'lon', 'FI', 'NN', 'DD', 'FF', 'TT']
        fill_these = self.synop_cols[0:8]
        #df_temp = df_temp.fillna(value=pd.np.nan, inplace=True) #get rid of None?
        for i in enumerate(df_temp['PP'].values):
            collect_dict=OrderedDict()
            for k,col in enumerate(colst):
                collect_dict[fill_these[k]] = df_temp[col].values[i[0]]
            #for col in self.synop_cols[8:]:
            #    collect_dict[col] = ''   
            df_out = df_out.append(collect_dict,ignore_index=True)
        for col in df_out.columns:
            df_out[col].replace('None', '', inplace=True)
        return df_out


    def write_vfld(self):
        ofile=os.path.join(self.outdir,''.join(['vfld',self.model,self.date]))
        #the extra QUOTE_NONE is to avoid using extra "" in output for var names, and the escapechar 
        #so it won't complain about no escapechar unset
        self.df_out.to_csv(ofile,sep=' ',header=False,index=False,na_rep='',quoting=csv.QUOTE_NONE,quotechar='',escapechar=' ')


if __name__ == '__main__':
    models=[]
    model='tasii'
    period='20190601-20190601'
    flen=52
    datadir='/data/cap/code_development_hpc/scripts_verif/merge_scripts/merge_vfld/example_data'
    #datadir='/netapp/dmiusr/aldtst/vfld'
    tasii = vfld(model=model, period=period, flen=52, datadir=datadir)
    sgl40h11 = vfld(model='sgl40h11', period=period, flen=52, datadir=datadir)
    qaan40h11 = vfld(model='qaan40h11', period=period, flen=52, datadir=datadir)
    #models=[tasii, sgl40h11, nuuk750, qaan40h11]
    models=[tasii, sgl40h11, qaan40h11]
    date=tasii.dates[0]
    frames_synop = [f for f in models if isinstance(f.data_synop[date],pd.DataFrame)]
    frames_temp = [f for f in models if isinstance(f.data_temp[date],pd.DataFrame)]
    dfs=[f.data_synop[date] for f in frames_synop]
    dft=[f.data_temp[date] for f in frames_temp]
    df_synop = pd.concat(dfs,sort=False)
    df_temp = pd.concat(dft)
    mon_save= vfld_monitor(model='gl',date=date,df_synop=df_synop,df_temp=df_temp,outdir=datadir)
    mon_save.write_vfld()

