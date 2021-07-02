import statistics

referencias = [100,200,150,300,-100,-200,-150,-300]

j1 = [28691,24661, 26658, 20541, 36663, 40738, 38707,44775]

j3 = [29046, 24699, 26797, 20378, 37020, 41055,39038,45357]

j4 = [32497,32050,32252,31614,33434,33892,33658,34345]

refs_j2 = [-150, -300, -400, 150, 300, 400]

j2 = [34850, 36869, 38238, 30821, 28762, 27437]


media = []
for l in [j1,j3,j4]:
    
    for i in range(len(referencias)):
        results = []
        for j in range(len(l)):
            if l[i] == l[j]:
                continue
            
            else:
                dif_dato = l[i] - l[j]
                dif_ref = referencias[i] - referencias[j]
                ref_per_count = abs(dif_ref/dif_dato)

                results.append(ref_per_count)

    media.append(statistics.mean(results))


for i in range(len(refs_j2)):

    results = []

    for j in range(len(j2)):
        if j2[i] == j2[j]:
            continue

        else:
            dif_dato = j2[i] - j2[j]
            dif_ref = referencias[i] - referencias[j]
            ref_per_count = abs(dif_ref/dif_dato)

            results.append(ref_per_count)


media.append(statistics.mean(results))

print(media)

