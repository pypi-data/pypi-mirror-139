# nuwsgi

This project is a fork of [uwsgi](https://uwsgi-docs.readthedocs.org/en/latest/).

nuwsgi is mostly a re-packaging of mainstream uwsgi with added functionality
from this [Pull Request](https://github.com/unbit/uwsgi/pull/2311)

## Background

uwsgi has a feature called harakiri which is often used as a last resort option
to prevent slow endpoints and/or bugs from taking too much production resources
by killing the worker after a specific timeout.

The downside is that it uses SIGKILL (ie kill -9) which terminates the process
abruptly. This creates a number of problems, especially with observability
tools: request metadata like traces and errors won't be flushed, which makes
harder to find the underlying issue that is causing the timeout.

## Solution

nuwsgi adds 3 extra flags to control harakiri's behavior:

- **harakiri-graceful-timeout** additional timeout for the worker to attempt a
graceful shutdown. The application can catch the termination signal and
perform an "emergency shutdown"
- **harakiri-graceful-signal** determines which signal should be used for
graceful harakiri (default SIGTERM)
- **harakiri-graceful-queue-threshold** only triggers a harakiri if/when the
listen queue crosses a threshold. Harakiri continues to be checked until the
conditions are met

The combination of those 3 features allow the operator to:

- gracefully shutdown your application by catching a signal
- add some extra time for the graceful shutdown to happen
- allow requests to continue running past harakiri timeout if the
  listen queue (backlog) is under a threshold
- do a hardkill if the graceful shutdown takes too long

## Examples:

```
$ uwsgi --master --http :8080 --harakiri 1 \
        --wsgi-file tests/harakiri.py \
	--py-call-osafterfork \
	--lazy-apps \
	--enable-threads \
	--threads 2 \
	--harakiri-graceful-timeout 1 \
	--harakiri-graceful-signal 31
```
## Installation:

pip install nuwsgi==2.0.19.2

Despite the different package name, the binary name is the same so you can use
`uwsgi` as usual. 

## Why fork?

I created the fork so I could deploy the changes before they get merged to the
mainstream project:

The binary, code, build process, and version numbers are exactly the same as
mainstream uwsgi. This is the [Pull Request](https://github.com/unbit/uwsgi/pull/2311)

The fork is (hopefully) temporary and will be discontinued(but not deleted)
after the PR is merged

# Mainstream uwsgi:

Official docs: https://uwsgi-docs.readthedocs.org/en/latest/
