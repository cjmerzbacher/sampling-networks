import cobra
from cobra.io import load_model
from cobra.sampling import sample
from cobra.sampling import OptGPSampler, ACHRSampler

print("Loading model in...")
# load core model
model = load_model("textbook")

achr = ACHRSampler(model) #thinning/step size set to 100 automatically
optgp = OptGPSampler(model, processes=4)

i = 0
for s in optgp.batch(10000, 10):
    i = i+1
    print("Saving out OptGP sampling", i)
    s.to_csv('training_data_optgp'+str(i)+'.csv')

i = 0
print("Running ACHR sampling...")
for s in optgp.batch(10000, 10):
    i = i+1
    print("Saving out ACHR sampling", i)
    s.to_csv('training_data_achr'+str(i)+'.csv')

