from flask import *
from extensions import mysql
from flask import Flask, session, redirect, url_for, escape, request, flash
import hashlib
import uuid
import ast


vitals = Blueprint('vitals', __name__, template_folder='templates') #, url_prefix="/04d8ee3a8730446aa2b4/pa3")


@vitals.route('/vitals', methods=['GET'])
def my_route():
	print 'GETTING'
	return render_template("index.html", name='vitals')