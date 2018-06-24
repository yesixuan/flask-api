# encoding: utf-8
"""
Created by Vic on 2018/6/24 15:38
"""
from app.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
