import numpy as np
import matplotlib.pyplot as plt

# Sabit Parametreler
DpS = 5
UnitHp = 100
EnemyInitialUnitCount = 100
EnemyDpS = 5
EnemyUnitHp = 100
dt = 1
T = 60

# InitialUnitCount aralığı
InitialUnitCount_list = np.arange(5, 300, 1)  # 5'ten 40'a kadar, 2 artarak
survivors = []

for InitialUnitCount in InitialUnitCount_list:
    unit_count = [InitialUnitCount]
    enemy_unit_count = [EnemyInitialUnitCount]
    total_damage_output = [0]
    total_damage_taken = [0]

    for t in range(1, T+1):
        curr_unit_count = unit_count[-1]
        curr_enemy_unit_count = enemy_unit_count[-1]

        if curr_unit_count <= 0 or curr_enemy_unit_count <= 0:
            unit_count.append(max(curr_unit_count, 0))
            enemy_unit_count.append(max(curr_enemy_unit_count, 0))
            total_damage_output.append(total_damage_output[-1])
            total_damage_taken.append(total_damage_taken[-1])
            continue

        damage_output = curr_unit_count * DpS * dt
        damage_taken = curr_enemy_unit_count * EnemyDpS * dt

        total_damage_output.append(total_damage_output[-1] + damage_output)
        total_damage_taken.append(total_damage_taken[-1] + damage_taken)

        next_unit_count = InitialUnitCount - total_damage_taken[-1] / UnitHp
        next_enemy_unit_count = EnemyInitialUnitCount - total_damage_output[-1] / EnemyUnitHp

        unit_count.append(max(next_unit_count, 0))
        enemy_unit_count.append(max(next_enemy_unit_count, 0))

    survivors.append(unit_count[-1])

plt.figure(figsize=(8,5))
plt.plot(InitialUnitCount_list, survivors, marker='o')
plt.title('Başlangıç Birim Sayısı vs Savaş Sonunda Hayatta Kalan Birim Sayısı')
plt.xlabel('Başlangıç Birim Sayısı (InitialUnitCount)')
plt.ylabel('Hayatta Kalan Birim Sayısı')
plt.grid(True)
plt.show()
