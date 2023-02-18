import functools
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request,
    session, url_for, make_response, jsonify
)
#from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import json


bp = Blueprint('master', __name__, url_prefix='/mst')


@bp.route('/getChannelType', methods=('GET', 'POST'))
def getChannelType():
    #model = str(request.form['model'])
    data = {}
    with open('master.json', encoding='utf-8') as fh:
        data = json.load(fh)
    
    return jsonify(data["channelType"])

@bp.route('/getBrand', methods=('GET', 'POST'))
def getBrand():
    channelType = str(request.form['channelType'])
    #channelType = request.args.get('channelType', default = 'all', type = str)
    data = {}
    result = []
    with open('master.json', encoding='utf-8') as fh:
        data = json.load(fh)

    for brand in data["brand"]:
        if channelType == 'online' :
            if brand["channelType"] == 'online' or brand["channelType"] == 'all' :
                result.append({"id":brand["id"], "value":brand["value"]})
        elif channelType == 'offline' :
            if brand["channelType"] == 'offline' or brand["channelType"] == 'all' :
                result.append({"id":brand["id"], "value":brand["value"]})
        else :
            result.append({"id":brand["id"], "value":brand["value"]})

    return jsonify(result)

@bp.route('/getCampaignType', methods=('GET', 'POST'))
def getCampaignType():
    data = {}
    with open('master.json', encoding='utf-8') as fh:
        data = json.load(fh)
    
    return jsonify(data["campaignType"])

@bp.route('/getOfferType', methods=('GET', 'POST'))
def getOfferType():
    data = {}
    with open('master.json', encoding='utf-8') as fh:
        data = json.load(fh)
    
    return jsonify(data["offerType"])

@bp.route('/getShop', methods=('GET', 'POST'))
def getShop():
    data = {}
    with open('master.json', encoding='utf-8') as fh:
        data = json.load(fh)
    
    return jsonify(data["shop"])

@bp.route('/getProduct', methods=('GET', 'POST'))
def getProduct():
    data = {}
    with open('master.json', encoding='utf-8') as fh:
        data = json.load(fh)
    
    return jsonify(data["product"])
