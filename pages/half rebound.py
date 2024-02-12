import pandas as pd
import yfinance as yf
import streamlit as st
# 仮のデータを作成
good_codes = [1430, 1431, 1434, 1436, 1438, 1451, 1491, 1739, 1780, 1789, 1802, 1803, 1808, 1879, 1905, 1914, 1921, 1934, 1942, 1960, 1965, 2001, 2002, 2114, 2136, 2148, 2150, 2164, 2179, 2180, 2193, 2195, 2215, 2266, 2303, 2317, 2329, 2330, 2332, 2335, 2349, 2353, 2359, 2372, 2376, 2411, 2425, 2436, 2437, 2438, 2445, 2449, 2453, 2459, 2471, 2480, 2481, 2483, 2488, 2491, 2497, 2652, 2666, 2668, 2683, 2694, 2734, 2749, 2754, 2792, 2795, 2820, 2884, 2903, 2917, 2924, 2926, 2930, 2936, 2970, 2975, 2978, 2999, 3003, 3023, 3064, 3065, 3121, 3143, 3157, 3181, 3192, 3195, 3204, 3236, 3238, 3241, 3245, 3252, 3271, 3276, 3284, 3293, 3294, 3317, 3350, 3352, 3355, 3359, 3361, 3371, 3375, 3388, 3392, 3405, 3409, 3435, 3441, 3452, 3457, 3475, 3482, 3486, 3489, 3495, 3512, 3513, 3537, 3538, 3553, 3558, 3566, 3580, 3622, 3623, 3640, 3661, 3672, 3676, 3679, 3681, 3690, 3723, 3744, 3747, 3762, 3766, 3784, 3802, 3804, 3816, 3834, 3836, 3841, 3842, 3844, 3845, 3848, 3851, 3858, 3864, 3878, 3896, 3902, 3903, 3916, 3917, 3920, 3927, 3929, 3933, 3939, 3963, 3964, 3969, 3974, 3978, 3979, 3981, 3983, 3988, 3992, 3997,4005, 4012, 4017, 4026, 4027, 4056, 4057, 4058, 4060, 4076, 4082, 4093, 4097, 4124, 4165, 4167, 4171, 4174, 4177, 4220, 4224, 4237, 4243, 4245, 4251, 4256, 4260, 4272, 4275, 4286, 4287, 4290, 4293, 4298, 4299, 4326, 4331, 4333, 4345, 4346, 4356, 4360, 4372, 4389, 4391, 4392, 4421, 4430, 4433, 4437, 4447, 4448, 4449, 4463, 4482, 4486, 4489, 4495, 4524, 4531, 4554, 4556, 4579, 4591, 4592, 4611, 4636, 4645, 4662, 4674, 4687, 4689, 4709, 4718, 4736, 4743, 4750, 4752, 4761, 4767, 4769, 4777, 4784, 4792, 4800, 4809, 4820, 4847, 4882, 4884, 4886, 4902, 4931, 4936, 4955, 4977, 4979, 4987, 4992, 5036, 5074, 5121, 5126, 5138, 5199, 5202, 5243, 5277, 5363, 5449, 5476, 5527, 5542, 5563, 5610, 5660, 5715, 5802, 5803, 5817, 5821, 5929, 5930, 5936, 5969, 5975, 5989, 5991, 5992, 5994, 6018, 6038, 6039, 6049, 6058, 6059, 6062, 6063, 6088, 6091, 6099, 6113, 6131, 6151, 6161, 6164, 6166, 6171, 6177, 6183, 6184, 6186, 6188, 6189, 6197, 6199, 6208, 6218, 6226, 6229, 6232, 6237, 6247, 6265, 6269, 6276, 6287, 6289, 6293, 6325, 6330, 6335, 6336, 6363, 6364, 6376, 6381, 6395, 6416, 6418, 6459, 6464, 6473, 6480, 6486, 6518, 6522, 6535, 6537, 6539, 6540, 6544, 6546, 6555, 6557, 6564, 6570, 6578, 6625, 6633, 6640, 6653, 6658, 6696, 6715, 6744, 6745, 6779, 6817, 6819, 6836, 6838, 6862, 6879, 6904, 6914, 6955, 7004, 7014, 7030, 7031, 7042, 7049, 7057, 7074, 7080, 7082, 7085, 7092, 7110, 7112, 7126, 7131, 7134, 7162, 7177, 7191, 7196, 7199, 7201, 7224, 7291, 7315, 7343, 7352, 7354, 7357, 7359, 7367, 7374, 7378, 7379, 7427, 7434, 7438, 7444, 7455, 7504, 7510, 7523, 7524, 7527, 7567, 7570, 7590, 7605, 7608, 7613, 7619, 7624, 7638, 7709, 7711, 7723, 7730, 7739, 7745, 7774, 7777, 7781, 7792, 7793, 7804, 7807, 7818, 7819, 7823, 7831, 7833, 7837, 7840, 7847, 7857, 7865, 7875, 7879, 7888, 7897, 7898, 7922, 7939, 7953, 7957, 7972, 7976, 7985, 7994, 8020, 8023, 8037, 8061, 8065, 8066, 8070, 8081, 8095, 8103, 8107, 8125, 8133, 8135, 8139, 8141, 8147, 8151, 8157, 8163, 8219, 8230, 8281, 8291, 8511, 8570, 8617, 8704, 8798, 8802, 8804, 8844, 8860, 8869, 8876, 8893, 8897, 8904, 8905, 8908, 8929, 8931, 8946, 8995, 9029, 9034, 9055, 9069, 9115, 9212, 9221, 9233, 9242, 9245, 9249, 9259, 9273, 9275, 9310, 9312, 9319, 9322, 9351, 9360, 9368, 9369, 9381, 9408, 9416, 9421, 9424, 9432, 9444, 9450, 9466, 9470, 9504, 9511, 9551, 9562, 9563, 9564, 9613, 9619, 9633, 9651, 9702, 9717, 9765, 9768, 9782, 9783, 9791, 9795, 9799, 9812, 9832, 9845, 9856, 9872, 9882, 9895, 9900, 9908, 9919, 9928, 9930, 9959, 9980, 9982]


last = 99
matching_stocks = []
if st.button('計算を行う'):
    for code in good_codes:
        st.write(code)
        option = code
        ticker = str(option) + '.T'
        tkr = yf.Ticker(ticker)
        hist = tkr.history(period='100d')
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
        
        price = source['Close']
        
        


        # 最近の高値を見つける
        recent_high = max(price[-20:])  # 最近20日間の最大値を取得

        # その前の安値を見つける
        previous_low = min(price[-30:])  # 最後の20日を除外したデータでの最小値を取得

        # 半分の価格を計算
        half_price = (recent_high + previous_low) / 2

        # 現在の価格が半分の価格に近いか確認
        if abs(source['Close'][last] - half_price) <= source['Close'][last]*0.1:  # 価格が±1の範囲内であるか確認
            matching_stocks.append(code)
            
            
    st.write('該当する銘柄', code)
