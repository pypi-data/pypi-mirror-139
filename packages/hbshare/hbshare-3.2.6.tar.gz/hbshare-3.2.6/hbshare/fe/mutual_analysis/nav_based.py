import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import  functionality


localdb=db_engine.PrvFunDB().engine
hbdb=db_engine.HBDB()
util=functionality.Untils()


def get_monthly_jjnav(jjdm):

    #get the nav ret  for given jjdm and time zone(already times 100)
    sql="select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm ='{0}' and rq1y!=99999  "\
        .format(jjdm)
    navdf=hbdb.db2df(sql, db='funduser')

    max_yearmonth=navdf['tjyf'].max()
    min_yearmonth=navdf['tjyf'].min()

    return navdf,max_yearmonth,min_yearmonth

def get_daily_jjnav(jjdm_list,start_date=None,end_date=None):

    jjdm_con=util.list_sql_condition(jjdm_list)

    sql="select jjdm,jzrq,hbdr from st_fund.t_st_gm_rhb where jjdm in ({0}) and hbdr!=99999 and hbdr!=0  "\
        .format(jjdm_con)
    navdf=hbdb.db2df(sql, db='funduser')

    return navdf

def get_monthly_index_ret(zqdm,start_date=None,end_date=None):

    sql="select zqdm,tjyf,rqzh,hb1y from st_market.t_st_zs_yhb where zqdm='{0}' and abs(hb1y)!=99999 "\
        .format(zqdm)

    benchmark_ret=hbdb.db2df(sql, db='alluser')

    return  benchmark_ret

def bhar(arr):
        return 100*(np.power(np.cumprod((arr+100)/100).tolist()[-1],1/12)-1)

def ols_for_group(arr):

    y_col=arr.columns[0]
    x_col=arr.columns.tolist()
    x_col.remove(y_col)

    return util.my_general_linear_model_func(arr[x_col].values,
                                      arr[y_col].values)['x'].tolist()

def get_barra_daily_ret(start_date=None,end_date=None):
    #barra return daily return
    sql='select factor_ret,factor_name,trade_date from st_ashare.r_st_barra_factor_return'
    test=hbdb.db2df(sql,db='alluser')
    factor_name_list=test['factor_name'].unique().tolist()
    factor_ret_df=pd.DataFrame()
    date_list=test['trade_date'].unique().tolist()
    date_list.sort()
    factor_ret_df['date']=date_list
    for factor in factor_name_list:
        factor_ret_df=pd.merge(factor_ret_df,test[test['factor_name']==factor][['factor_ret','trade_date']],
                               how='left',left_on='date',right_on='trade_date').drop('trade_date',axis=1)
        factor_ret_df.rename(columns={'factor_ret':factor},inplace=True)

    return factor_ret_df

def get_styleindex_ret(index_list,start_date=None,end_date=None):

    # style daily return
    style_ret=pd.DataFrame()
    for zqdm in index_list:

        sql = "select spjg,zqmc,jyrq from st_market.t_st_zs_hqql where zqdm='{}' ".format(zqdm)
        # sql= "select zqdm,jyrq,hbdr from st_market.t_st_zs_rhb where zqdm='{}' ".format(zqdm)
        test = hbdb.db2df(sql=sql, db='alluser')
        test['ret'] = test['spjg'].pct_change()
        test[zqdm]=test['ret']
        test.set_index('jyrq',inplace=True)
        style_ret=pd.concat([style_ret,test[zqdm]],axis=1)

    return style_ret

def get_jj_daily_ret(jjdm_list):

    tempdf = get_daily_jjnav(jjdm_list)
    jj_ret = pd.DataFrame()
    jj_ret['date'] = tempdf.sort_values('jzrq')['jzrq']
    for jjdm in tempdf['jjdm'].unique():
        jj_ret=pd.merge(jj_ret,tempdf[tempdf['jjdm']==jjdm][['hbdr','jzrq']],
                        how='left',left_on='date',right_on='jzrq').drop('jzrq',axis=1)
        jj_ret.rename(columns={'hbdr':jjdm},inplace=True)
        jj_ret[jjdm]=jj_ret[jjdm]/100

    jj_ret.set_index('date',drop=True,inplace=True)

    return jj_ret

class Scenario_return:
    @staticmethod
    def get_histroy_scenario_ret():
        benchmark_ret=get_monthly_index_ret('000002')
        benchmark_ret['med']=99999
        benchmark_ret['scenario'] = ''
        for i in range(1,len(benchmark_ret)):
            benchmark_ret.loc[i,'med']=benchmark_ret.loc[0:i-1]['hb1y'].median()
            if(benchmark_ret.loc[i,'med']>=benchmark_ret.loc[i,'hb1y']):
                benchmark_ret.loc[i, 'scenario']='opt'
            else:
                benchmark_ret.loc[i, 'scenario'] = 'pes'

        return  benchmark_ret[['scenario','hb1y','tjyf','rqzh']]

    @staticmethod
    def pessimistic_ret(jjdm,benchmark_ret):

        navdf,max_yearmonth,min_yearmonth=get_monthly_jjnav(jjdm)

        navdf=pd.merge(navdf,benchmark_ret,how='left',on='tjyf')

        navdf['ext_ret']=navdf['hb1y_x']-navdf['hb1y_y']
        navdf.rename(columns={'rqzh_y':'rqzh'},inplace=True)

        #last 12 month average month return by calculating last 12 month cul ret and turn it into month return

        temp=navdf[navdf['scenario']=='pes']['ext_ret'].rolling(12).apply(bhar)
        temp=temp.to_frame('pes_ext_ret')
        navdf=pd.merge(navdf,temp,how='left',left_index=True, right_index=True)

        temp=navdf[navdf['scenario']=='opt']['ext_ret'].rolling(12).apply(bhar)
        temp=temp.to_frame('opt_ext_ret')
        navdf=pd.merge(navdf,temp,how='left',left_index=True, right_index=True)

        navdf['ext_ret'] = navdf['ext_ret'].rolling(12).apply(bhar)


        last_pes_ret=np.nan
        last_opt_ret=np.nan

        for i in range(0,len(navdf)):
            if(navdf.loc[i]['pes_ext_ret']==navdf.loc[i]['pes_ext_ret']):
                last_pes_ret=navdf.loc[i]['pes_ext_ret']

            else:
                navdf.loc[i,'pes_ext_ret']=last_pes_ret

            if(navdf.loc[i]['opt_ext_ret']==navdf.loc[i]['opt_ext_ret']):
                last_opt_ret=navdf.loc[i]['opt_ext_ret']

            else:
                navdf.loc[i,'opt_ext_ret']=last_opt_ret

        navdf=navdf[navdf['ext_ret'].notnull()]

        # for col in['ext_ret','pes_ext_ret','opt_ext_ret']:
        #     navdf[col] = (navdf[col]/100).astype(float).map("{:.2%}".format)

        return navdf[['jjdm','tjyf','rqzh','ext_ret','pes_ext_ret','opt_ext_ret']]

    @staticmethod
    def factorlize_ret(factor_name,fre='M'):

        sql="select * from scenario_ret"
        raw_df=pd.read_sql(sql,con=localdb)

        raw_df.rename(columns={'rqzh':'date'},inplace=True)
        raw_df=raw_df[raw_df[factor_name].notnull()]


        if(fre=='Q'):
            raw_df = raw_df[(raw_df['tjyf'].astype(str).str[4:6] == '03') | (raw_df['tjyf'].astype(str).str[4:6] == '06') | (
                        raw_df['tjyf'].astype(str).str[4:6] == '09') | (raw_df['tjyf'].astype(str).str[4:6] == '12')]
        elif(fre=='HA'):
            raw_df = raw_df[(raw_df['tjyf'].astype(str).str[4:6] == '06') | (raw_df['tjyf'].astype(str).str[4:6] == '12')]


        return raw_df


class Style_exp:


    def __init__(self,asofdate,fre='Q',start_date=None,end_date=None):
        self.jjdm_list=util.get_mutual_stock_funds(asofdate)
        self.get_style_exp(self.jjdm_list,fre,start_date,end_date)

    @staticmethod
    def get_style_exp(jjdm_list,fre,start_date=None,end_date=None):

        value_col = ['399370', '399371']
        size_col=['399314','399315','399316']

        #get value index ret :
        style_index_ret=get_styleindex_ret(value_col+size_col)

        if(fre=='M'):
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = [str(x)[0:6] for x in olsdf.index]
                return olsdf
        elif(fre=='Q'):
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = ''
                olsdf.loc[olsdf.index.astype(str).str[4:6]<='03','yearmonth']='Q1'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '06')&(olsdf.index.astype(str).str[4:6] > '03'), 'yearmonth'] = 'Q2'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '09')&(olsdf.index.astype(str).str[4:6] > '06'), 'yearmonth'] = 'Q3'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '12')&(olsdf.index.astype(str).str[4:6] > '09'), 'yearmonth'] = 'Q4'
                olsdf['yearmonth']=olsdf.index.astype(str).str[0:4]+olsdf['yearmonth']

                return olsdf


        for jjdm in jjdm_list:

            #get jj nav ret
            jj_ret=get_jj_daily_ret([jjdm])

            olsdf = pd.merge(jj_ret, style_index_ret, how='inner', left_index=True, right_index=True)

            olsdf=timezone_transform(olsdf)

            value_exp_df=pd.DataFrame()
            tempdf=olsdf[olsdf[[jjdm]+value_col].notnull().sum(axis=1)==(len(value_col)+1)]
            tempdf=tempdf.groupby('yearmonth')[[jjdm]+value_col].apply(ols_for_group).to_frame('exp')
            i=0
            for col in value_col:
                tempdf[col]=[x[i] for x in tempdf['exp']]
                i+=1
            tempdf.drop('exp',inplace=True,axis=1)
            value_exp_df=pd.concat([value_exp_df,tempdf],axis=1)

            size_exp_df=pd.DataFrame()
            tempdf=olsdf[olsdf[[jjdm]+size_col].notnull().sum(axis=1)==(len(size_col)+1)]
            tempdf=tempdf.groupby('yearmonth')[[jjdm]+size_col].apply(ols_for_group).to_frame('exp')
            i=0
            for col in size_col:
                tempdf[col]=[x[i] for x in tempdf['exp']]
                i+=1
            tempdf.drop('exp',inplace=True,axis=1)
            size_exp_df=pd.concat([size_exp_df,tempdf],axis=1)

            print('jj {} Done'.format(jjdm))

        value_exp_df.to_sql('value_exposure',index=False,if_exists='append',con=localdb)
        size_exp_df.to_sql('size_exposure', index=False, if_exists='append',con=localdb)


if __name__ == '__main__':

    #calculate the return for different scenarios

    # stock_jjdm_list=util.get_mutual_stock_funds('20211231')
    # stock_jjdm_list.sort()
    # benchmark_ret = get_histroy_scenario_ret()
    # saved_df=pd.DataFrame()
    # for jjdm in stock_jjdm_list:
    #     scenario_ret=pessimistic_ret(jjdm,benchmark_ret)
    #     saved_df=pd.concat([saved_df,scenario_ret],axis=0)
    # saved_df.to_sql('scenario_ret',index=False,con=localdb,if_exists='append')

    #barra return daily return

    #factor_ret_df=get_barra_daily_ret()
    # factor_ret_df['year_month']=factor_ret_df['date'].str[0:6]

    # cordf=factor_ret_df.copy()

    se=Style_exp('20211231')

    # style_ret=pd.DataFrame()
    # #style daily return
    # for zqdm in ['399372','399373','399374','399375','399376','399377','399314','399315','399316','399370','399371']:
    #
    #     sql = "select spjg,zqmc,jyrq from st_market.t_st_zs_hqql where zqdm='{}' ".format(zqdm)
    #     # sql= "select zqdm,jyrq,hbdr from st_market.t_st_zs_rhb where zqdm='{}' ".format(zqdm)
    #     test = hbdb.db2df(sql=sql, db='alluser')
    #     test['ret'] = test['spjg'].pct_change()
    #     test[zqdm]=test['ret']
    #     test.set_index('jyrq',inplace=True)
    #     style_ret=pd.concat([style_ret,test[zqdm]],axis=1)
    #
    # tempdf=get_daily_jjnav(['001856'])
    # jj_ret=pd.DataFrame()
    # jj_ret['date']=tempdf.sort_values('jzrq')['jzrq']
    #
    # for jjdm in tempdf['jjdm'].unique():
    #     jj_ret=pd.merge(jj_ret,tempdf[tempdf['jjdm']==jjdm][['hbdr','jzrq']],
    #                     how='left',left_on='date',right_on='jzrq').drop('jzrq',axis=1)
    #     jj_ret.rename(columns={'hbdr':jjdm},inplace=True)
    #     jj_ret[jjdm]=jj_ret[jjdm]/100
    #
    # jj_ret.set_index('date',drop=True,inplace=True)
    # olsdf=pd.merge(jj_ret,style_ret,how='inner',left_index=True,right_index=True)


    #monthly
    #olsdf['yearmonth'] = [str(x)[0:6] for x in olsdf.index]

    #quarterly
    # olsdf['yearmonth'] = ''
    # olsdf.loc[olsdf.index.astype(str).str[4:6]<='03','yearmonth']='Q1'
    # olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '06')&(olsdf.index.astype(str).str[4:6] > '03'), 'yearmonth'] = 'Q2'
    # olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '09')&(olsdf.index.astype(str).str[4:6] > '06'), 'yearmonth'] = 'Q3'
    # olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '12')&(olsdf.index.astype(str).str[4:6] > '09'), 'yearmonth'] = 'Q4'
    # olsdf['yearmonth']=olsdf.index.astype(str).str[0:4]+olsdf['yearmonth']

    # plot=functionality.Plot(2000,2000)
    #
    # for x_col in [['399372','399373','399374','399375','399376','399377'],
    #               ['399314','399315','399316','399370','399371'],['399314','399315','399316'],
    #               ['399370', '399371'] ]:
    #
    #
    #     tempdf=olsdf.groupby('yearmonth')[['001856']+x_col].apply(ols_by_month).to_frame('exp')
    #     i=0
    #     for col in x_col:
    #         tempdf[col]=[x[i] for x in tempdf['exp']]
    #         i+=1
    #     tempdf.drop('exp',inplace=True,axis=1)
    #     plot.plotly_line_style(tempdf,'asdf')


