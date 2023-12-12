"""
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from collections import namedtuple
from functools import cache


seed_soil = namedtuple("seed_soil", "target, source, r")
soil_fertilizer = namedtuple("soil_fertilizer", "target, source, r")
fertilizer_water = namedtuple("fertilizer_water", "target, source, r")
water_light = namedtuple("water_light", "target, source, r")
light_temp = namedtuple("light_temp", "target, source, r")
temp_humidity = namedtuple("temp_humidity", "target, source, r")
humidity_loc = namedtuple("humidity_loc", "target, source, r")

seeds = "432986705 28073546 1364097901 88338513 2733524843 234912494 3151642679 224376393 485709676 344068331 1560394266 911616092 3819746175 87998136 892394515 435690182 4218056486 23868437 848725444 8940450".split()
# seeds = "79 14 55 13".split()
seeds = list(map(int, seeds))


def get_mapping(mapping_str, value):
    return [value(*x.split()) for x in mapping_str.strip().split("\n")]

# seed_to_soil_str = """
# 50 98 2
# 52 50 48
# """
seed_to_soil_str = """
748585809 2125564114 88980459
1317392128 775565564 217595062
1218610825 676784261 98781303
954230685 2235762425 141777617
2920242079 4081180892 51765553
2972007632 3159586797 16102841
0 2377540042 17565155
2834452876 3712797875 58062179
2892515055 2917079842 6424918
3327351062 3175689638 162608005
673338549 647264576 29519685
1197392973 2214544573 21217852
738232750 116664417 10353059
2988110473 2429807442 71556277
17565155 334379348 277510712
1700771639 228674051 105705297
3059666750 4132946445 162020851
1806476936 993160626 588628261
1096008302 127289380 101384671
622123656 1908836676 50942989
3221687601 3338297643 28028532
2408505336 3770860054 310320838
4175210607 3039830108 119756689
3326652416 3039131462 698646
2898939973 2408505336 21302106
673066645 127017476 271904
3489959067 3382623558 330174317
702858234 611890060 35374516
4086270124 2562002619 88940483
837566268 0 116664417
1534987190 1959779665 165784449
2718826174 2923504760 115626702
3249716133 3366326175 16297383
3820133384 2650943102 266136740
3266013516 2501363719 60638900
295075867 1581788887 327047789
"""

seed_to_soil_mapping = get_mapping(seed_to_soil_str, seed_soil)

# soil_to_fertilizer_str = """
# 0 15 37
# 37 52 2
# 39 0 15
# """
soil_to_fertilizer_str = """
2018515973 2192795257 82329405
3722326327 3015971185 249665840
3046459770 3689390318 25519185
3971992167 3265637025 40217941
3071978955 3453653215 203407731
0 443504340 17965088
584437096 1722124969 470670288
1055107384 744431503 164966659
1489299099 461469428 282962075
2321848831 2380372526 153650776
2100845378 269225056 174279284
3487660258 2648616968 234666069
3275386686 3305854966 147798249
1772261174 1172578553 246254799
4012210108 2883283037 132688148
3423184935 4138946628 64475323
4144898256 2321848831 58523695
538253726 1418833352 46183370
1220074043 0 269225056
17965088 909398162 263180391
2590093273 3657060946 32329372
281145479 1465016722 257108247
2622422645 3714909503 424037125
2475499607 2534023302 114593666
"""

soil_to_fertilizer_mapping = get_mapping(soil_to_fertilizer_str, soil_fertilizer)

# fertilizer_to_water_str = """
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4
# """

fertilizer_to_water_str = """
3731805434 353192162 37567806
926873139 889685769 255250442
3170336676 695153543 194532226
679924479 451681440 193671776
3009343704 3081959489 160992972
1242360754 3579359343 278026518
1861131448 2500688596 20068354
4028837903 4006213119 266129393
1182123581 3242952461 60237173
3877550443 645353216 49800327
2223776164 1371077033 341527178
3364868902 2566566565 36440100
1773121333 0 76664401
264823995 2444756861 55931735
3929841219 3857385861 27802851
2166799431 1712604211 56976733
873596255 1769580944 53276884
645696746 3047731756 34227733
3927350770 3955153621 2490449
3769373240 177937131 108177203
0 3314535348 264823995
1942121274 3885188712 69964909
1881199802 390759968 60921472
1849785734 3303189634 11345714
3401309002 2855740726 104355610
2079164011 2960096336 87635420
544424016 76664401 101272730
2565303342 2520756950 45809615
1520387272 2603006665 252734061
2012086183 286114334 67077828
2611112957 1822857828 398230747
320755730 2221088575 223668286
3505664612 1144936211 226140822
4006213119 4272342512 22624784
"""

fertilizer_to_water_mapping = get_mapping(fertilizer_to_water_str, fertilizer_water)

# water_to_light_str = """
# 88 18 7
# 18 25 70
# """
water_to_light_str = """
62780592 544346201 30115959
2740764032 1352944740 34082945
377487729 807592920 35446631
1316419610 1454554942 34907962
986581913 756881718 50711202
4167758628 3240047125 127208668
818809239 1222506283 58684750
3649838514 2036598113 6212644
127663629 0 10715051
3023280854 1435387310 19167632
663070842 10715051 124076893
2774846977 2422700597 37614763
1812617371 2460315360 5121443
1640337506 1864318248 172279865
2986755724 1316419610 36525130
2023334670 2467203928 540327060
1159184084 248462172 14557802
1037293115 152894449 95567723
0 134791944 18102505
18102505 712203631 44678087
465375803 972369801 197695039
2576394916 3007530988 65274194
92896551 1281191033 34767078
3656051158 4289142647 5824649
412934360 1170064840 52441443
3417303830 3873138614 84580361
787147735 263019974 31661504
1817738814 2042810757 205595856
1285160111 843039551 30798000
2563661730 3123136764 12733186
138378680 305237152 239109049
3648071389 2465436803 1767125
1132860838 574462160 26323246
888049663 873837551 98532250
3626039273 3072805182 22032116
3530183657 4193287031 95855616
1404769450 3957718975 235568056
3042448486 1489462904 374855344
2641669110 1387027685 48359625
877493989 294681478 10555674
3501884191 3094837298 28299466
1351327572 3186605247 53441878
2690028735 3135869950 50735297
2812461740 2248406613 174293984
3661875807 3367255793 505882821
1173741886 600785406 111418225
"""

water_to_light_mapping = get_mapping(water_to_light_str, water_light)

# light_to_temperature_str = """
# 45 77 23
# 81 45 19
# 68 64 13
# """
light_to_temperature_str = """
964570004 989608620 226759942
2204148775 2545437438 20646474
233260112 338444213 39032265
958191857 332066066 6378147
2318799855 914518254 75090366
4247140372 3146297568 47826924
2224795249 1216368562 94004606
2871022952 1310373168 80313918
1400254919 233260112 98805954
445493256 487550555 149554087
2576473348 3962746668 294549604
3535295748 2775008885 371288683
1499060873 377476478 110074077
272292377 2215619580 173200879
3347481948 1867953550 157067409
4161267146 3794452372 85873226
3504549357 2184873189 30746391
1759636962 1780717197 87236353
2951336870 2388820459 6114967
1191329946 2566083912 208924973
1884544339 3880325598 82421070
595047343 3431307858 363144514
2393890221 731935127 182583127
4001414916 2025020959 159852230
2957451837 1390687086 390030111
1846873315 4257296272 37671024
1966965409 3194124492 237183366
1609134950 2394935426 150502012
3906584431 637104642 94830485
"""

light_to_temperature_mapping = get_mapping(light_to_temperature_str, light_temp)

# temperature_to_humidity_str = """
# 0 69 1
# 1 0 69
# """
temperature_to_humidity_str = """
1406768592 2335526312 13344484
666958498 1862550129 472976183
558853371 843618476 74696086
1168798622 129171378 168640618
1713291209 297811996 183431863
1993628008 635748116 152317885
2560263686 2849350774 11516524
32266442 1212766321 287276323
2571780210 3319898101 11192927
375095240 995599149 183758131
2661986290 2353962919 50829838
3252020768 4280298713 14668583
1337439240 1793220777 69329352
3419718116 3502299739 574454544
2353962919 2650392505 198958269
633549457 1179357280 33409041
2582973137 4076754283 50515665
319542765 788066001 55552475
1896723072 32266442 96904936
1420113076 1500042644 293178133
3006421020 2404792757 245599748
2842554807 3331091028 163866213
2633488802 2990605977 28497488
2300450150 947178503 48420646
3266689351 4127269948 153028765
2145945893 481243859 154504257
3994172660 3019103465 300794636
1139934681 918314562 28863941
2712816128 2860867298 129738679
2552921188 3494957241 7342498
"""

temperature_to_humidity_mapping = get_mapping(temperature_to_humidity_str, temp_humidity)

# humidity_to_location_str = """
# 60 56 37
# 56 93 4
# """
humidity_to_location_str = """
897459980 3171885613 268595078
506368722 1864971513 13322696
1166055058 2803961444 53745388
2572095034 667166679 114420176
687118932 1725187165 139784348
2478398695 0 14138781
3427672233 370325921 251085897
3888215738 3612891343 82449665
1674720770 1530101168 79955344
3970665403 925512154 2812137
519691418 2452425610 167427514
3884704963 3168374838 3510775
826903280 2381868910 70556700
2399774019 349568762 20757159
2972099388 3465151802 147739541
1754676114 131614075 217954687
2865104023 3440480691 24671111
2206760431 932309368 77882935
2284643366 1610056512 115130653
2492537476 14138781 35151040
2527688516 3695341008 44406518
3119838929 781586855 143925299
2732270071 2857706832 132833952
1599442846 2728683520 75277924
3263764228 3995626854 27783181
0 2990540784 177834054
2686515210 621411818 45754861
2420531178 2670816003 57867517
1219800446 1010192303 191374197
3678758130 3789680021 205946833
3973477540 3739747526 49932495
1972630801 2014419033 234129630
3291547409 1878294209 136124824
2889775134 49289821 82324254
1411174643 2619853124 50962879
1466122599 2248548663 133320247
177834054 1201566500 328534668
1462137522 928324291 3985077
"""

humidity_to_location_mapping = get_mapping(humidity_to_location_str, humidity_loc)


def get_destination(mappings, seek_val):
    for ma in mappings:
        _source = int(ma.source)
        _target = int(ma.target)
        _range = int(ma.r)
        # print(_source, _target, _range, _target + _range, seek_val)
        if seek_val == _source:
            return _target
        
        elif seek_val <= (_source + _range) and seek_val > _source:
            return _target + seek_val - _source
        
        else:
            continue
    
    return seek_val

def get_min_location(_seeds):
    locations = []
    for seed in _seeds:
        soil = get_destination(seed_to_soil_mapping, seed)
        fertilizer = get_destination(soil_to_fertilizer_mapping, soil)
        water = get_destination(fertilizer_to_water_mapping, fertilizer)
        light = get_destination(water_to_light_mapping, water)
        temperature = get_destination(light_to_temperature_mapping, light)
        humidity = get_destination(temperature_to_humidity_mapping, temperature)
        location = get_destination(humidity_to_location_mapping, humidity)

        locations.append(location)
        # print(f"{seed} -> {soil} -> {fertilizer} -> {water} -> {light} -> {temperature} -> {humidity} -> {location}")

        # print(soil)
    return min(locations)

def part1():
    return get_min_location(seeds)

"""
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""

def part2():
    _seeds = []
    for i in range(0, len(seeds), 2):
        for j in range(seeds[i + 1]):
            _seeds.append(seeds[i] + j)
    # print(_seeds)
    return get_min_location(_seeds)

if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)