iteration=3
scenario='multi_04'
log_file="result_${scenario}_demab.log"
result_file="result_${scenario}_demab.txt"
csv_file="result_${scenario}_demab"
sampler_idx=0 # 0 / 1 / -1 (-1 is for alternate)
sampler_type=demab # demab / dmab / random / dce / halton / udemab
simulator=scenic.simulators.metadrive.model
simulation_steps=200

rm $scenario/outputs/$log_file
rm $scenario/outputs/$result_file
rm $scenario/outputs/$csv_file.*csv
rm $scenario/outputs/$csv_file\_scatter.png
for seed in $(seq 0 2);
do
    python $scenario/$scenario.py -n $iteration --headless -e $csv_file.$seed -sp $scenario/$scenario.scenic -gp $scenario/ -rp $scenario/$scenario\_spec.py -s $sampler_type --seed $seed --using-sampler $sampler_idx -m $simulator --max-simulation-steps $simulation_steps -co $scenario/outputs >> $scenario/outputs/$log_file
done
python $scenario/util/$scenario\_collect_result.py $scenario/outputs/$log_file multi $sampler_idx >> $scenario/outputs/$result_file
python $scenario/util/$scenario\_analyze_diversity.py $scenario/outputs/ $csv_file multi >> $scenario/outputs/$result_file
