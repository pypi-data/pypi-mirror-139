import os
import json

class bal:
  def start(foldername, userdatajsonfilename, template):
    foldername = str(foldername)
    template = dict(template)
    userdatajsonfilename = str(userdatajsonfilename)
    if os.path.isfile(f"{foldername}/{userdatajsonfilename}") or os.path.isfile(f"{userdatajsonfilename}"):
      pass
    else:
      if foldername == None: 
        f = open(f"{userdatajsonfilename}", "x")
        f.write(json.dumps(template))
      else:
        if os.path.exists(foldername):
          f = open(f"{foldername}/{userdatajsonfilename}", "x")
          f.write(json.dumps(template))
          return True
        else:
          folder = os.mkdir(foldername)
          f = open(f"{foldername}/{userdatajsonfilename}", "x")
          f.write(json.dumps(template))
class instance:
  def addinstance(foldername, userdatajsonfilename, valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    value = str(value)
    if foldername == None:
      f = open(f"{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      unloadf.update({valuename: value})
      os.remove(f"{userdatajsonfilename}")
      f = open(f"{userdatajsonfilename}", "x")
      f.write(json.dumps(unloadf))
    elif foldername != None:
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      unloadf.update({valuename: value})
      os.remove(f"{foldername}/{userdatajsonfilename}")
      f = open(f"{foldername}/{userdatajsonfilename}","x")
      f.write(json.dumps(unloadf))
    
  def subtractinstance(foldername, userdatajsonfilename, valuename):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    if foldername == None:
      f = open(f"{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      unloadf.pop(valuename)
      os.remove(f"{userdatajsonfilename}")
      f = open(f"{userdatajsonfilename}","x")
      f.write(json.dumps(unloadf))
    elif foldername != None:
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      unloadf.pop(valuename)
      os.remove(f"{foldername}/{userdatajsonfilename}")
      f = open(f"{foldername}/{userdatajsonfilename}","x")
      f.write(json.dumps(unloadf))


class value:
  def newvalue(foldername, userdatajsonfilename, valuename, value):
    if foldername == None:
      userdatajsonfilename = str(userdatajsonfilename)
      foldername = str(foldername)
      valuename = str(valuename)
      value = int(value)
      f = open(f"{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      unloadf.update({valuename: value})
      os.remove(f"{userdatajsonfilename}")
      f = open(f"{userdatajsonfilename}","x")
      f.write(json.dumps(unloadf))
    elif foldername != None:
      userdatajsonfilename = str(userdatajsonfilename)
      foldername = str(foldername)
      valuename = str(valuename)
      value = int(value)
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      unloadf.update({valuename: value})
      os.remove(f"{foldername}/{userdatajsonfilename}")
      f = open(f"{foldername}/{userdatajsonfilename}","x")
      f.write(json.dumps(unloadf))
  
  def changevalue(foldername, userdatajsonfilename, valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    value = int(value)
    if foldername == None:
      f = open(f"{userdatajsonfilename}", "rt").read()
      fw = open(f"{userdatajsonfilename}", "w")
      unloadf = json.loads(f)
      if valuename in unloadf:
        unloadf.update({valuename: value})
        fw.write(json.dumps(unloadf))
    elif foldername != None:
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      fw = open(f"{foldername}/{userdatajsonfilename}", "w")
      unloadf = json.loads(f)
      if valuename in unloadf:
        unloadf.update({valuename: value})
        fw.write(json.dumps(unloadf))

  def getvalue(foldername, userdatajsonfilename,valuename):
    if foldername == None:
      userdatajsonfilename = str(userdatajsonfilename)
      foldername = str(foldername)
      valuename = str(valuename)
      f = open(f"{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      return str(unloadf[valuename])
    elif foldername != None:
      userdatajsonfilename = str(userdatajsonfilename)
      foldername = str(foldername)
      valuename = str(valuename)
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      unloadf = json.loads(f)
      return str(unloadf[valuename])

  def addvalue(foldername, userdatajsonfilename,valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    value = int(value)
    valuename = str(valuename)
    if foldername != None:
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      fw = open(f"{foldername}/{userdatajsonfilename}", "w")
      unloadf = json.loads(f)
      unloadf[valuename] = unloadf[valuename] + value
      fw.write(json.dumps(unloadf))
    elif foldername == None:
      f = open(f"{userdatajsonfilename}", "rt").read()
      fw = open(f"{userdatajsonfilename}", "w")
      unloadf = json.loads(f)
      unloadf[valuename] = unloadf[valuename] + value
      fw.write(json.dumps(unloadf))
    
  def subtractvalue(foldername, userdatajsonfilename,valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    value = int(value)
    valuename = str(valuename)
    if foldername != None:
      f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
      fw = open(f"{foldername}/{userdatajsonfilename}","w")
      unloadf = json.loads(f)
      unloadf[valuename] = unloadf[valuename] - value
      fw.write(json.dumps(unloadf))
    elif foldername == None:
      f = open(f"{userdatajsonfilename}", "rt").read()
      fw = open(f"{userdatajsonfilename}","w")
      unloadf = json.loads(f)
      unloadf[valuename] = unloadf[valuename] - value
      fw.write(json.dumps(unloadf))
