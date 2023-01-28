advice_list=calc_shanten_14(txt)
        for idx,x in enumerate(advice_list):
            advice="打"+str(convert_num_to_card(x[0]))+str(x[2])+"枚\n"+" 摸"+str([convert_num_to_card(x) for x in x[1]])