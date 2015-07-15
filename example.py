# coding: utf8-interpy

# example path building
datdir = '/projects/data'
ver = 1
feat = 'spe'
ndim = {'mfc' : 35, 'spe' : 513}
search = "#{datdir}/feat/#{feat}_#{ndim[feat]}/ver#{ver}/*.#{feat}"
print(search)

# example command building for cli applications 
in_wav = 'in.wav'
out_mfc = 'out.mfc'
cmd = "calc_mfc --order #{ndim['mfc']-1} #{in_wav} #{out_mfc}"
print(cmd)

# example combining local and global variables
global_var = 'foo'
	
def my_fun():
    local_var = 'bar'
    print("#{local_var}#{global_var}")

my_fun()

# python alternatives
your_name = 'John'
print("Hello %s" % (your_name))
print("Hello {}".format(your_name))
print("Hello {your_name}".format(your_name=your_name))
print("Hello {your_name}".format(**locals()))
	
import os
search = "{}/feat/{}_{}/ver{}/*.{}".format(datdir, feat, ndim[feat], ver, feat)
search = "{datdir}/feat/{feat}_{ndim}/ver{ver}/*.{feat}".format(datdir=datdir, feat=feat, ndim=ndim[feat], ver=ver)
search = os.path.join(datdir, feat, '%s_%d' % (feat, ndim[feat]), 'ver%d' % ver, '*.%s' % feat)
	
def my_fun2():
    local_var = 'bar'
    print("#{global_var}#{local_var}".format(global_var=global_var, local_var=local_var))
    print("#{global_var}#{local_var}".format(**dict(globals(), **locals())))

my_fun2()

