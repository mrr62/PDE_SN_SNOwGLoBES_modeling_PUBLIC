#runs in bash environment, run using command "./run_all_SN_pinched_ARGON" 
#!/bin/bash

# Run supernova.pl on all pinched_*.dat files for chosen detector

#set input file directory - modify to your personal file path that leads to the directory you are storing your pinched flux files outputted from the pinched.cc fct
flux_dir="your/file/path/snowglobes/fluxes/PDE_pinched_flux_files" #this variable allows for the input file directory to be flexible and easily changed :) 

#argon detector setup
for i in {0..1099}
do
    if [ -f "$flux_dir/pinched_${i}.dat" ]; then
        echo "▶ Running supernova.pl on pinched_${i}.dat"
        # Pass only 'pinched_${i}' (no extra 'fluxes/' in the argument)      
        cp "$flux_dir/pinched_${i}.dat" fluxes/ # Copy to working fluxes directory
        ./supernova.pl 0 pinched_${i} argon ar40kt #ARGON --> command is in form ./supernova.pl [run mode] [input files] [detector material] [detector name] 
    else
        echo "⚠️  File $flux_dir/pinched_${i}.dat not found, skipping..."
    fi
done
