from __future__ import print_function
import glob, re
import vtk
from vtk.util.numpy_support import vtk_to_numpy

def list_files(fpattern):
    files = glob.glob(fpattern)
    grab_digit = lambda f : int(re.search("([0-9]*)\.vtk",f).groups()[-1])
    files.sort(key=lambda f: grab_digit(f) )
    return files

def iterate(fpattern):
    files = list_files(fpattern)
    for f in files:
        yield get_data(f)

def get_data(fname):
    r=vtk.vtkUnstructuredGridReader()
    r.SetFileName(fname)
    r.ReadAllFieldsOn()
    r.ReadAllScalarsOn()
    r.ReadAllVectorsOn()
    r.Update()
    op = r.GetOutput()
    x = vtk_to_numpy( op.GetPoints().GetData() )
    pd = op.GetPointData()
    n = pd.GetNumberOfArrays()
    dic = { pd.GetArrayName(i):vtk_to_numpy( pd.GetArray(i) ) 
            for i in range(n) }
    cd = op.GetCellData()
    nc = cd.GetNumberOfArrays()
    dic.update( { 'cell_'+cd.GetArrayName(i):vtk_to_numpy( cd.GetArray(i) ) 
                    for i in range(nc) } )
    return x,dic

def cat_with_times(fpattern,timefile, fields):
    with open(timefile,"r") as f:
        times = [ float(l) for l in f ]
    for dat in iterate(fpattern):
        pass
