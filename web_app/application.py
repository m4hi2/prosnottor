import functools

from flask import Blueprint, redirect, render_template, request

bp = Blueprint('application', __name__, url_prefix='/')
