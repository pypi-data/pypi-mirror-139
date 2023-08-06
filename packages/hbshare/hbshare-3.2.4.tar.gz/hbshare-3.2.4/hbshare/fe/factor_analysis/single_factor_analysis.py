import numpy as np
import pandas as pd
from hbshare.fe.XZ import db_engine as dbeng
from hbshare.fe.XZ import functionality
from hbshare.fe.mutual_analysis import holdind_based
from hbshare.fe.mutual_analysis import nav_based as nbs
import datetime

until=functionality.Untils()
hbdb=dbeng.HBDB()
fre_map={'M':'2101','Q':'2103','HA':'2106'}

def bhar(arr):
    return np.cumprod((arr/100+1)).values[-1]

def grouping(df,pic_title,fre):

    df['date']=df['date'].astype(str)
    # fre_code=fre_map[fre]
    draw_df=pd.DataFrame()
    df=df.sort_values('date')
    draw_df['date']=df['date'].unique()
    ret_list=[[],[],[],[],[]]
    for i in range(len(draw_df)):
        date=draw_df.iloc[i]['date']
        tempdf=df[df['date']==date].groupby('group').mean()
        for j in range(5):
            ret_list[j].append(tempdf.loc[j]['zbnp'])

    # data_con=until.list_sql_condition(draw_df['date'].tolist())
    # sql = "select zbnp,jyrq from st_market.t_st_zs_rqjhb where zqdm='930950' and zbnp!=99999 and zblb='{1}' and jyrq in ({0}) "\
    #     .format(data_con,fre_code)
    # benchmark_ret=hbdb.db2df(sql,db='alluser')
    # benchmark_ret['jyrq']=benchmark_ret['jyrq'].astype(str)
    # draw_df=pd.merge(draw_df,benchmark_ret,how='left',right_on='jyrq',left_on='date').drop('jyrq',axis=1)
    # draw_df.rename(columns={'zbnp':'benchmark_ret'},inplace=True)
    draw_df = pd.merge(draw_df, df.groupby('date').mean()[['zbnp']], how='left', right_index=True, left_on='date')
    draw_df.rename(columns={'zbnp': 'benchmark_ret'}, inplace=True)
    for i in range(5):
        draw_df['group_'+str(i)]=ret_list[i]
        draw_df['group_'+str(i)]=draw_df['group_'+str(i)].rolling(len(draw_df), 1).apply(bhar)

    draw_df['benchmark_ret']=draw_df['benchmark_ret'].rolling(len(draw_df), 1).apply(bhar)

    draw_df['date']=draw_df['date'].astype(str)
    draw_df.set_index('date',inplace=True)

    plot=functionality.Plot(2000,2000)
    plot.plotly_line_style(draw_df,pic_title)
    ext_ret = 1+np.max([draw_df.iloc[-1]['group_4'] - draw_df.iloc[-1]['benchmark_ret']
                     , draw_df.iloc[-1]['group_0'] - draw_df.iloc[-1]['benchmark_ret']])
    if(fre=='M'):
        mi=len(draw_df)/12
    elif(fre=='Q'):
        mi = len(draw_df) / 4
    elif(fre=='HA'):
        mi = len(draw_df) / 2
    else:
        print('input frequence is not supported, only M,Q,HY is supported')
        raise Exception

    ext_ret =np.power(ext_ret, 1/mi) - 1
    print('annually ext ret for best group is {}%'.format(ext_ret*100))

def single_factor_ic(df,factor_name,fre,fund_flag=True):

    date_list = df['date'].unique().tolist()
    date_list.sort()
    ic_df=pd.DataFrame()
    # ic_df['date']=date_list[0:-1]
    ic_list=[]
    ic_date=[]
    fre=fre_map[fre]
    groupdf=pd.DataFrame()

    if(fund_flag):
        # ticker_ret=pd.DataFrame()
        for i in range(len(date_list)-1):
            factor_date=date_list[i]
            #ret_date = (datetime.datetime.strptime(factor_date, '%Y%m%d')+ datetime.timedelta(days=91)).strftime('%Y%m%d')
            ret_date=date_list[i+1]
            ticker_list = df[df['date']==factor_date]['jjdm'].unique().tolist()
            ticker_con = until.list_sql_condition(ticker_list)
            sql="select jjdm,jzrq,zbnp from st_fund.t_st_gm_rqjhb where zblb='{2}' and jjdm in ({0}) and jzrq ='{1}' and zbnp!=99999 "\
                .format(ticker_con,ret_date,fre)
            tempdf=hbdb.db2df(sql,db='funduser')

            if(len(tempdf)<400):
                continue

            ic_date.append(factor_date)
            # tempdf['rank_ret']=tempdf['zbnp'].rank()

            tempdf['jzrq']=tempdf['jzrq'].astype(str)
            tempdf=pd.merge(tempdf,df[df['date']==factor_date],how='inner',on='jjdm')
            # tempdf[factor_name + '_rank'] = tempdf[factor_name].rank()
            #ic_list.append((tempdf.sort_values('jjdm')['rank_ret'].reset_index(drop=True)).corr(df[df['date']==factor_date].sort_values('jjdm')[factor_name].rank().reset_index(drop=True)))

            ic_list.append(tempdf[['zbnp',factor_name]].corr(method='spearman')['zbnp'][1])

            gap=int(np.floor(len(tempdf)*0.2))
            # ret_df=pd.merge(df[df['date']==factor_date], tempdf, how='left', on='jjdm')[['jjdm','zbnp',factor_name]]
            ret_df=tempdf[['jjdm','zbnp',factor_name]]
            for group in range(2):
                tempgroup=ret_df.sort_values(factor_name)[['jjdm','zbnp']].iloc[(group)*gap:(1+group)*gap]
                tempgroup['group']=group
                tempgroup['date']=factor_date
                tempgroup['ret_date'] = ret_date
                groupdf=pd.concat([groupdf,tempgroup],axis=0)

                if(group==0):
                    tempgroup=ret_df.sort_values(factor_name)[['jjdm','zbnp']].iloc[-1*(1+group)*gap:]
                else:
                    tempgroup = ret_df.sort_values(factor_name)[['jjdm','zbnp']].iloc[
                                -1 * (1 + group) * gap:-1 * (group) * gap]
                tempgroup['group']=4-group
                tempgroup['date'] = factor_date
                tempgroup['ret_date'] = ret_date
                groupdf=pd.concat([groupdf,tempgroup],axis=0)

            tempgroup = ret_df.sort_values(factor_name)[['jjdm','zbnp']].iloc[
                        2 * gap:-2 * gap]
            tempgroup['group'] = 2
            tempgroup['date'] = factor_date
            tempgroup['ret_date'] = ret_date
            groupdf=pd.concat([groupdf,tempgroup],axis=0)

    ic_df['ic']=ic_list
    ic_df['date']=ic_date

    print('\n the average ic of {3} is {0}, the pro that ic >0 is {1},the ic std is {4},the IR of the factor is{2} '
          .format(ic_df['ic'].describe()['mean'],
                  sum(ic_df['ic']>0)/len(ic_df),
                  ic_df['ic'].describe()['mean']/ic_df['ic'].describe()['std'],factor_name,
                  ic_df['ic'].describe()['std']))

    return groupdf

if __name__ == '__main__':

    localdb=dbeng.PrvFunDB().engine
    bra = holdind_based.Barra_analysis()
    brison=holdind_based.Brinson_ability()

    # # # new joinner  return factor ic test
    # factor_name='t1_ret'
    #
    # raw_df=bra.factorlize_new_joinner(factor_name)
    # groupdf=single_factor_ic(raw_df,factor_name='new_join_'+factor_name,fre='Q',fund_flag=True)
    # grouping(groupdf, '新股季度',fre='Q')
    #
    # #pess return as factor
    # factor_name='ext_ret'
    #raw_df = nbs.factorlize_ret(factor_name)
    # groupdf = single_factor_ic(raw_df, factor_name=factor_name, fre='M', fund_flag=True)
    # grouping(groupdf, '超额月度',fre='M')
    #
    # factor_name='pes_ext_ret'
    #raw_df=nbs.factorlize_ret(factor_name,fre='Q')
    # groupdf=single_factor_ic(raw_df, factor_name=factor_name, fre='Q',fund_flag=True)
    # grouping(groupdf,'逆境季度')

    for factor_name in ['short_term_equity','long_term_equity','short_term_sector',
                        'long_term_sector','short_term_trading','long_term_trading',
                        'short_term_asset','long_term_asset']:

        raw_df=brison.factorlize_brinson(factor_name)
        groupdf=single_factor_ic(raw_df, factor_name=factor_name, fre='HA',fund_flag=True)
        grouping(groupdf,factor_name,'HA')



