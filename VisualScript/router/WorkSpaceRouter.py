from flask import request, jsonify
from tkinter import filedialog, Tk

from VisualScript import app
from VisualScript.src.File.FileManager import *


@app.route('/VisualScript/WorkSpace')
def getWorkSpace():
    return jsonify(WORKSPACE.getTreeJSON())

@app.route('/VisualScript/WorkSpace/create', methods=['POST'])
def createProject():
    info = {
        'project' : request.form['project'],
        'suite' : request.form['suite'],
        'case' : request.form['case'],
        'path' : request.form['path']
    }
    try:
        new(info)
        path = info['path']
        jsonPath = path + '/' + info['project'] + '/' + info['project'] + '.json'
        return load(jsonPath)
    except:
        return False

@app.route('/VisualScript/WorkSpace/load', methods=['POST'])
def loadProjects():
    path = request.form['path']
    return load(path)

@app.route('/VisualScript/WorkSpace/getFilePath')
def getFilePath():
    root = Tk()
    f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
    root.destroy()
    filePath = f.name
    return filePath
