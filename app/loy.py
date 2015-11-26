from datetime import datetime


from apscheduler.scheduler import Scheduler

import time

# Start the scheduler
sched = Scheduler()
sched.start()


@sched.interval_schedule(seconds=5)
def job_function():
    return fun()

def fun():
	print "Loloy"
# Schedule job_function to be called every two hours
#sched.add_interval_job(fun, hours=.001)

# The same as before, but start after a certain time point
#sched.add_interval_job(job_function, hours=.01, start_date='2014-03-26 17:01')
while True:
	pass
