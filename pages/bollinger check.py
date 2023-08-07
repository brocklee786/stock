import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt

# 銘柄コードの指定
#symbol = "7203.T"  # 例としてApple Inc. (AAPL)を使用
codes = [1332, 1376, 1379, 1380, 1382, 1384, 1400, 1401, 1417, 1418, 1420, 1429, 1430, 1431, 1433, 1434, 1435, 1436, 1438, 1439, 1443, 1446, 1447, 1451, 1491, 1514, 1605, 1711, 1712, 1716, 1717, 1719, 1720, 1724, 1726, 1730, 1739, 1743, 1757, 1768, 1770, 1776, 1780, 1783, 1786, 1789, 1799, 1802, 1803, 1805, 1808, 1810, 1813, 1814, 1815, 1821, 1826, 1827, 1828, 1840, 1841, 1844, 1847, 1848, 1850, 1853, 1860, 1867, 1870, 1871, 1873, 1879, 1887, 1890, 1893, 1898, 1905, 1909, 1914, 1921, 1926, 1929, 1930, 1934, 1938, 1942, 1944, 1945, 1960, 1961, 1963, 1964, 1965, 1966, 1967, 1971, 1973, 1976, 1981, 1992, 1994, 1997, 2001, 2002, 2009, 2053, 2055, 2060, 2107, 2108, 2112, 2114, 2120, 2122, 2127, 2130, 2134, 2136, 2138, 2139, 2148, 2150, 2152, 2153, 2156, 2157, 2158, 2160, 2162, 2163, 2164, 2168, 2169, 2170, 2173, 2179, 2180, 2183, 2185, 2186, 2193, 2195, 2196, 2198, 2207, 2215, 2216, 2266, 2270, 2286, 2288, 2291, 2296, 2300, 2301, 2303, 2304, 2307, 2309, 2311, 2315, 2317, 2321, 2323, 2329, 2330, 2331, 2332, 2335, 2337, 2338, 2340, 2341, 2342, 2344, 2345, 2349, 2351, 2353, 2354, 2359, 2370, 2372, 2373, 2374, 2375, 2376, 2378, 2385, 2388, 2389, 2391, 2393, 2397, 2402, 2404, 2408, 2410, 2411, 2412, 2415, 2418, 2424, 2425, 2427, 2428, 2432, 2433, 2435, 2436, 2437, 2438, 2440, 2445, 2449, 2453, 2454, 2459, 2461, 2462, 2464, 2468, 2469, 2471, 2479, 2480, 2481, 2483, 2484, 2485, 2487, 2488, 2489, 2491, 2492, 2493, 2497, 2499, 2531, 2533, 2540, 2579, 2586, 2597, 2599, 2607, 2613, 2652, 2654, 2656, 2666, 2667, 2668, 2673, 2674, 2681, 2683, 2686, 2687, 2689, 2693, 2694, 2706, 2708, 2715, 2721, 2722, 2730, 2734, 2735, 2736, 2743, 2749, 2750, 2752, 2754, 2762, 2763, 2764, 2769, 2776, 2778, 2788, 2789, 2790, 2792, 2795, 2796, 2804, 2806, 2812, 2814, 2816, 2818, 2820, 2874, 2876, 2877, 2883, 2884, 2894, 2901, 2903, 2904, 2907, 2908, 2910, 2915, 2916, 2917, 2922, 2924, 2926, 2927, 2929, 2930, 2931, 2933, 2935, 2936, 2970, 2975, 2978, 2982, 2983, 2984, 2987, 2991, 2997, 2999, 3001, 3003, 3004, 3010, 3011, 3021, 3023, 3024, 3028, 3030, 3031, 3034, 3035, 3036, 3040, 3041, 3042, 3045, 3048, 3050, 3053, 3054, 3058, 3059, 3063, 3064, 3065, 3067, 3069, 3070, 3071, 3073, 3075, 3077, 3079, 3080, 3082, 3083, 3086, 3089, 3093, 3094, 3096, 3099, 3101, 3103, 3105, 3109, 3111, 3113, 3121, 3123, 3133, 3134, 3135, 3137, 3138, 3140, 3143, 3151, 3153, 3154, 3157, 3159, 3160, 3161, 3166, 3167, 3168, 3169, 3172, 3173, 3174, 3175, 3176, 3178, 3179, 3181, 3183, 3185, 3187, 3189, 3190, 3191, 3192, 3195, 3196, 3197, 3199, 3201, 3202, 3204, 3205, 3222, 3223, 3224, 3228, 3232, 3236, 3237, 3238, 3241, 3242, 3245, 3246, 3248, 3252, 3254, 3261, 3264, 3266, 3267, 3271, 3275, 3276, 3277, 3280, 3284, 3286, 3289, 3293, 3294, 3297, 3299, 3300, 3302, 3306, 3315, 3316, 3317, 3319, 3320, 3321, 3322, 3323, 3326, 3329, 3333, 3341, 3347, 3350, 3352, 3355, 3358, 3359, 3361, 3370, 3371, 3372, 3375, 3377, 3386, 3387, 3388, 3392, 3393, 3395, 3396, 3401, 3402, 3405, 3407, 3409, 3415, 3416, 3417, 3418, 3420, 3421, 3422, 3423, 3426, 3433, 3434, 3435, 3439, 3440, 3441, 3444, 3447, 3449, 3452, 3454, 3457, 3458, 3461, 3464, 3467, 3469, 3474, 3475, 3477, 3482, 3484, 3486, 3489, 3491, 3494, 3495, 3497, 3512, 3513, 3521, 3524, 3526, 3529, 3536, 3537, 3538, 3539, 3541, 3542, 3544, 3546, 3547, 3548, 3550, 3551, 3553, 3556, 3557, 3558, 3559, 3562, 3565, 3566, 3571, 3577, 3580, 3583, 3598, 3600, 3604, 3607, 3608, 3611, 3612, 3622, 3623, 3624, 3625, 3627, 3632, 3633, 3634, 3639, 3640, 3641, 3645, 3646, 3647, 3648, 3649, 3653, 3655, 3656, 3657, 3660, 3661, 3662, 3663, 3664, 3665, 3666, 3667, 3668, 3670, 3671, 3672, 3673, 3674, 3675, 3676, 3677, 3678, 3679, 3680, 3681, 3682, 3683, 3686, 3687, 3688, 3690, 3691, 3692, 3694, 3696, 3698, 3710, 3719, 3723, 3726, 3727, 3738, 3744, 3747, 3750, 3753, 3758, 3762, 3763, 3766, 3768, 3770, 3772, 3773, 3776, 3777, 3778, 3779, 3782, 3784, 3787, 3793, 3796, 3799, 3800, 3802, 3803, 3804, 3807, 3810, 3814, 3815, 3816, 3823, 3825, 3826, 3834, 3835, 3836, 3837, 3839, 3840, 3841, 3842, 3843, 3844, 3845, 3848, 3850, 3851, 3852, 3853, 3857, 3858, 3861, 3863, 3864, 3865, 3877, 3878, 3880, 3892, 3895, 3896, 3900, 3902, 3903, 3904, 3905, 3907, 3908, 3909, 3910, 3911, 3912, 3913, 3916, 3917, 3918, 3920, 3921, 3922, 3924, 3926, 3927, 3928, 3929, 3930, 3931, 3933, 3934, 3935, 3936, 3937, 3939, 3940, 3941, 3945, 3947, 3951, 3953, 3954, 3955, 3961, 3963, 3964, 3965, 3967, 3968, 3969, 3970, 3974, 3976, 3978, 3979, 3981, 3983, 3985, 3986, 3987, 3988, 3989, 3990, 3992, 3995, 3996, 3997, 3998, 4005, 4012, 4013, 4014, 4015, 4016, 4017, 4019, 4020, 4026, 4027, 4028, 4031, 4042, 4045, 4047, 4052, 4053, 4054, 4056, 4057, 4058, 4059, 4060, 4064, 4069, 4073, 4075, 4076, 4078, 4080, 4082, 4088, 4092, 4093, 4094, 4095, 4097, 4098, 4099, 4102, 4113, 4124, 4165, 4166, 4167, 4168, 4169, 4170, 4171, 4172, 4173, 4174, 4175, 4176, 4177, 4178, 4179, 4180, 4188, 4192, 4196, 4199, 4200, 4202, 4205, 4215, 4218, 4220, 4222, 4224, 4228, 4231, 4234, 4237, 4238, 4240, 4241, 4242, 4243, 4245, 4246, 4247, 4248, 4251, 4255, 4256, 4259, 4260, 4262, 4263, 4265, 4267, 4268, 4272, 4274, 4275, 4284, 4286, 4287, 4288, 4290, 4293, 4295, 4298, 4299, 4301, 4304, 4308, 4312, 4316, 4317, 4319, 4320, 4326, 4331, 4333, 4335, 4341, 4344, 4345, 4346, 4347, 4350, 4351, 4355, 4356, 4360, 4361, 4366, 4370, 4372, 4374, 4375, 4376, 4378, 4379, 4380, 4384, 4386, 4387, 4388, 4389, 4391, 4392, 4394, 4395, 4397, 4398, 4404, 4406, 4409, 4410, 4412, 4415, 4416, 4418, 4419, 4420, 4421, 4422, 4423, 4424, 4427, 4428, 4429, 4430, 4433, 4436, 4437, 4438, 4440, 4441, 4443, 4444, 4446, 4447, 4448, 4449, 4461, 4462, 4463, 4464, 4475, 4476, 4477, 4479, 4482, 4484, 4486, 4487, 4489, 4490, 4491, 4492, 4494, 4495, 4496, 4506, 4512, 4524, 4531, 4536, 4538, 4539, 4548, 4549, 4552, 4553, 4554, 4556, 4558, 4563, 4564, 4565, 4569, 4570, 4571, 4572, 4574, 4575, 4576, 4579, 4582, 4583, 4584, 4586, 4587, 4588, 4591, 4592, 4593, 4594, 4596, 4597, 4598, 4599, 4611, 4612, 4615, 4616, 4617, 4619, 4620, 4621, 4623, 4625, 4627, 4629, 4633, 4636, 4642, 4644, 4645, 4650, 4651, 4657, 4658, 4662, 4664, 4666, 4668, 4671, 4674, 4676, 4678, 4679, 4680, 4687, 4689, 4691, 4705, 4707, 4708, 4709, 4712, 4714, 4718, 4720, 4722, 4725, 4728, 4735, 4736, 4743, 4745, 4750, 4751, 4752, 4754, 4755, 4760, 4761, 4762, 4765, 4766, 4767, 4769, 4770, 4772, 4777, 4781, 4783, 4784, 4792, 4800, 4809, 4813, 4814, 4820, 4824, 4826, 4829, 4833, 4837, 4838, 4839, 4840, 4845, 4847, 4881, 4882, 4883, 4884, 4885, 4886, 4888, 4889, 4890, 4891, 4892, 4893, 4902, 4912, 4917, 4918, 4920, 4923, 4926, 4929, 4931, 4932, 4934, 4935, 4936, 4951, 4955, 4957, 4960, 4963, 4968, 4972, 4974, 4977, 4978, 4979, 4987, 4990, 4992, 4996, 4997, 4998, 5009, 5010, 5011, 5013, 5015, 5017, 5018, 5020, 5025, 5026, 5027, 5028, 5029, 5031, 5033, 5035, 5036, 5070, 5071, 5074, 5076, 5103, 5105, 5110, 5121, 5125, 5126, 5129, 5131, 5133, 5134, 5138, 5142, 5161, 5162, 5185, 5187, 5191, 5194, 5195, 5199, 5202, 5204, 5208, 5210, 5212, 5216, 5218, 5237, 5240, 5243, 5244, 5246, 5255, 5258, 5259, 5262, 5268, 5269, 5271, 5277, 5279, 5280, 5282, 5284, 5285, 5287, 5288, 5290, 5301, 5333, 5337, 5341, 5355, 5357, 5363, 5367, 5368, 5380, 5381, 5386, 5388, 5391, 5406, 5408, 5423, 5440, 5446, 5449, 5458, 5461, 5476, 5484, 5491, 5527, 5541, 5542, 5563, 5570, 5571, 5580, 5603, 5609, 5610, 5612, 5632, 5658, 5660, 5697, 5698, 5699, 5702, 5703, 5704, 5707, 5715, 5721, 5724, 5727, 5742, 5759, 5781, 5802, 5803, 5805, 5809, 5816, 5817, 5819, 5821, 5830, 5831, 5832, 5838, 5852, 5856, 5857, 5884, 5900, 5902, 5903, 5905, 5906, 5909, 5915, 5928, 5929, 5930, 5932, 5933, 5936, 5938, 5940, 5941, 5942, 5943, 5949, 5950, 5951, 5952, 5955, 5956, 5957, 5958, 5959, 5962, 5965, 5967, 5969, 5970, 5973, 5974, 5975, 5976, 5981, 5984, 5985, 5986, 5987, 5989, 5990, 5991, 5992, 5994, 5997, 5998, 6013, 6018, 6022, 6023, 6029, 6031, 6032, 6033, 6034, 6035, 6037, 6038, 6039, 6040, 6044, 6045, 6046, 6047, 6048, 6049, 6054, 6058, 6059, 6060, 6062, 6063, 6069, 6071, 6072, 6073, 6074, 6078, 6081, 6082, 6083, 6085, 6086, 6088, 6089, 6090, 6091, 6092, 6093, 6094, 6095, 6096, 6099, 6101, 6113, 6118, 6121, 6131, 6136, 6138, 6140, 6143, 6144, 6147, 6149, 6151, 6155, 6156, 6157, 6158, 6159, 6161, 6164, 6165, 6166, 6167, 6171, 6173, 6176, 6177, 6178, 6181, 6182, 6183, 6184, 6185, 6186, 6188, 6189, 6190, 6192, 6193, 6194, 6195, 6197, 6198, 6199, 6200, 6203, 6208, 6210, 6217, 6218, 6222, 6226, 6227, 6229, 6232, 6233, 6237, 6238, 6239, 6240, 6246, 6247, 6248, 6250, 6255, 6257, 6262, 6264, 6265, 6269, 6272, 6276, 6279, 6282, 6286, 6287, 6289, 6291, 6292, 6293, 6297, 6306, 6307, 6310, 6312, 6316, 6317, 6319, 6322, 6325, 6327, 6330, 6332, 6334, 6335, 6336, 6339, 6343, 6345, 6347, 6349, 6356, 6357, 6363, 6364, 6366, 6373, 6376, 6378, 6379, 6380, 6381, 6382, 6384, 6390, 6395, 6400, 6402, 6403, 6405, 6416, 6418, 6424, 6428, 6433, 6440, 6444, 6445, 6455, 6458, 6459, 6461, 6463, 6464, 6466, 6467, 6469, 6470, 6471, 6472, 6473, 6480, 6482, 6484, 6485, 6486, 6488, 6489, 6493, 6494, 6495, 6497, 6498, 6505, 6507, 6508, 6513, 6518, 6522, 6523, 6533, 6535, 6537, 6538, 6539, 6540, 6542, 6543, 6544, 6545, 6546, 6547, 6548, 6549, 6550, 6551, 6552, 6554, 6555, 6556, 6557, 6558, 6562, 6563, 6564, 6566, 6567, 6568, 6569, 6570, 6571, 6572, 6573, 6574, 6578, 6579, 6580, 6584, 6613, 6615, 6618, 6619, 6620, 6625, 6629, 6630, 6632, 6633, 6634, 6635, 6637, 6638, 6640, 6644, 6647, 6648, 6653, 6654, 6656, 6658, 6659, 6662, 6663, 6664, 6666, 6668, 6670, 6677, 6694, 6696, 6698, 6699, 6703, 6704, 6715, 6721, 6727, 6730, 6731, 6734, 6736, 6740, 6741, 6742, 6743, 6744, 6745, 6748, 6750, 6752, 6753, 6754, 6757, 6763, 6768, 6769, 6770, 6771, 6775, 6776, 6778, 6779, 6785, 6786, 6794, 6800, 6803, 6804, 6809, 6810, 6814, 6817, 6819, 6823, 6832, 6834, 6835, 6836, 6837, 6838, 6840, 6848, 6853, 6855, 6858, 6862, 6863, 6864, 6867, 6870, 6879, 6881, 6882, 6888, 6894, 6897, 6901, 6904, 6905, 6907, 6912, 6914, 6919, 6925, 6926, 6927, 6928, 6930, 6932, 6937, 6938, 6942, 6952, 6955, 6958, 6962, 6964, 6969, 6973, 6977, 6982, 6986, 6989, 6993, 6994, 6996, 6997, 6999, 7003, 7004, 7014, 7018, 7021, 7022, 7030, 7031, 7034, 7035, 7036, 7037, 7038, 7040, 7041, 7042, 7043, 7044, 7048, 7049, 7057, 7060, 7062, 7063, 7066, 7067, 7068, 7069, 7072, 7074, 7077, 7078, 7080, 7081, 7082, 7083, 7084, 7085, 7086, 7087, 7088, 7089, 7090, 7091, 7092, 7093, 7097, 7105, 7110, 7111, 7112, 7115, 7116, 7119, 7122, 7126, 7127, 7129, 7131, 7134, 7135, 7138, 7140, 7148, 7150, 7157, 7161, 7162, 7163, 7167, 7172, 7175, 7177, 7180, 7182, 7183, 7184, 7186, 7189, 7191, 7192, 7196, 7198, 7199, 7201, 7202, 7205, 7208, 7211, 7212, 7213, 7214, 7215, 7217, 7218, 7219, 7220, 7222, 7224, 7226, 7229, 7235, 7236, 7238, 7239, 7241, 7244, 7245, 7246, 7247, 7250, 7254, 7255, 7256, 7261, 7264, 7266, 7268, 7271, 7273, 7277, 7279, 7280, 7283, 7284, 7287, 7291, 7294, 7296, 7297, 7298, 7313, 7314, 7315, 7317, 7318, 7322, 7325, 7326, 7330, 7337, 7338, 7342, 7343, 7345, 7347, 7351, 7352, 7353, 7354, 7356, 7357, 7358, 7359, 7360, 7362, 7367, 7368, 7369, 7370, 7371, 7372, 7374, 7377, 7378, 7379, 7383, 7399, 7408, 7412, 7413, 7414, 7416, 7419, 7420, 7421, 7426, 7427, 7434, 7435, 7438, 7442, 7443, 7444, 7445, 7450, 7453, 7455, 7460, 7461, 7462, 7463, 7466, 7477, 7481, 7482, 7486, 7487, 7490, 7494, 7501, 7502, 7504, 7505, 7506, 7508, 7510, 7512, 7513, 7514, 7521, 7522, 7523, 7524, 7527, 7531, 7537, 7538, 7539, 7544, 7545, 7551, 7554, 7555, 7559, 7561, 7567, 7570, 7571, 7575, 7578, 7585, 7590, 7593, 7599, 7600, 7601, 7602, 7603, 7604, 7605, 7608, 7610, 7613, 7614, 7615, 7618, 7619, 7623, 7624, 7625, 7628, 7635, 7636, 7638, 7640, 7643, 7646, 7647, 7670, 7671, 7673, 7676, 7678, 7687, 7689, 7692, 7694, 7698, 7702, 7707, 7709, 7711, 7713, 7718, 7719, 7721, 7722, 7723, 7725, 7726, 7727, 7730, 7731, 7732, 7739, 7743, 7745, 7746, 7752, 7760, 7762, 7769, 7771, 7774, 7775, 7776, 7777, 7779, 7781, 7782, 7791, 7792, 7793, 7795, 7800, 7803, 7804, 7805, 7806, 7807, 7810, 7811, 7812, 7813, 7814, 7815, 7816, 7818, 7819, 7820, 7822, 7823, 7827, 7829, 7831, 7833, 7836, 7837, 7840, 7841, 7844, 7847, 7850, 7851, 7856, 7857, 7859, 7860, 7863, 7864, 7865, 7867, 7871, 7872, 7874, 7875, 7877, 7879, 7883, 7885, 7886, 7888, 7893, 7896, 7897, 7898, 7899, 7902, 7906, 7908, 7915, 7916, 7918, 7919, 7922, 7923, 7925, 7927, 7928, 7938, 7939, 7940, 7942, 7946, 7953, 7955, 7956, 7957, 7962, 7963, 7970, 7971, 7972, 7975, 7976, 7980, 7981, 7983, 7984, 7985, 7986, 7987, 7989, 7991, 7992, 7994, 7997, 7999, 8005, 8008, 8013, 8016, 8018, 8020, 8023, 8025, 8037, 8040, 8045, 8051, 8061, 8065, 8066, 8070, 8076, 8077, 8081, 8086, 8089, 8093, 8095, 8097, 8101, 8103, 8104, 8105, 8107, 8115, 8118, 8119, 8123, 8125, 8127, 8131, 8133, 8135, 8139, 8141, 8143, 8144, 8147, 8151, 8157, 8158, 8163, 8165, 8166, 8167, 8168, 8174, 8181, 8182, 8185, 8202, 8203, 8207, 8208, 8209, 8214, 8215, 8217, 8219, 8226, 8230, 8233, 8237, 8242, 8247, 8254, 8256, 8260, 8275, 8278, 8281, 8282, 8285, 8289, 8291, 8306, 8308, 8331, 8334, 8337, 8338, 8343, 8344, 8346, 8349, 8358, 8359, 8360, 8361, 8362, 8364, 8365, 8368, 8370, 8377, 8381, 8383, 8386, 8387, 8395, 8399, 8410, 8416, 8418, 8462, 8508, 8511, 8515, 8518, 8524, 8537, 8541, 8542, 8544, 8550, 8558, 8562, 8563, 8570, 8572, 8585, 8593, 8595, 8596, 8600, 8601, 8604, 8609, 8613, 8614, 8616, 8617, 8622, 8624, 8628, 8698, 8699, 8700, 8704, 8705, 8706, 8707, 8708, 8713, 8714, 8715, 8732, 8737, 8739, 8742, 8746, 8747, 8769, 8772, 8783, 8789, 8798, 8802, 8804, 8818, 8835, 8836, 8841, 8844, 8848, 8854, 8860, 8864, 8869, 8871, 8876, 8881, 8887, 8889, 8891, 8892, 8893, 8894, 8897, 8898, 8903, 8904, 8905, 8908, 8912, 8917, 8918, 8920, 8923, 8925, 8927, 8929, 8931, 8934, 8935, 8938, 8940, 8944, 8945, 8946, 8995, 8996, 8999, 9005, 9006, 9007, 9024, 9025, 9028, 9029, 9033, 9034, 9036, 9051, 9055, 9059, 9067, 9069, 9073, 9078, 9082, 9099, 9115, 9119, 9127, 9130, 9160, 9171, 9193, 9204, 9211, 9212, 9213, 9215, 9218, 9220, 9221, 9227, 9232, 9233, 9240, 9241, 9242, 9244, 9245, 9247, 9248, 9249, 9251, 9253, 9254, 9256, 9258, 9259, 9262, 9263, 9264, 9268, 9271, 9273, 9274, 9275, 9278, 9305, 9306, 9307, 9308, 9310, 9312, 9313, 9319, 9322, 9324, 9325, 9326, 9327, 9339, 9340, 9341, 9342, 9343, 9348, 9351, 9353, 9355, 9360, 9361, 9363, 9365, 9366, 9367, 9368, 9369, 9376, 9377, 9380, 9381, 9385, 9404, 9405, 9408, 9409, 9412, 9414, 9416, 9417, 9419, 9421, 9423, 9424, 9425, 9428, 9432, 9434, 9438, 9439, 9441, 9444, 9445, 9446, 9450, 9466, 9470, 9474, 9475, 9476, 9478, 9479, 9501, 9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509, 9511, 9514, 9517, 9519, 9522, 9535, 9536, 9543, 9551, 9554, 9557, 9560, 9561, 9562, 9563, 9564, 9600, 9610, 9613, 9619, 9622, 9625, 9629, 9633, 9640, 9644, 9651, 9656, 9675, 9685, 9686, 9692, 9696, 9698, 9702, 9704, 9709, 9713, 9716, 9717, 9723, 9726, 9729, 9742, 9743, 9753, 9760, 9761, 9765, 9767, 9768, 9776, 9782, 9783, 9788, 9791, 9795, 9799, 9812, 9816, 9818, 9827, 9831, 9832, 9835, 9837, 9842, 9845, 9846, 9850, 9853, 9854, 9856, 9857, 9872, 9876, 9878, 9880, 9882, 9885, 9888, 9890, 9895, 9896, 9900, 9903, 9904, 9906, 9908, 9913, 9914, 9919, 9927, 9928, 9929, 9930, 9941, 9946, 9959, 9969, 9972, 9973, 9976, 9978, 9979, 9980, 9982, 9990, 9991, 9993, 9995, 9996, 9997]
codes1 = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']
good_codes = [1430, 1431, 1434, 1436, 1438, 1451, 1491, 1739, 1780, 1789, 1802, 1803, 1808, 1879, 1905, 1914, 1921, 1934, 1942, 1960, 1965, 2001, 2002, 2114, 2136, 2148, 2150, 2164, 2179, 2180, 2185, 2186, 2193, 2195, 2215, 2266, 2303, 2317, 2329, 2330, 2332, 2335, 2349, 2353, 2359, 2372, 2376, 2411, 2425, 2436, 2437, 2438, 2445, 2449, 2453, 2459, 2471, 2480, 2481, 2483, 2488, 2491, 2497, 2652, 2666, 2668, 2683, 2694, 2734, 2749, 2754, 2792, 2795, 2820, 2884, 2903, 2917, 2922, 2924, 2926, 2930, 2936, 2970, 2975, 2978, 2999, 3003, 3023, 3064, 3065, 3121, 3143, 3157, 3181, 3192, 3195, 3204, 3236, 3238, 3241, 3245, 3252, 3271, 3276, 3284, 3293, 3294, 3316, 3317, 3350, 3352, 3355, 3359, 3361, 3371, 3375, 3388, 3392, 3405, 3409, 3435, 3441, 3449, 3452, 3457, 3464, 3475, 3482, 3486, 3489, 3495, 3512, 3513, 3537, 3538, 3553, 3558, 3566, 3580, 3622, 3623, 3640, 3661, 3672, 3676, 3677, 3679, 3681, 3690, 3723, 3744, 3747, 3762, 3766, 3784, 3802, 3804, 3816, 3834, 3836, 3841, 3842, 3844, 3845, 3848, 3851, 3858, 3864, 3878, 3896, 3900, 3902, 3903, 3916, 3917, 3920, 3927, 3929, 3933, 3939, 3963, 3964, 3969, 3974, 3978, 3979, 3981, 3983, 3988, 3992, 3997,4005, 4012, 4017, 4026, 4027, 4056, 4057, 4058, 4060, 4076, 4082, 4093, 4097, 4124, 4165, 4167, 4171, 4174, 4177, 4220, 4224, 4237, 4243, 4245, 4251, 4256, 4260, 4272, 4275, 4286, 4287, 4290, 4293, 4298, 4299, 4326, 4331, 4333, 4345, 4346, 4356, 4360, 4372, 4380, 4386, 4389, 4391, 4392, 4421, 4430, 4433, 4437, 4447, 4448, 4449, 4463, 4482, 4486, 4489, 4495, 4524, 4531, 4554, 4556, 4579, 4591, 4592, 4611, 4621, 4636, 4645, 4662, 4674, 4687, 4689, 4709, 4718, 4736, 4743, 4750, 4752, 4761, 4767, 4769, 4777, 4784, 4792, 4800, 4809, 4820, 4847, 4882, 4884, 4886, 4888, 4902, 4931, 4936, 4955, 4977, 4979, 4987, 4992, 5036, 5074, 5121, 5126, 5138, 5199, 5202, 5243, 5277, 5363, 5449, 5476, 5527, 5542, 5563, 5610, 5660, 5715, 5802, 5803, 5817, 5821, 5929, 5930, 5936, 5969, 5975, 5989, 5991, 5992, 5994, 6018, 6038, 6039, 6049, 6058, 6059, 6062, 6063, 6088, 6091, 6099, 6113, 6131, 6151, 6161, 6164, 6166, 6171, 6177, 6183, 6184, 6186, 6188, 6189, 6193, 6197, 6199, 6208, 6218, 6226, 6229, 6232, 6237, 6247, 6265, 6269, 6276, 6287, 6289, 6293, 6325, 6330, 6335, 6336, 6363, 6364, 6376, 6381, 6395, 6416, 6418, 6459, 6464, 6473, 6480, 6486, 6518, 6522, 6535, 6537, 6539, 6540, 6544, 6546, 6555, 6557, 6564, 6570, 6578, 6625, 6633, 6640, 6653, 6658, 6696, 6715, 6744, 6745, 6779, 6817, 6819, 6836, 6838, 6862, 6879, 6904, 6914, 6955, 7004, 7014, 7030, 7031, 7042, 7049, 7057, 7074, 7080, 7082, 7085, 7092, 7110, 7112, 7126, 7131, 7134, 7162, 7177, 7191, 7196, 7199, 7201, 7224, 7291, 7315, 7343, 7352, 7354, 7357, 7359, 7367, 7374, 7378, 7379, 7427, 7434, 7438, 7444, 7455, 7504, 7510, 7523, 7524, 7527, 7567, 7570, 7590, 7599, 7605, 7608, 7613, 7619, 7624, 7638, 7709, 7711, 7723, 7730, 7739, 7745, 7774, 7777, 7781, 7792, 7793, 7804, 7807, 7818, 7819, 7823, 7831, 7833, 7837, 7840, 7847, 7857, 7865, 7875, 7879, 7888, 7897, 7898, 7922, 7939, 7953, 7957, 7972, 7976, 7985, 7994, 8020, 8023, 8037, 8061, 8065, 8066, 8070, 8081, 8095, 8103, 8107, 8125, 8133, 8135, 8139, 8141, 8147, 8151, 8157, 8163, 8168, 8219, 8230, 8256, 8281, 8291, 8511, 8570, 8617, 8704, 8798, 8802, 8804, 8844, 8860, 8869, 8876, 8893, 8897, 8904, 8905, 8908, 8929, 8931, 8946, 8995, 9029, 9034, 9055, 9069, 9115, 9212, 9221, 9233, 9240, 9242, 9245, 9249, 9259, 9273, 9275, 9310, 9312, 9319, 9322, 9351, 9360, 9368, 9369, 9381, 9408, 9416, 9421, 9424, 9432, 9444, 9450, 9466, 9470, 9504, 9511, 9519, 9551, 9561, 9562, 9563, 9564, 9613, 9619, 9633, 9651, 9702, 9717, 9765, 9768, 9782, 9783, 9791, 9795, 9799, 9812, 9832, 9845, 9856, 9872, 9882, 9895, 9900, 9908, 9919, 9928, 9930, 9959, 9980, 9982]




symbol_all = []
time_all = []
win_all = []
win_all_price = []
lose_all = []
lose_all_price = []
if st.button('計算を行う'):
    for symbol in good_codes:
        # 過去の株価データの取得
        ticker = str(symbol) + '.T'
        tkr = yf.Ticker(ticker)
        hist = tkr.history(period='1700d')
        hist = hist.reset_index()
        hist = hist.set_index(['Date'])
        hist = hist.rename_axis('Date').reset_index()
        hist = hist.T
        a = hist.to_dict()
    
        for items in a.values():
                time = items['Date']
                items['Date'] = time.strftime("%Y/%m/%d")
    
        b = [x for x in a.values()]
    
        source = pd.DataFrame(b)
    
    
    
        # 条件1: 株価が20日移動平均線と50日移動平均線の下にあるか判断
        source['SMA_20'] = source['Close'].rolling(window=20).mean()
        source['SMA_50'] = source['Close'].rolling(window=50).mean()
        source['sma01'] = source['Close'].rolling(window=5).mean()
        source['sma02'] = source['Close'].rolling(window=20).mean()
        source['sma03'] = source['Close'].rolling(window=50).mean()
        #RSI
        # 前日との差分を計算
        df_diff = source["Close"].diff(1)
    
        # 計算用のDataFrameを定義
        df_up, df_down = df_diff.copy(), df_diff.copy()
    
        # df_upはマイナス値を0に変換
        # df_downはプラス値を0に変換して正負反転
        df_up[df_up < 0] = 0
        df_down[df_down > 0] = 0
        df_down = df_down * -1
    
    
        # 期間14でそれぞれの平均を算出
        df_up_sma14 = df_up.rolling(window=14, center=False).mean()
        df_down_sma14 = df_down.rolling(window=14, center=False).mean()
    
    
    
        # RSIを算出
        source["RSI"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))
    
        #DMIの計算
        high = source['High']
        low = source['Low']
        close = source['Close']
        pDM = (high - high.shift(1))
        mDM = (low.shift(1) - low)
        pDM.loc[pDM<0] = 0
        pDM.loc[pDM-mDM < 0] = 0
        mDM.loc[mDM<0] = 0
        mDM.loc[mDM-pDM < 0] = 0
        # trの計算
        a = (high - low).abs()
        b = (high - close.shift(1)).abs()
        c = (low - close.shift(1)).abs()
        tr = pd.concat([a, b, c], axis=1).max(axis=1)
        source['tr'] = tr
        source['ATR'] = tr.rolling(20).mean()
        source['pDI'] = pDM.rolling(14).sum()/tr.rolling(14).sum() * 100
        source['mDI'] = mDM.rolling(14).sum()/tr.rolling(14).sum() * 100
        # ADXの計算
        DX = (source['pDI']-source['mDI']).abs()/(source['pDI']+source['mDI']) * 100
        DX = DX.fillna(0)
        source['ADX'] = DX.rolling(14).mean()
        # 基準線
        high26 = source["High"].rolling(window=26).max()
        low26 = source["Low"].rolling(window=26).min()
        source["base_line"] = (high26 + low26) / 2
    
        # 転換線
        high9 = source["High"].rolling(window=9).max()
        low9 = source["Low"].rolling(window=9).min()
        source["conversion_line"] = (high9 + low9) / 2
    
        # 先行スパン1
        leading_span1 = (source["base_line"] + source["conversion_line"]) / 2
        source["leading_span1"] = leading_span1.shift(25)
    
        # 先行スパン2
        high52 = source["High"].rolling(window=52).max()
        low52 = source["Low"].rolling(window=52).min()
        leading_span2 = (high52 + low52) / 2
        source["leading_span2"] = leading_span2.shift(25)
      
        #大循環macd
        exp5 = source['Close'].ewm(span=5, adjust=False).mean()
        exp20 = source['Close'].ewm(span=20, adjust=False).mean()
        source['MACD1'] = exp5 - exp20


        exp40 = source['Close'].ewm(span=40, adjust=False).mean()
        source['MACD2'] = exp5 - exp40

        source['MACD3'] = exp20 - exp40

    
        # 遅行スパン
        source["lagging_span"] = source["Close"].shift(-25)

        KDAY = 26  # K算定用期間
        MDAY = 3  # D算定用期間

        # stochasticks K
        source["sct_k_price"] = (
            100*
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
        )

        # stochasticks D
        source["sct_d_price"] = (
            100*
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()
        )

        # slow stochasticks
        source["slow_sct_d_price"] = source["sct_d_price"].rolling(window=MDAY, min_periods=MDAY).mean()
        # 移動平均線
        source["SMA20"] = source["Close"].rolling(window=20,min_periods=20).mean()
        # 標準偏差
        source["std"] = source["Close"].rolling(window=20,min_periods=20).std()
        # ボリンジャーバンド
        source["2upper"] = source["SMA20"] + (2 * source["std"])
        source["2lower"] = source["SMA20"] - (2 * source["std"])
        source["3upper"] = source["SMA20"] + (3 * source["std"])
        source["3lower"] = source["SMA20"] - (3 * source["std"])
        source['bandwidth'] = (source['2upper'] - source['2lower']) / source['SMA20']
        source['percent_b'] = (source['Close'] - source['2lower']) / (source['2upper'] - source['2lower'])
        minimum20 = source["Low"].rolling(window=30).min()
        source["minimum"] = minimum20
        minimum_band = source["bandwidth"].rolling(window=120).min()
        source["minimum_band"] = minimum_band
        maximum30 = source["Close"].rolling(window=120).max()
        source["maximum"] = maximum30

              #GMMA
        exp3 = source['Close'].ewm(span=3, adjust=False).mean()
        exp8 = source['Close'].ewm(span=8, adjust=False).mean()
        exp10 = source['Close'].ewm(span=10, adjust=False).mean()
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp15 = source['Close'].ewm(span=15, adjust=False).mean()
        exp20 = source['Close'].ewm(span=20, adjust=False).mean()
        source['EMA3'] = exp3
        source['EMA5'] = exp5
        source['EMA8'] = exp8
        source['EMA10'] = exp10
        source['EMA12'] = exp12
        source['EMA15'] = exp15
        source['EMA20'] = exp20

        source["stage"] = 1
        stage6_list = []
        stage4_list = []
        stage5_list = []
        chance1 = []
        chance1_win_price = []
        chance1_lose_price = []
        if source.index[-1] == 1699:
          for i in range(326,1558):
              bandwidth = source['bandwidth'][i]
              bandwidth_yesterday = source['bandwidth'][i-1]
              percent_b = source['percent_b'][i]
              percent_b_yesterday = source['percent_b'][i-1]
              volume_difference = source['Volume'][i] - source['Volume'][i-1]*1.5
              midband = source['SMA20'][i]
              midband_yesterday = source['SMA20'][i-1]
              
              if percent_b>1 and percent_b_yesterday<1 and bandwidth_yesterday<bandwidth and midband>midband_yesterday:
                  for k in range(-5,0):
                      bandwidth = source['bandwidth'][i+k]
                      bandwidth_yesterday = source['bandwidth'][i-1+k]
                      minimum_bandwidth = source['minimum_band'][i+k]
                      minimum_bandwidth_yesterday = source['minimum_band'][i-1+k]
                      percent_b2 = source['percent_b'][i+k]
                      ema20 = source['EMA20'][i+k]
                      ema50 = source['EMA50'][i+k]
                      if bandwidth == minimum_bandwidth and 0.45<percent_b2<0.55:
    
    
                        # 条件3: 翌日または翌々日に、2のスラスト日の高値の価格で買う。2の日の安値より下がった場合は損切りする。
                        buy_price = source['Open'][i]
                        
      
                        if percent_b>percent_b_yesterday:
                            chance1.append(1)
      
      
      
                            # 条件4: トレーリングストップを使って利益を確定する
                            #trailing_stop = buy_price * 1.05  # 3%の利益確定を目指すと仮定
                            for a in range(11):
                                atr15 = source['ATR'][i+a-1] *0.8
                                stop_loss_price = source['Close'][i+a-1] - atr15
                                #20日経過した時
                                if source['Low'][i+a]>stop_loss_price:
                                    if a ==10 and source['Close'][i+a]>buy_price:
                                        price_win = source['Close'][i+a] - buy_price
                                        chance1_win_price.append(price_win)
                                        break
                                    if a ==10 and source['Close'][i+a]<buy_price:
                                        sonkiri = source['Close'][i+a] - buy_price
                                        chance1_lose_price.append(sonkiri)
                                    else:
                                        continue
                                #20日経過しなかった時
                                if source['Low'][i+a]<stop_loss_price:
                                    if stop_loss_price<buy_price:
                                        sonkiri = stop_loss_price - buy_price
                                        chance1_lose_price.append(sonkiri)
                                        break
                                    if stop_loss_price>buy_price:
                                        price_win =  stop_loss_price - buy_price
                                        chance1_win_price.append(price_win)
                                        break
      
    
          st.write(symbol)
          symbol_all.append(symbol)
          st.write('回数',len(chance1))
          time_all.append(len(chance1))
          st.write('勝ち', len(chance1_win_price), sum(chance1_win_price))
          win_all.append(len(chance1_win_price))
          win_all_price.append(sum(chance1_win_price))
          st.write('負け', len(chance1_lose_price), sum(chance1_lose_price))
          lose_all.append(len(chance1_lose_price))
          lose_all_price.append(sum(chance1_lose_price))
        else:
          continue
    
    st.write('回数', sum(time_all))
    st.write('勝率', sum(win_all)/sum(time_all))
    st.write('勝ち額', (sum(win_all_price) + sum(lose_all_price))*100)
    st.write('期待値', ((sum(win_all_price) + sum(lose_all_price))/ sum(time_all))*100)
