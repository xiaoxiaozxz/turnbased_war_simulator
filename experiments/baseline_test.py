import sys
import os

# Get the directory where the current file is located (experiments)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root directory turn_battle_sim)
parent_dir = os.path.dirname(current_dir)

# Add the project root directory to the system path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import random, time, csv
import matplotlib.pyplot as plt
from ai.agents import CRandomAgent
from simulator_env.simulator import CBattleSimulator, SimulateBattle
from core.unit import PLAYER_CAMP,MONSTER_CAMP

N = 1000
oPlayerAgent = CRandomAgent()
oMonsterAgent = CRandomAgent()

iWinsPlayer = 0
iWinsMonster = 0
iDraws = 0
iTurnsList = []

random.seed(42)
start = time.perf_counter()

for i in range(N):
    iWinner, iTurn = SimulateBattle(oPlayerAgent, oMonsterAgent, iMaxTurns=13)
    iTurnsList.append(iTurn)
    if iWinner == PLAYER_CAMP:
        iWinsPlayer += 1
    elif iWinner == MONSTER_CAMP:
        iWinsMonster += 1
    else:
        iDraws += 1

elapsed = time.perf_counter() - start

print(f"完成 {N} 场，耗时 {elapsed:.2f} 秒")
print(f"玩家胜: {iWinsPlayer} ({iWinsPlayer/N*100:.1f}%)")
print(f"怪物胜: {iWinsMonster} ({iWinsMonster/N*100:.1f}%)")
print(f"平局: {iDraws} ({iDraws/N*100:.1f}%)")
print(f"平均回合: {sum(iTurnsList)/N:.1f}")

# save CSV
with open('docs/phase1/baseline.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['game_id', 'winner', 'turns'])
    for i, t in enumerate(iTurnsList):
        winner_str = 'player' if iTurnsList else 'monster' if iTurnsList else 'draw'
        writer.writerow([i, winner_str, t])

import matplotlib.pyplot as plt
plt.bar(['Player Win','Monster Win','Draw'], [iWinsPlayer, iWinsMonster, iDraws])
plt.title('Random Baseline (1000 games)')
plt.savefig('docs/phase1/baseline_hist.png')
plt.show()