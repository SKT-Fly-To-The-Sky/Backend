import functools
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request,
    session, url_for, jsonify
)
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from app.db import init_db
from app.db import query_db
from app.db import query_db2

bp = Blueprint('stat', __name__, url_prefix='/stat')


@bp.route('/StatRecByDate', methods=('GET', 'POST'))
@login_required  
def StatRecByDate():
    return render_template('stat/StatRecByDate.html')

@bp.route('/StatCarTypeByDate', methods=('GET', 'POST'))
@login_required  
def StatCarTypeByDate():
    return render_template('stat/StatCarTypeByDate.html')

@bp.route('/StatTimeByDate', methods=('GET', 'POST'))
@login_required  
def StatTimeByDate():
    return render_template('stat/StatTimeByDate.html')


@bp.route('/StatRecByDateChart', methods=('GET', 'POST'))
@login_required  
def StatRecByDateChart():
    crtfromdt = str(request.form['crtfromdt'])
    crttodt = str(request.form['crttodt'])
    origin = str(request.form['origin'])
    brand = str(request.form['brand'])
    carType = str(request.form['model'])
    carTypeDtl = str(request.form['type'])
    caryear = str(request.form['year'])
    carcolor = str(request.form['color'])
    cardmg = str(request.form['cardmg'])
    recrsltcd = str(request.form['recrsltcd'])
    fake = str(request.form['fake'])
    
    print(crtfromdt)
    print(crttodt)

    error = None
    sql = '''
    select 
        d.basedt,
        count(reqid) as tot,
        sum(case when recrsltcd=0 then 1 else 0 end) as succ,
        sum(case when recrsltcd<>0 then 1 else 0 end) as fail,
        to_char(case when count(reqid)<>0 then sum(case when recrsltcd=0 then 1.0 else 0.0 end) /count(reqid) else 0 end*100,'FM990.00') as succ_rate
    from
        (
            select to_char(generate_series( '2019-12-25'::date , '2020-01-07'::date, '1 day'::interval)::date,'YYYY/MM/DD') as basedt
        ) d left outer join 
        ( 
            select * 
            from tbrecresult 
            where 
                    crtdt >= to_date('20191225','YYYYMMDD') 
                and crtdt < to_date('20200110','YYYYMMDD') + INTERVAL '1 day'
        ) r
        on d.basedt=to_char(r.crtdt,'YYYY/MM/DD')
    group by d.basedt
    order by 1
    '''
    
    '''
    param = ()
    
    sql = sql +  ' and crtdt >= to_date(%s,\'YYYYMMDD\')'
    param = param + (crtfromdt.replace('-',''),)

    sql = sql +  ' and crtdt < to_date(%s,\'YYYYMMDD\') + INTERVAL \'1 day\''
    param = param + (crttodt.replace('-',''),)

    if origin != 'ALL':
        sql = sql +  ' and recbrand in (select codenm from tbcode where classtype=\'BRAND\' and uppercode = %s)'
        param = param + (origin,)
        print("origin:"+origin)

    if brand != 'ALL':
        sql = sql +  ' and recbrand = %s'
        param = param + (brand,)
        print("brand:"+brand)
    
    if carType != 'ALL':
        sql = sql +  ' and reccarType = %s'
        param = param + (carType,)
        print("carType:"+carType)
    
    if carTypeDtl != 'ALL':
        sql = sql +  ' and reccartypedtl = %s'
        param = param + (carTypeDtl,)
        print("carTypeDtl:"+carTypeDtl)
    
    if caryear != 'ALL':
        sql = sql +  ' and reccaryear >= %s'
        param = param + (caryear,)
        print("caryear:"+caryear)
    
    if carcolor != 'ALL':
        sql = sql +  ' and reccolor = %s'
        param = param + (carcolor,)
        print("carcolor:"+carcolor)
    
    if cardmg != 'ALL':
        sql = sql +  ' and recdmg = %s'
        param = param + (cardmg,)
        print("cardmg:"+cardmg)
    
    if recrsltcd !='ALL':
        sql = sql +  ' and recfsltcd = %s'
        param = param + (recrsltcd,)
        print("recrsltcd:"+recrsltcd)
    
    sql = sql+ ' LIMIT %s' # 한 페이지에 표시되는 행수 10
    param = param + ( pageSize,) 

    sql = sql+ ' OFFSET %s' # 어디서부터 읽을 것인지
    param = param + ( pageSize*pageNo,) 
    '''
    # {list:[{data:[],label},{data:[],label}]}
    obj = query_db2(sql)
    print(obj)
    return jsonify(obj)

@bp.route('/StatCarTypeByDateChart', methods=('GET', 'POST'))
@login_required  
def StatCarTypeByDateChart():
    crtfromdt = str(request.form['crtfromdt'])
    crttodt = str(request.form['crttodt'])
    origin = str(request.form['origin'])
    brand = str(request.form['brand'])
    carType = str(request.form['model'])
    carTypeDtl = str(request.form['type'])
    caryear = str(request.form['year'])
    carcolor = str(request.form['color'])
    cardmg = str(request.form['cardmg'])
    recrsltcd = str(request.form['recrsltcd'])
    fake = str(request.form['fake'])
    
    print(crtfromdt)
    print(crttodt)

    error = None
    sql = '''
    select 
        d.basedt as "일자",
        sum(case when reqbrand = '현대'  then 1 else 0 end) as "현대",
        to_char(case when sum(case when reqbrand = '현대'  then 1else 0 end)=0 then 0.0 else sum(case when reqbrand = '현대' and recrsltcd=0 then 1.0 else 0.0 end)/sum(case when r.reqbrand = '현대'  then 1 else 0 end) end * 100 ,'FM990.00') as "현대_성공률",
        sum(case when reqbrand = '기아'  then 1 else 0 end) as "기아",
        to_char(case when sum(case when reqbrand = '기아'  then 1else 0 end)=0 then 0.0 else sum(case when reqbrand = '기아' and recrsltcd=0 then 1.0 else 0.0 end)/sum(case when r.reqbrand = '기아'  then 1 else 0 end) end * 100 ,'FM990.00') as "기아_성공률"
    from
        (
            select to_char(generate_series( '2019-12-25'::date , '2020-01-07'::date, '1 day'::interval)::date,'YYYY/MM/DD') as basedt
        ) d left outer join 
        ( 
            select * 
            from tbrecresult 
            where 
                    crtdt >= to_date('20191225','YYYYMMDD') 
                and crtdt < to_date('20200110','YYYYMMDD') + INTERVAL '1 day'
        ) r
        on d.basedt=to_char(r.crtdt,'YYYY/MM/DD')
    group by d.basedt
    order by 1
    '''
    sql = '''
    select 
        d.basedt,
        case when r.reqbrand is null  then '없음' else r.reqbrand end reqbrand,
        count(reqid) as tot,
        sum(case when recrsltcd=0 then 1 else 0 end) as succ,
        sum(case when recrsltcd<>0 then 1 else 0 end) as fail,
        to_char(case when count(reqid)<>0 then sum(case when recrsltcd=0 then 1.0 else 0.0 end) /count(reqid) else 0 end*100,'FM990.00') as succ_rate
    from
        (
            select to_char(generate_series( '2019-12-25'::date , '2020-01-07'::date, '1 day'::interval)::date,'YYYY/MM/DD') as basedt
        ) d left outer join 
        ( 
            select * 
            from tbrecresult 
            where 
                    crtdt >= to_date('20191225','YYYYMMDD') 
                and crtdt < to_date('20200110','YYYYMMDD') + INTERVAL '1 day'
        ) r
        on d.basedt=to_char(r.crtdt,'YYYY/MM/DD')
    group by d.basedt, r.reqbrand
    order by 1
    '''

    obj = query_db2(sql)
    print(obj)
    return jsonify(obj)

@bp.route('/StatTime', methods=('GET', 'POST'))
@login_required  
def StatTime():
    print("StatTime")
    
    crtfromdt = str(request.form['crtfromdt'])
    crttodt = str(request.form['crttodt'])
    origin = str(request.form['origin'])
    brand = str(request.form['brand'])
    carType = str(request.form['model'])
    carTypeDtl = str(request.form['type'])
    caryear = str(request.form['year'])
    carcolor = str(request.form['color'])
    cardmg = str(request.form['cardmg'])
    recrsltcd = str(request.form['recrsltcd'])
    fake = str(request.form['fake'])
    
    
    print(crttodt)

    error = None
    sql = '''
    select 
        d.basedt,
        count(reqid) as tot,
        sum(case when recrsltcd=0 then 1 else 0 end) as succ,
        sum(case when recrsltcd<>1 then 1 else 0 end) as fail,
        to_char(case when count(reqid)<>0 then sum(case when recrsltcd=0 then 1.0 else 0.0 end) /count(reqid) else 0 end*100,'FM990.00') as succ_rate
    from
        (
            select to_char(  generate_series 
            ('2020-01-01 00:00:00'::date,'2020-01-01 23:59:59'::date + '1 day - 1 second'::interval,'1 hour'), 'HH24') as basedt
        ) d left outer join 
        ( 
            select * 
            from tbrecresult 
            where 
                    crtdt >= to_date('20191225','YYYYMMDD') 
                and crtdt < to_date('20200110','YYYYMMDD') + INTERVAL '1 hour'
        ) r
        on d.basedt=to_char(r.crtdt,'HH24')
    group by d.basedt
    order by 1
    '''

    obj = query_db2(sql)
    print(obj)
    return jsonify(obj)