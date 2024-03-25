import cobra
from cobra.io import read_sbml_model
from cobra.sampling import sample
from cobra.sampling import OptGPSampler, ACHRSampler
import os
import time
import signal

seeds = ['Seed299768.3.xml', 'Seed362242.7.796.xml', 'Seed357348.6.796.xml', 'Seed264203.3.xml', 'Seed354.1.796.xml', 'Seed270374.3.796.xml', 'Seed232721.5.796.xml', 'Seed122587.1.796.xml', 'Seed211110.1.796.xml', 'Seed78245.7.796.xml', 'Seed575585.3.796.xml', 'Seed1496.1.796.xml', 'Seed351016.3.796.xml', 'Seed317655.17.796.xml', 'Seed749414.3.796.xml', 'Seed177416.3.xml', 'Seed536230.4.796.xml', 'Seed526980.3.796.xml', 'Seed537970.5.796.xml', 'Seed714995.3.796.xml', 'Seed269798.12.xml', 'Seed567106.3.796.xml', 'Seed342108.5.xml', 'Seed189518.1.xml', 'Seed537006.5.796.xml', 'Seed272622.10.796.xml', 'Seed391624.3.796.xml', 'Seed360910.3.796.xml', 'Seed508765.6.796.xml', 'Seed194439.1.796.xml', 'Seed326297.7.xml', 'Seed205918.4.796.xml', 'Seed644107.3.796.xml', 'Seed744980.3.796.xml', 'Seed76869.3.xml', 'Seed297245.3.796.xml', 'Seed176299.3.xml', 'Seed115711.7.xml', 'Seed667128.3.796.xml', 'Seed269483.3.796.xml', 'Seed260799.14.796.xml', 'Seed244592.3.796.xml', 'Seed290402.34.xml', 'Seed563040.3.796.xml', 'Seed205914.11.796.xml', 'Seed324925.4.796.xml', 'Seed323261.3.xml', 'Seed393130.3.xml', 'Seed217.1.796.xml', 'Seed281090.3.xml', 'Seed318161.16.796.xml', 'Seed93062.4.xml', 'Seed471872.6.796.xml', 'Seed314225.3.796.xml', 'Seed398578.3.796.xml', 'Seed243230.1.xml', 'Seed170187.1.xml', 'Seed632292.3.796.xml', 'Seed641147.3.796.xml', 'Seed161544.4.796.xml', 'Seed272624.3.xml', 'Seed435591.10.796.xml', 'Seed220664.3.796.xml', 'Seed436717.3.796.xml', 'Seed537457.7.796.xml', 'Seed246194.3.xml', 'Seed221988.1.xml', 'Seed228399.1.796.xml', 'Seed279714.3.796.xml', 'Seed326298.3.xml', 'Seed100226.1.xml', 'Seed349101.4.796.xml', 'Seed683837.3.796.xml', 'Seed400673.6.796.xml', 'Seed60480.18.xml', 'Seed297246.15.796.xml', 'Seed76114.4.xml', 'Seed757424.7.796.xml', 'Seed376686.10.796.xml', 'Seed198094.1.xml', 'Seed509191.4.796.xml', 'Seed290397.13.xml', 'Seed521098.4.796.xml', 'Seed391591.24.796.xml', 'Seed714359.3.796.xml', 'Seed634456.3.796.xml', 'Seed525246.3.796.xml', 'Seed85962.1.xml', 'Seed412021.3.796.xml', 'Seed525368.3.796.xml', 'Seed575584.3.796.xml', 'Seed267608.1.796.xml', 'Seed292414.10.796.xml', 'Seed290633.1.xml', 'Seed460265.11.796.xml', 'Seed360106.5.796.xml', 'Seed613026.4.796.xml', 'Seed608538.3.796.xml', 'Seed543728.3.796.xml', 'Seed467661.3.796.xml', 'Seed227377.1.xml', 'Seed517418.3.796.xml', 'Seed390235.3.796.xml', 'Seed862516.3.796.xml', 'Seed211586.9.xml', 'Seed580331.4.796.xml', 'Seed323098.3.xml', 'Seed525371.3.796.xml', 'Seed480119.5.796.xml', 'Seed637380.6.796.xml', 'Seed267671.1.xml', 'Seed243261.3.796.xml', 'Seed749927.5.796.xml', 'Seed426117.3.796.xml', 'Seed398527.4.796.xml', 'Seed334802.3.796.xml', 'Seed350054.11.796.xml', 'Seed265072.7.xml', 'Seed537972.5.796.xml', 'Seed391613.3.796.xml', 'Seed693985.5.796.xml', 'Seed272561.1.xml', 'Seed163164.1.xml', 'Seed160492.1.xml', 'Seed412022.9.796.xml', 'Seed262768.1.xml', 'Seed640512.3.796.xml', 'Seed380749.4.796.xml', 'Seed295405.11.796.xml', 'Seed412694.5.796.xml', 'Seed158879.1.xml', 'Seed106370.11.xml', 'Seed498848.5.796.xml', 'Seed634459.3.796.xml', 'Seed85963.1.xml', 'Seed360110.3.xml', 'Seed557599.3.796.xml', 'Seed169963.1.xml', 'Seed266117.6.xml', 'Seed556267.4.796.xml', 'Seed471871.7.796.xml', 'Seed212717.1.xml', 'Seed405532.4.796.xml', 'Seed137722.3.796.xml', 'Seed469609.3.796.xml', 'Seed349106.5.796.xml', 'Seed207559.3.xml', 'Seed405533.4.796.xml', 'Seed272843.1.796.xml', 'Seed243273.1.xml', 'Seed223926.1.xml', 'Seed261594.1.xml', 'Seed438753.3.796.xml', 'Seed604162.3.796.xml', 'Seed246200.3.xml', 'Seed314565.3.796.xml', 'Seed206672.1.xml', 'Seed391038.7.796.xml', 'Seed649639.3.796.xml', 'Seed320389.3.796.xml', 'Seed122586.1.xml', 'Seed592022.4.796.xml', 'Seed373153.25.796.xml', 'Seed335543.6.796.xml', 'Seed226185.1.796.xml', 'Seed243233.4.xml', 'Seed264462.1.xml', 'Seed302409.3.xml', 'Seed573066.3.796.xml', 'Seed292415.3.xml', 'Seed445932.3.xml', 'Seed257313.1.xml', 'Seed391595.3.796.xml', 'Seed391593.3.796.xml', 'Seed360095.3.xml', 'Seed402882.10.796.xml', 'Seed405416.6.796.xml', 'Seed417398.15.796.xml', 'Seed271848.6.796.xml', 'Seed243231.1.xml', 'Seed224326.1.xml', 'Seed396595.4.796.xml', 'Seed401614.5.xml', 'Seed68909.1.796.xml', 'Seed639282.3.796.xml', 'Seed167555.5.796.xml', 'Seed216596.1.xml', 'Seed526994.3.796.xml', 'Seed272947.1.xml', 'Seed381666.6.796.xml', 'Seed315730.11.796.xml', 'Seed515621.3.796.xml', 'Seed391037.3.796.xml', 'Seed675817.3.796.xml', 'Seed205922.3.xml', 'Seed243277.1.xml', 'Seed224308.1.xml', 'Seed638300.3.796.xml', 'Seed767463.3.796.xml', 'Seed298386.1.xml', 'Seed525271.4.796.xml', 'Seed190304.1.xml', 'Seed160490.1.xml', 'Seed535289.3.796.xml', 'Seed596153.3.796.xml', 'Seed317025.3.xml', 'Seed413999.4.796.xml', 'Seed580332.3.796.xml', 'Seed598659.3.796.xml', 'Seed296591.1.xml', 'Seed269799.3.xml', 'Seed405531.7.796.xml', 'Seed342610.3.796.xml', 'Seed326442.4.xml', 'Seed537971.5.796.xml', 'Seed266834.1.xml', 'Seed399795.3.796.xml', 'Seed674977.3.796.xml', 'Seed634457.3.796.xml', 'Seed762051.3.796.xml', 'Seed314282.3.796.xml', 'Seed59922.7.796.xml', 'Seed652103.3.796.xml', 'Seed500635.8.796.xml', 'Seed626418.3.796.xml', 'Seed351746.4.796.xml', 'Seed318167.13.xml', 'Seed272626.1.xml', 'Seed224914.1.xml', 'Seed288681.12.796.xml', 'Seed192222.1.xml', 'Seed259536.19.796.xml', 'Seed367737.4.796.xml', 'Seed406425.4.796.xml', 'Seed272560.3.xml', 'Seed233412.1.796.xml', 'Seed52598.3.796.xml', 'Seed610130.3.796.xml', 'Seed66692.3.796.xml', 'Seed243276.1.xml', 'Seed383629.4.796.xml', 'Seed331272.3.796.xml', 'Seed391597.3.796.xml', 'Seed643562.5.796.xml', 'Seed688245.4.796.xml', 'Seed399726.4.xml', 'Seed320372.3.796.xml', 'Seed228410.1.xml', 'Seed644042.3.796.xml', 'Seed485915.4.796.xml', 'Seed671076.4.796.xml', 'Seed224324.1.xml', 'Seed693971.4.796.xml', 'Seed292459.1.xml', 'Seed322159.7.796.xml', 'Seed546267.4.796.xml', 'Seed345073.6.xml', 'Seed314289.8.796.xml', 'Seed402626.5.796.xml', 'Seed439497.5.796.xml', 'Seed171101.1.xml', 'Seed319701.3.xml', 'Seed869269.3.796.xml', 'Seed266265.5.796.xml', 'Seed272630.7.796.xml', 'Seed905067.3.796.xml', 'Seed410289.13.796.xml', 'Seed283942.3.xml', 'Seed269482.1.xml', 'Seed272831.7.796.xml', 'Seed527029.3.796.xml', 'Seed634452.3.796.xml', 'Seed272635.1.xml', 'Seed234826.3.xml', 'Seed93061.3.xml', 'Seed309807.19.xml', 'Seed680198.5.796.xml', 'Seed572264.4.796.xml', 'Seed272562.1.xml', 'Seed402881.6.796.xml', 'Seed210007.1.796.xml', 'Seed445335.4.796.xml', 'Seed242231.4.xml', 'Seed235279.1.796.xml', 'Seed864569.5.796.xml', 'Seed517417.4.796.xml', 'Seed749219.3.796.xml', 'Seed220668.1.xml', 'Seed516466.4.796.xml', 'Seed693982.3.796.xml', 'Seed563773.3.796.xml', 'Seed365044.20.796.xml', 'Seed208964.1.xml', 'Seed645464.3.796.xml', 'Seed634453.3.796.xml', 'Seed451516.9.796.xml', 'Seed447214.4.796.xml', 'Seed525897.4.796.xml', 'Seed247156.1.xml', 'Seed83332.1.xml', 'Seed31964.6.796.xml', 'Seed164546.7.796.xml', 'Seed472759.3.796.xml', 'Seed272623.1.xml', 'Seed258594.1.xml', 'Seed640511.6.796.xml', 'Seed742159.3.796.xml', 'Seed395963.13.796.xml', 'Seed760570.3.796.xml', 'Seed380394.3.796.xml', 'Seed331271.3.796.xml', 'Seed400667.4.xml', 'Seed407976.7.796.xml', 'Seed62977.3.xml', 'Seed243274.1.xml', 'Seed36873.1.xml', 'Seed360107.5.796.xml', 'Seed319224.15.xml', 'Seed641149.3.796.xml', 'Seed224911.1.xml', 'Seed439235.3.796.xml']
excludes = ['Seed266940.5.xml']

# Define a timeout handler
class TimeoutException(Exception): pass

def timeout_handler(signum, frame):
    raise TimeoutException

# Apply the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)

count = 1
for f in seeds:
    filename = str(f)+'_training_data_optgp_1.csv'
    if filename not in os.listdir():
        print("Loading model " + str(count) + " in...")
        # Set a 60-second alarm
        signal.alarm(10)
        try:
            start_time = time.time()
            model = read_sbml_model(f)
            # Cancel the alarm after successful execution
            signal.alarm(0)
            end_time = time.time()
            print(f"Model {count} loaded in {end_time - start_time} seconds.")

            print('Beginning sampling for model ', f)
            optgp = OptGPSampler(model, processes=4)

            i = 0
            for s in optgp.batch(5000, 4):
                i = i+1
                print("Saving out OptGP sampling", i)
                s.to_csv(str(f)+'_training_data_optgp_'+str(i)+'.csv')
                
            count = count + 1
        except TimeoutException:
            print("Model loading exceeded 60 seconds, skipping...")
        except Exception as e:
            print(f'Model not valid or error occurred, skipping... Error: {str(e)}')