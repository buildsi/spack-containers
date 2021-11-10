# Spack Monitor Analysis Containers

I think we are eventually going to need to do actual splicing, meaning that we
save successful container builds that have a bunch of spack software installed:

 - across packages
 - across versions
 - across operating systems
 
And actually, if we just use binding of libraries from a host into a container (or between containers!)
we can also emulate a splice without needing spack. That would be neat! Let's give it a try.
The base containers (the same to generate the analysis results and predictions) are built at [spack-monitor-analysis](https://github.com/buildsi/spack-monitor-analysis).

**under development**
