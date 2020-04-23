from django.conf import settings

import numpy as np
import pandas as pd
from pandas import ExcelWriter
import pickle


from rest_framework import viewsets
from rest_framework.response import Response


class ProductPredictionsViewSet(viewsets.ViewSet):
    def list(self, request):
        dct_inputs = {}
        ret_status = ''
        ret_dct = {'status': ret_status}
        ret_dct = {}
        if self.request.query_params.get('frghtgrp') is None :
            ret_dct['status'] = 'Invalid data passed.'
            ret_dct['data'] = ''
            return Response(ret_dct)
        else:
            if self.request.query_params.get('frghtgrp') == '':
                ret_dct['status'] = 'Invalid data passed.'
                ret_dct['data'] = ''
                return Response(ret_dct)
            print(self.request.query_params.get('frghtgrp'))
            dct_inputs['Freight Grp'] = self.request.query_params.get('frghtgrp')

        if self.request.query_params.get('matgrp') is None:
            ret_dct['status'] = 'Invalid data passed.'
            ret_dct['data'] = ''
            return Response(ret_dct)
        else:
            if self.request.query_params.get('matgrp') == '':
                ret_dct['status'] = 'Invalid data passed.'
                ret_dct['data'] = ''
                return Response(ret_dct)
            dct_inputs['Mat Grp'] = self.request.query_params.get('matgrp')
        if self.request.query_params.get('extmatgrp') is None:
            ret_dct['status'] = 'Invalid data passed.'
            ret_dct['data'] = ''
            return Response(ret_dct)
        else:
            if self.request.query_params.get(('extmatgrp')) == '':
                ret_dct['status'] = 'Invalid data passed.'
                ret_dct['data'] = ''
                return Response(ret_dct)
            dct_inputs['Ext Mat Grp'] = self.request.query_params.get('extmatgrp')

        if self.request.query_params.get('memo') is None:
            ret_dct['status'] = 'Invalid data passed.'
            ret_dct['data']
            return Response(ret_dct)
        else:
            if self.request.query_params.get('memo')=='':
                ret_dct['status'] = 'Invalid data passed.'
                ret_dct['data'] = ''
                return Response(ret_dct)
            dct_inputs['Memo'] = self.request.query_params.get('memo')

        if self.request.query_params.get('Hierarchy') is None:
            ret_dct['status'] = 'Invalid data passed.'
            ret_dct['data'] = ''
            return Response(ret_dct)
        else:
            if self.request.query_params.get('Hierarchy')=='':
                ret_dct['status'] = 'Invalid data passed.'
                ret_dct['data'] = ''
                return Response(ret_dct)
            dct_inputs['Hierarchy'] = self.request.query_params.get('Hierarchy')
        #print(dct_inputs)
        model_files = settings.PICKLE_FILES_URL
        file_loc = settings.TEMP_FILE_LOC
        output_loc = settings.OUTPUT_FILES

        model = pickle.load(open(rf'{model_files}\model.pkl', 'rb'))

        freightGrp = pickle.load(open(rf'{model_files}\FreightGrp.pkl', 'rb'))
        matGrp = pickle.load(open(rf'{model_files}\MatGrp.pkl', 'rb'))
        extMatGrp = pickle.load(open(rf'{model_files}\ExtMatGrp.pkl', 'rb'))
        memo = pickle.load(open(rf'{model_files}\Memo.pkl', 'rb'))
        hierarchy = pickle.load(open(rf'{model_files}\Hierarchy.pkl', 'rb'))
        # df = pd.read_excel(rf'{file_loc}\New.xlsx')
        df = pd.DataFrame([list(dct_inputs.values())],columns = ['Freight Grp', 'Mat Grp', 'Ext Mat Grp', 'Memo', 'Hierarchy'])
        df.iloc[0] = list(dct_inputs.values())
        df = df.dropna()
        data = pd.DataFrame(dct_inputs.items())
        data = data.dropna()
        df.replace(freightGrp, inplace=True)
        df.replace(extMatGrp, inplace=True)
        df.replace(matGrp, inplace=True)
        df.replace(memo, inplace=True)
        df.replace(hierarchy, inplace=True)
        df = df.replace(regex='([a-zA-Z])', value=0)
        #print(df.columns)
        result = model.predict(df)
        prob = model.predict_proba(df)

        Maxprob = prob.max(axis=1) * 100
        #data['HTS Code'] = result.tolist()
        #data['Probability'] = Maxprob.tolist()
        #dct_inputs['data'] = Maxprob.tolist()
        #print(Maxprob.tolist())
        #data.to_excel(writer, 'Sheet1')
        #writer.save()
        #writer = ExcelWriter(rf'{output_loc}\\PythonExport.xlsx')"""
        #ret_dct['file_loc'] = rf'{output_loc}\PythonExport.xlsx'
        # data.to_excel(r'C:\Users\Abhinav Abhishek\Desktop\Heruku-Demo-master', index = False)
        dct_inputs['Probability'] = Maxprob.tolist()[0]
        ret_dct['status'] = 'success'
        ret_dct['data'] = dct_inputs
        return Response(ret_dct)


