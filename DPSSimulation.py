import numpy as np
import matplotlib.pyplot as plt

# Sabit Parametreler
InitialUnitCount = 100
UnitHp = 100
EnemyInitialUnitCount = 100
EnemyDpS = 10
EnemyUnitHp = 50
dt = 1
T = 60

# DpS değerleri aralığı
DpS_list = np.arange(1, 20, 1)  # 2'den 15'e kadar

survivors = []

for DpS in DpS_list:
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
plt.plot(DpS_list, survivors, marker='o')
plt.title('DpS vs Savaş Sonunda Hayatta Kalan Birim Sayısı')
plt.xlabel('DpS (Birim Başına Saniyelik Hasar)')
plt.ylabel('Hayatta Kalan Birim Sayısı')
plt.grid(True)
plt.show()
