import cobra
from cobra.io import read_sbml_model
from cobra.sampling import sample
from cobra.sampling import OptGPSampler, ACHRSampler
import os
import time
import signal

# Define a timeout handler
class TimeoutException(Exception): pass

def timeout_handler(signum, frame):
    raise TimeoutException

# Apply the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)

count = 1
for f in os.listdir():
    if "xml" in f:
        filename = str(f)+'_training_data_optgp_1.csv'
        if filename not in os.listdir():
            print("Loading model " + str(count) + " in...")
            # Set a 60-second alarm
            signal.alarm(60)
            try:
                start_time = time.time()
                model = read_sbml_model(f)

                optgp = OptGPSampler(model, processes=4)

                i = 0
                for s in optgp.batch(5000, 4):
                    i = i+1
                    print("Saving out OptGP sampling", i)
                    s.to_csv(str(f)+'_training_data_optgp_'+str(i)+'.csv')
                
                # Cancel the alarm after successful execution
                signal.alarm(0)
                end_time = time.time()
                print(f"Model {count} loaded in {end_time - start_time} seconds.")
                count = count + 1
            except TimeoutException:
                print("Model loading exceeded 60 seconds, skipping...")
            except Exception as e:
                print(f'Model not valid or error occurred, skipping... Error: {str(e)}')
            finally:
                # Cancel the alarm if an exception occurred
                signal.alarm(0)