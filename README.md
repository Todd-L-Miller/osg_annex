# osg-annex-tools
Tools for using XSEDE resources from OSG.

These tools are meant to help you acquire and manage XSEDE resources so that you can use them via
OSG.  The OSG uses [HTCondor](http://htcondor.org) as its workload management (batch) system.  The
detailed instructions further below will assume that you're accessing the OSG via
[OSG Connect](https://osgconnect.net).

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
These instructions assume you have an [OSG Connect](https://osgconnect.net) account and an
[XSEDE User Portal](https://portal.xsede.org) account.

You will need to have contacted an OSG administrator and obtained a token to allow your annexes
to join the OSG pool.  The following instructions assume that the token is in the file
`~/token.txt` ast OSG Connect.

The following instructions assume that your user name at the XSEDE User Portal is *xsede-sicilian* and
*osg-sicilian* at OSG Connect.

## First-Time set-up
1.  Open two terminal windows.
1.  [Log in](https://support.opensciencegrid.org/support/solutions/articles/12000027675)
    to your OSG Connect account in one of them.
1.  In that terminal,
	1.  get a copy of the tools: `git clone https://github.com/Todd-L-Miller/osg_annex_tools.git`
	1.  `cd osg_annex_tools`
	1.  generate the SLURM script: `osg_annex_generate`
	1.  copy it and the token to XSEDE:
	    `scp stampede2-normal.slurm ~/token.txt xsede-sicilian@login.xsede.org:~`
1.  [Log in](https://portal.xsede.org/web/xup/single-sign-on-hub) to the XSEDE single-sign-on
    portal (login.xsede.org) in the other.
1.  In that terminal,
	1.  copy the SLURM script and the token to Stampede2:\
	    `gsiscp stampede2-normal.slurm ~/token.txt stampede2`
	1.  log into Stampede2: `gsissh stampede2`
	1.  create a directory that the SLURM script will need: `mkdir ~/osvo-pilot`

## Annexing Resources
(These instructions assume you have two terminal windows open, one logged into OSG Connect, and the
other logged into login.xsede.org; if you just finished the first-time set-up instructions, just keep
going.)

1.  In the login.xsede.org terminal,
	1.  submit the SLURM script: `sbatch ./stampede2-normal.slurm`.\
	    This starts the annexation process.  You should see a line like
		> Submitted batch job 5438235
		
		at the end of the output.
	1.  Optionally, you can run `squeue -j 5438235` (replacing 5438235 with your batch job number)
	    to see if the job has started yet; it might take a while.
	1.  Optionally, once it has, you can run watch the HTCondor logs to see what's happening:\
		`tail --follow osgvo-pilot/5438235.out` (replacing 5438235 with your batch job number)

## Monitoring Annexes
1.  In the OSG Connect terminal,
	1.  run `osg_annex_status osg-sicilian@stampede2-normal` to see if your resources have joined the
	    pool; it might take a while.  If you elected to watch the HTCondor logs, you're waiting for
		a line like
		> 03/27/20 01:48:17 Setting ready state 'Ready' for STARTD

## Starting Jobs
It might take a while for HTCondor to schedule jobs to run on your annex.  (By default, the annex is
configured to run only your jobs.)  If your jobs won't run on the other resources available to OSG, you
can require that they run on a particular annex by using the **requirements** command in the submit file,
specifically: `requirements = AnnexName == "osg-sicilian@stampede2-normal"`.

## Shutting Annexes Off
1.  In the OSG Connect terminal,
	1. run `osg_annex_off osg-sicilian@stampede2-normal`.
