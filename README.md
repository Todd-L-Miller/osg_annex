# osg-annex-tools
Tools for using XSEDE resources from OSG.

These tools are meant to help you acquire and manage XSEDE resources so that you can use them via
OSG.  The OSG uses [HTCondor](http://htcondor.org) as its workload management (batch) system.  The
detailed instructions further below will assume that you're accessing the OSG via
[OSG Connect](http://osgconnect.net).

In this toolset, XSEDE resources are grouped into "annexes", each with a name; an annex may contain one
or more machines from one or more XSEDE resources or sites; or one annex may be one part of a resource
and another example some other part of the same resource.  For example, TACC's
[Stampede2](https://www.tacc.utexas.edu/systems/stampede2) supercomputer has both Knight's Landing and 
Xeon processors, which you may wish to manage independently.

# Quick Reference

## osg_annex_status
Run `osg_annex_status annex-name` to get information about how busy *annex-name* is.

You may append arguments for *condor_status* (see the man page) after the *annex-name*.

## osg_annex_off
Run `osg_annex_off annex-name` to turn off *annex-name*.  This will release the corresponding resource,
preserving your allocation.  Annexes turn themselves off after they've been idle for three hours.

You may append arguments for *condor_off* (see the man page) after the *annex-name*.

## osg_annex_generate
**Only works for Stampede2 right now**

Run `osg_annex_generate` to create a SLURM script which annexes (part of) an XSEDE resource.  (For now,
you'll have to copy the script to Stampede2 (and perform a few other steps) manually.)  Each time you
submit the script there, it will add more resources to the same annex.  By default, the max runtime of
the SLURM job is one hour.  Use the `--duration` command-line argument to specify, as *hh::mm::ss*,
your preferred duration.

The default queue (partition) is `normal`; use the command-line option `--queue` to change it.  The
default name for the annex (*user-name*@Stampede2-normal) includes the name of the user who ran
`osg_annex_generate` and the queue name; to specify annex's name, use the `--name` option.  Likewise,
the default name for the generated file (stampede2-normal.slurm) includes the queue name; use the
`--target` option to change it.

# Detailed Instructions
...
