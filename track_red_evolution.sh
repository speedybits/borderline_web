#!/bin/bash
echo "=== RED EVOLUTION (Blue Strategy Locked) ===" > red_evolution_results.txt
echo "Target: Red achieves 90%+ win rate" >> red_evolution_results.txt
echo "" >> red_evolution_results.txt

for gen in {21..40}; do
  echo "Generation $gen..."
  result=$(python3 test_current_generation.py 2>&1 | tail -1)
  
  red=$(echo $result | grep -oP 'Red: \K\d+')
  blue=$(echo $result | grep -oP 'Blue: \K\d+')
  
  if [ ! -z "$red" ] && [ ! -z "$blue" ]; then
    total=$((red + blue))
    if [ $total -gt 0 ]; then
      win_rate=$((red * 100 / total))
      echo "Gen $gen: Red $red, Blue $blue (Red win rate: $win_rate%)" | tee -a red_evolution_results.txt
      
      if [ $win_rate -ge 90 ]; then
        echo "🎯 TARGET ACHIEVED! Red wins $win_rate% of decisive games!" | tee -a red_evolution_results.txt
        break
      fi
    else
      echo "Gen $gen: Red $red, Blue $blue (No decisive games)" | tee -a red_evolution_results.txt
    fi
  fi
done
