iteration=3
scenario='multi_03'
log_file="result_${scenario}_demab0.log"
result_file="result_${scenario}_demab0.txt"
csv_file="result_${scenario}_demab0"
sampler_idx=0 # 0 / 1 / 2 / -1 (-1 is for alternate)
sampler_type=demab # demab / dmab / random / dce / halton / udemab
exploration_ratio=2.0
simulator=scenic.simulators.metadrive.model
use_dynamic_rulebook=false # true / false (false is for a monolithic rulebook)
simulation_steps=300

rm $scenario/outputs/$log_file
rm $scenario/outputs/$result_file
rm $scenario/outputs/$csv_file.*csv
rm $scenario/outputs/$csv_file\_scatter.png
if [ "$use_dynamic_rulebook" = true ]; then

    for seed in $(seq 0 2);
    do
        python $scenario/$scenario.py -n $iteration --headless -e $csv_file.$seed -sp $scenario/$scenario.scenic -gp $scenario/ -rp $scenario/$scenario\_spec.py -s $sampler_type --seed $seed --using-sampler $sampler_idx -m $simulator --max-simulation-steps $simulation_steps -co $scenario/outputs --exploration-ratio $exploration_ratio >> $scenario/outputs/$log_file
    done

    python $scenario/util/$scenario\_collect_result.py $scenario/outputs/$log_file multi $sampler_idx >> $scenario/outputs/$result_file
    python $scenario/util/$scenario\_analyze_diversity.py $scenario/outputs/ $csv_file multi >> $scenario/outputs/$result_file

else

    for seed in $(seq 0 2);
    do
        python $scenario/$scenario.py -n $iteration --headless -e $csv_file.$seed -sp $scenario/$scenario.scenic --single-graph -gp $scenario/$scenario.sgraph -rp $scenario/$scenario\_spec.py -s $sampler_type --seed $seed --using-sampler $sampler_idx -m $simulator --max-simulation-steps $simulation_steps -co $scenario/outputs --exploration-ratio $exploration_ratio >> $scenario/outputs/$log_file
    done

    python $scenario/util/$scenario\_collect_result.py $scenario/outputs/$log_file single $sampler_idx >> $scenario/outputs/$result_file
    python $scenario/util/$scenario\_analyze_diversity.py $scenario/outputs/ $csv_file single >> $scenario/outputs/$result_file
fi
