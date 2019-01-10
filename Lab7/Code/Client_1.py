import thread
import time

count = 0
# Define a function for the thread
def loop1( ):
	global count

	while True:
		count = input("")



def loop2( ):
	global count

	while True:

		time.sleep(0.5)
		count +=1
		print "%s" % ( count )

thread.start_new_thread( loop1, () )

loop2()
