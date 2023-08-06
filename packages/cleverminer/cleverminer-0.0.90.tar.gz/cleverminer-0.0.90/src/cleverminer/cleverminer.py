import time #line:1
from time import strftime #line:3
from time import gmtime #line:4
import pandas as pd #line:6
class cleverminer :#line:8
    version_string ="0.0.90"#line:10
    def __init__ (OO00000000000O000 ,**OO00OOOOO00O00O00 ):#line:12
        OO00000000000O000 ._print_disclaimer ()#line:13
        OO00000000000O000 .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:21
        OO00000000000O000 ._init_data ()#line:22
        OO00000000000O000 ._init_task ()#line:23
        if len (OO00OOOOO00O00O00 )>0 :#line:24
            OO00000000000O000 .kwargs =OO00OOOOO00O00O00 #line:25
            OO00000000000O000 ._calc_all (**OO00OOOOO00O00O00 )#line:26
    def _init_data (O0O0O00OO00OOO0OO ):#line:28
        O0O0O00OO00OOO0OO .data ={}#line:30
        O0O0O00OO00OOO0OO .data ["varname"]=[]#line:31
        O0O0O00OO00OOO0OO .data ["catnames"]=[]#line:32
        O0O0O00OO00OOO0OO .data ["vtypes"]=[]#line:33
        O0O0O00OO00OOO0OO .data ["dm"]=[]#line:34
        O0O0O00OO00OOO0OO .data ["rows_count"]=int (0 )#line:35
        O0O0O00OO00OOO0OO .data ["data_prepared"]=0 #line:36
    def _init_task (OOO00O0OO0O0OO0O0 ):#line:38
        OOO00O0OO0O0OO0O0 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:47
        OOO00O0OO0O0OO0O0 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:51
        OOO00O0OO0O0OO0O0 .rulelist =[]#line:52
        OOO00O0OO0O0OO0O0 .stats ['total_cnt']=0 #line:54
        OOO00O0OO0O0OO0O0 .stats ['total_valid']=0 #line:55
        OOO00O0OO0O0OO0O0 .stats ['control_number']=0 #line:56
        OOO00O0OO0O0OO0O0 .result ={}#line:57
    def _get_ver (OOOOOOO00000OO00O ):#line:59
        return OOOOOOO00000OO00O .version_string #line:60
    def _print_disclaimer (OO000O0O00O0OOOOO ):#line:62
        print ("***********************************************************************************************************************************************************************")#line:63
        print ("Cleverminer version ",OO000O0O00O0OOOOO ._get_ver ())#line:64
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:65
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:66
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:67
        print ("This version is for personal and educational use only.")#line:68
        print ("***********************************************************************************************************************************************************************")#line:69
    def _prep_data (OO0OOOOO0000OO0OO ,OO0OO0O000O00OOO0 ):#line:71
        print ("Starting data preparation ...")#line:72
        OO0OOOOO0000OO0OO ._init_data ()#line:73
        OO0OOOOO0000OO0OO .stats ['start_prep_time']=time .time ()#line:74
        OO0OOOOO0000OO0OO .data ["rows_count"]=OO0OO0O000O00OOO0 .shape [0 ]#line:75
        for OOO0OOOO0OO0OO0OO in OO0OO0O000O00OOO0 .select_dtypes (exclude =['category']).columns :#line:76
            OO0OO0O000O00OOO0 [OOO0OOOO0OO0OO0OO ]=OO0OO0O000O00OOO0 [OOO0OOOO0OO0OO0OO ].apply (str )#line:77
        OO0O0OO0OO00OOO00 =pd .DataFrame .from_records ([(OO0000OO0000O0OOO ,OO0OO0O000O00OOO0 [OO0000OO0000O0OOO ].nunique ())for OO0000OO0000O0OOO in OO0OO0O000O00OOO0 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:79
        print ("Unique value counts are:")#line:80
        print (OO0O0OO0OO00OOO00 )#line:81
        for OOO0OOOO0OO0OO0OO in OO0OO0O000O00OOO0 .columns :#line:82
            if OO0OO0O000O00OOO0 [OOO0OOOO0OO0OO0OO ].nunique ()<100 :#line:83
                OO0OO0O000O00OOO0 [OOO0OOOO0OO0OO0OO ]=OO0OO0O000O00OOO0 [OOO0OOOO0OO0OO0OO ].astype ('category')#line:84
            else :#line:85
                print (f"WARNING: attribute {OOO0OOOO0OO0OO0OO} has more than 100 values, will be ignored.")#line:86
                del OO0OO0O000O00OOO0 [OOO0OOOO0OO0OO0OO ]#line:87
        print ("Encoding columns into bit-form...")#line:88
        OO0O0OO0000OOO000 =0 #line:89
        OOOOO00OO0OO0O000 =0 #line:90
        for O0OO0O0000000OO0O in OO0OO0O000O00OOO0 :#line:91
            print ('Column: '+O0OO0O0000000OO0O )#line:93
            OO0OOOOO0000OO0OO .data ["varname"].append (O0OO0O0000000OO0O )#line:94
            OO0OOO0O00O0O0OO0 =pd .get_dummies (OO0OO0O000O00OOO0 [O0OO0O0000000OO0O ])#line:95
            OOOO0O000OOOOO0OO =0 #line:96
            if (OO0OO0O000O00OOO0 .dtypes [O0OO0O0000000OO0O ].name =='category'):#line:97
                OOOO0O000OOOOO0OO =1 #line:98
            OO0OOOOO0000OO0OO .data ["vtypes"].append (OOOO0O000OOOOO0OO )#line:99
            OOO0000O00O00000O =0 #line:102
            OO0O000O0OOOOOO00 =[]#line:103
            OOO0OO0OOO0O00000 =[]#line:104
            for OOO0OOOOOOOO0O0O0 in OO0OOO0O00O0O0OO0 :#line:106
                print ('....category : '+str (OOO0OOOOOOOO0O0O0 )+" @ "+str (time .time ()))#line:108
                OO0O000O0OOOOOO00 .append (OOO0OOOOOOOO0O0O0 )#line:109
                OOOO0O0O0O0O000OO =int (0 )#line:110
                O0OOO000OO0OOO000 =OO0OOO0O00O0O0OO0 [OOO0OOOOOOOO0O0O0 ].values #line:111
                for O0O0OO00OOO0000OO in range (OO0OOOOO0000OO0OO .data ["rows_count"]):#line:113
                    if O0OOO000OO0OOO000 [O0O0OO00OOO0000OO ]>0 :#line:114
                        OOOO0O0O0O0O000OO +=1 <<O0O0OO00OOO0000OO #line:115
                OOO0OO0OOO0O00000 .append (OOOO0O0O0O0O000OO )#line:116
                OOO0000O00O00000O +=1 #line:126
                OOOOO00OO0OO0O000 +=1 #line:127
            OO0OOOOO0000OO0OO .data ["catnames"].append (OO0O000O0OOOOOO00 )#line:129
            OO0OOOOO0000OO0OO .data ["dm"].append (OOO0OO0OOO0O00000 )#line:130
        print ("Encoding columns into bit-form...done")#line:132
        print ("Encoding columns into bit-form...done")#line:133
        print (f"List of attributes for analysis is: {OO0OOOOO0000OO0OO.data['varname']}")#line:134
        print (f"List of category names for individual attributes is : {OO0OOOOO0000OO0OO.data['catnames']}")#line:135
        print (f"List of vtypes is (all should be 1) : {OO0OOOOO0000OO0OO.data['vtypes']}")#line:136
        OO0OOOOO0000OO0OO .data ["data_prepared"]=1 #line:138
        print ("Data preparation finished ...")#line:139
        print ('Number of variables : '+str (len (OO0OOOOO0000OO0OO .data ["dm"])))#line:140
        print ('Total number of categories in all variables : '+str (OOOOO00OO0OO0O000 ))#line:141
        OO0OOOOO0000OO0OO .stats ['end_prep_time']=time .time ()#line:142
        print ('Time needed for data preparation : ',str (OO0OOOOO0000OO0OO .stats ['end_prep_time']-OO0OOOOO0000OO0OO .stats ['start_prep_time']))#line:143
    def bitcount (O0000O0OOO00OOO0O ,OOOOOO0OOOOO0OO0O ):#line:146
        OO00O000OO00OO000 =0 #line:147
        while OOOOOO0OOOOO0OO0O >0 :#line:148
            if (OOOOOO0OOOOO0OO0O &1 ==1 ):OO00O000OO00OO000 +=1 #line:149
            OOOOOO0OOOOO0OO0O >>=1 #line:150
        return OO00O000OO00OO000 #line:151
    def _verifyCF (OO0000O0O00OO00O0 ,_OO0O0O00OO0O0O0O0 ):#line:154
        O0OOO0OOO0OOOO0OO =bin (_OO0O0O00OO0O0O0O0 ).count ("1")#line:155
        OO000OOO000000OOO =[]#line:156
        O00OOOO0OOO0000O0 =[]#line:157
        OOOO000O000O0OOO0 =0 #line:158
        O0000OO0OO00O0000 =0 #line:159
        O00OO0OO0OOO0OO0O =0 #line:160
        O00OO0OOOOOOOOOOO =0 #line:161
        OO0OOO000OOOO000O =0 #line:162
        O000OOO0000O000OO =0 #line:163
        O0O00OO0O0000O00O =0 #line:164
        O0O0O0000OOO00OO0 =0 #line:165
        OO000000OO000O0O0 =0 #line:166
        OOOO00000O000O0OO =OO0000O0O00OO00O0 .data ["dm"][OO0000O0O00OO00O0 .data ["varname"].index (OO0000O0O00OO00O0 .kwargs .get ('target'))]#line:167
        for OO00OO0000OO0O0OO in range (len (OOOO00000O000O0OO )):#line:168
            O0000OO0OO00O0000 =OOOO000O000O0OOO0 #line:169
            OOOO000O000O0OOO0 =bin (_OO0O0O00OO0O0O0O0 &OOOO00000O000O0OO [OO00OO0000OO0O0OO ]).count ("1")#line:170
            OO000OOO000000OOO .append (OOOO000O000O0OOO0 )#line:171
            if OO00OO0000OO0O0OO >0 :#line:172
                if (OOOO000O000O0OOO0 >O0000OO0OO00O0000 ):#line:173
                    if (O00OO0OO0OOO0OO0O ==1 ):#line:174
                        O0O0O0000OOO00OO0 +=1 #line:175
                    else :#line:176
                        O0O0O0000OOO00OO0 =1 #line:177
                    if O0O0O0000OOO00OO0 >O00OO0OOOOOOOOOOO :#line:178
                        O00OO0OOOOOOOOOOO =O0O0O0000OOO00OO0 #line:179
                    O00OO0OO0OOO0OO0O =1 #line:180
                    O000OOO0000O000OO +=1 #line:181
                if (OOOO000O000O0OOO0 <O0000OO0OO00O0000 ):#line:182
                    if (O00OO0OO0OOO0OO0O ==-1 ):#line:183
                        OO000000OO000O0O0 +=1 #line:184
                    else :#line:185
                        OO000000OO000O0O0 =1 #line:186
                    if OO000000OO000O0O0 >OO0OOO000OOOO000O :#line:187
                        OO0OOO000OOOO000O =OO000000OO000O0O0 #line:188
                    O00OO0OO0OOO0OO0O =-1 #line:189
                    O0O00OO0O0000O00O +=1 #line:190
                if (OOOO000O000O0OOO0 ==O0000OO0OO00O0000 ):#line:191
                    O00OO0OO0OOO0OO0O =0 #line:192
                    OO000000OO000O0O0 =0 #line:193
                    O0O0O0000OOO00OO0 =0 #line:194
        OO0000O00O000000O =True #line:197
        for O0OOOOO0O00OO0O00 in OO0000O0O00OO00O0 .quantifiers .keys ():#line:198
            if O0OOOOO0O00OO0O00 .upper ()=='BASE':#line:199
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=O0OOO0OOO0OOOO0OO )#line:200
            if O0OOOOO0O00OO0O00 .upper ()=='RELBASE':#line:201
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=O0OOO0OOO0OOOO0OO *1.0 /OO0000O0O00OO00O0 .data ["rows_count"])#line:202
            if O0OOOOO0O00OO0O00 .upper ()=='S_UP':#line:203
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=O00OO0OOOOOOOOOOO )#line:204
            if O0OOOOO0O00OO0O00 .upper ()=='S_DOWN':#line:205
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=OO0OOO000OOOO000O )#line:206
            if O0OOOOO0O00OO0O00 .upper ()=='S_ANY_UP':#line:207
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=O00OO0OOOOOOOOOOO )#line:208
            if O0OOOOO0O00OO0O00 .upper ()=='S_ANY_DOWN':#line:209
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=OO0OOO000OOOO000O )#line:210
            if O0OOOOO0O00OO0O00 .upper ()=='MAX':#line:211
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=max (OO000OOO000000OOO ))#line:212
            if O0OOOOO0O00OO0O00 .upper ()=='MIN':#line:213
                OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=min (OO000OOO000000OOO ))#line:214
            if O0OOOOO0O00OO0O00 .upper ()=='RELMAX':#line:215
                if sum (OO000OOO000000OOO )>0 :#line:216
                    OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=max (OO000OOO000000OOO )*1.0 /sum (OO000OOO000000OOO ))#line:217
                else :#line:218
                    OO0000O00O000000O =False #line:219
            if O0OOOOO0O00OO0O00 .upper ()=='RELMAX_LEQ':#line:220
                if sum (OO000OOO000000OOO )>0 :#line:221
                    OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )>=max (OO000OOO000000OOO )*1.0 /sum (OO000OOO000000OOO ))#line:222
                else :#line:223
                    OO0000O00O000000O =False #line:224
            if O0OOOOO0O00OO0O00 .upper ()=='RELMIN':#line:225
                if sum (OO000OOO000000OOO )>0 :#line:226
                    OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )<=min (OO000OOO000000OOO )*1.0 /sum (OO000OOO000000OOO ))#line:227
                else :#line:228
                    OO0000O00O000000O =False #line:229
            if O0OOOOO0O00OO0O00 .upper ()=='RELMIN_LEQ':#line:230
                if sum (OO000OOO000000OOO )>0 :#line:231
                    OO0000O00O000000O =OO0000O00O000000O and (OO0000O0O00OO00O0 .quantifiers .get (O0OOOOO0O00OO0O00 )>=min (OO000OOO000000OOO )*1.0 /sum (OO000OOO000000OOO ))#line:232
                else :#line:233
                    OO0000O00O000000O =False #line:234
        OOOOO0O0O000OOO00 ={}#line:235
        if OO0000O00O000000O ==True :#line:236
            OO0000O0O00OO00O0 .stats ['total_valid']+=1 #line:238
            OOOOO0O0O000OOO00 ["base"]=O0OOO0OOO0OOOO0OO #line:239
            OOOOO0O0O000OOO00 ["rel_base"]=O0OOO0OOO0OOOO0OO *1.0 /OO0000O0O00OO00O0 .data ["rows_count"]#line:240
            OOOOO0O0O000OOO00 ["s_up"]=O00OO0OOOOOOOOOOO #line:241
            OOOOO0O0O000OOO00 ["s_down"]=OO0OOO000OOOO000O #line:242
            OOOOO0O0O000OOO00 ["s_any_up"]=O000OOO0000O000OO #line:243
            OOOOO0O0O000OOO00 ["s_any_down"]=O0O00OO0O0000O00O #line:244
            OOOOO0O0O000OOO00 ["max"]=max (OO000OOO000000OOO )#line:245
            OOOOO0O0O000OOO00 ["min"]=min (OO000OOO000000OOO )#line:246
            if sum (OO000OOO000000OOO )>0 :#line:249
                OOOOO0O0O000OOO00 ["rel_max"]=max (OO000OOO000000OOO )*1.0 /sum (OO000OOO000000OOO )#line:250
                OOOOO0O0O000OOO00 ["rel_min"]=min (OO000OOO000000OOO )*1.0 /sum (OO000OOO000000OOO )#line:251
            else :#line:252
                OOOOO0O0O000OOO00 ["rel_max"]=0 #line:253
                OOOOO0O0O000OOO00 ["rel_min"]=0 #line:254
            OOOOO0O0O000OOO00 ["hist"]=OO000OOO000000OOO #line:255
        return OO0000O00O000000O ,OOOOO0O0O000OOO00 #line:257
    def _verify4ft (O0OO00O00O0O00OOO ,_OOOOO00OOO0OO0OOO ):#line:259
        OO00OO0O00OO00O00 ={}#line:260
        O00OO00O000O000O0 =0 #line:261
        for OOOO0O00O00OO0000 in O0OO00O00O0O00OOO .task_actinfo ['cedents']:#line:262
            OO00OO0O00OO00O00 [OOOO0O00O00OO0000 ['cedent_type']]=OOOO0O00O00OO0000 ['filter_value']#line:264
            O00OO00O000O000O0 =O00OO00O000O000O0 +1 #line:265
        OO00O00000000OOO0 =bin (OO00OO0O00OO00O00 ['ante']&OO00OO0O00OO00O00 ['succ']&OO00OO0O00OO00O00 ['cond']).count ("1")#line:267
        O000O00O00OO00OO0 =None #line:268
        O000O00O00OO00OO0 =0 #line:269
        if OO00O00000000OOO0 >0 :#line:278
            O000O00O00OO00OO0 =bin (OO00OO0O00OO00O00 ['ante']&OO00OO0O00OO00O00 ['succ']&OO00OO0O00OO00O00 ['cond']).count ("1")*1.0 /bin (OO00OO0O00OO00O00 ['ante']&OO00OO0O00OO00O00 ['cond']).count ("1")#line:279
        OO000O0000O000OOO =1 <<O0OO00O00O0O00OOO .data ["rows_count"]#line:281
        OO0O0000O00OOO00O =bin (OO00OO0O00OO00O00 ['ante']&OO00OO0O00OO00O00 ['succ']&OO00OO0O00OO00O00 ['cond']).count ("1")#line:282
        OO0OOOOO00O0OOOO0 =bin (OO00OO0O00OO00O00 ['ante']&~(OO000O0000O000OOO |OO00OO0O00OO00O00 ['succ'])&OO00OO0O00OO00O00 ['cond']).count ("1")#line:283
        OOOO0O00O00OO0000 =bin (~(OO000O0000O000OOO |OO00OO0O00OO00O00 ['ante'])&OO00OO0O00OO00O00 ['succ']&OO00OO0O00OO00O00 ['cond']).count ("1")#line:284
        O0OO0O0OO0O0OO00O =bin (~(OO000O0000O000OOO |OO00OO0O00OO00O00 ['ante'])&~(OO000O0000O000OOO |OO00OO0O00OO00O00 ['succ'])&OO00OO0O00OO00O00 ['cond']).count ("1")#line:285
        O0OO00O0O0OO000OO =0 #line:286
        if (OO0O0000O00OOO00O +OO0OOOOO00O0OOOO0 )*(OO0O0000O00OOO00O +OOOO0O00O00OO0000 )>0 :#line:287
            O0OO00O0O0OO000OO =OO0O0000O00OOO00O *(OO0O0000O00OOO00O +OO0OOOOO00O0OOOO0 +OOOO0O00O00OO0000 +O0OO0O0OO0O0OO00O )/(OO0O0000O00OOO00O +OO0OOOOO00O0OOOO0 )/(OO0O0000O00OOO00O +OOOO0O00O00OO0000 )-1 #line:288
        else :#line:289
            O0OO00O0O0OO000OO =None #line:290
        O0O00O0OO0OOOO00O =0 #line:291
        if (OO0O0000O00OOO00O +OO0OOOOO00O0OOOO0 )*(OO0O0000O00OOO00O +OOOO0O00O00OO0000 )>0 :#line:292
            O0O00O0OO0OOOO00O =1 -OO0O0000O00OOO00O *(OO0O0000O00OOO00O +OO0OOOOO00O0OOOO0 +OOOO0O00O00OO0000 +O0OO0O0OO0O0OO00O )/(OO0O0000O00OOO00O +OO0OOOOO00O0OOOO0 )/(OO0O0000O00OOO00O +OOOO0O00O00OO0000 )#line:293
        else :#line:294
            O0O00O0OO0OOOO00O =None #line:295
        OO0000OO00O000O0O =True #line:296
        for OOOOO00OOO0OO0OO0 in O0OO00O00O0O00OOO .quantifiers .keys ():#line:297
            if OOOOO00OOO0OO0OO0 .upper ()=='BASE':#line:298
                OO0000OO00O000O0O =OO0000OO00O000O0O and (O0OO00O00O0O00OOO .quantifiers .get (OOOOO00OOO0OO0OO0 )<=OO00O00000000OOO0 )#line:299
            if OOOOO00OOO0OO0OO0 .upper ()=='RELBASE':#line:300
                OO0000OO00O000O0O =OO0000OO00O000O0O and (O0OO00O00O0O00OOO .quantifiers .get (OOOOO00OOO0OO0OO0 )<=OO00O00000000OOO0 *1.0 /O0OO00O00O0O00OOO .data ["rows_count"])#line:301
            if (OOOOO00OOO0OO0OO0 .upper ()=='PIM')or (OOOOO00OOO0OO0OO0 .upper ()=='CONF'):#line:302
                OO0000OO00O000O0O =OO0000OO00O000O0O and (O0OO00O00O0O00OOO .quantifiers .get (OOOOO00OOO0OO0OO0 )<=O000O00O00OO00OO0 )#line:303
            if OOOOO00OOO0OO0OO0 .upper ()=='AAD':#line:304
                if O0OO00O0O0OO000OO !=None :#line:305
                    OO0000OO00O000O0O =OO0000OO00O000O0O and (O0OO00O00O0O00OOO .quantifiers .get (OOOOO00OOO0OO0OO0 )<=O0OO00O0O0OO000OO )#line:306
                else :#line:307
                    OO0000OO00O000O0O =False #line:308
            if OOOOO00OOO0OO0OO0 .upper ()=='BAD':#line:309
                if O0O00O0OO0OOOO00O !=None :#line:310
                    OO0000OO00O000O0O =OO0000OO00O000O0O and (O0OO00O00O0O00OOO .quantifiers .get (OOOOO00OOO0OO0OO0 )<=O0O00O0OO0OOOO00O )#line:311
                else :#line:312
                    OO0000OO00O000O0O =False #line:313
            OOOO00000OOO0O000 ={}#line:314
        if OO0000OO00O000O0O ==True :#line:315
            O0OO00O00O0O00OOO .stats ['total_valid']+=1 #line:317
            OOOO00000OOO0O000 ["base"]=OO00O00000000OOO0 #line:318
            OOOO00000OOO0O000 ["rel_base"]=OO00O00000000OOO0 *1.0 /O0OO00O00O0O00OOO .data ["rows_count"]#line:319
            OOOO00000OOO0O000 ["conf"]=O000O00O00OO00OO0 #line:320
            OOOO00000OOO0O000 ["aad"]=O0OO00O0O0OO000OO #line:321
            OOOO00000OOO0O000 ["bad"]=O0O00O0OO0OOOO00O #line:322
            OOOO00000OOO0O000 ["fourfold"]=[OO0O0000O00OOO00O ,OO0OOOOO00O0OOOO0 ,OOOO0O00O00OO0000 ,O0OO0O0OO0O0OO00O ]#line:323
        return OO0000OO00O000O0O ,OOOO00000OOO0O000 #line:327
    def _verifysd4ft (O0O0O0OO0O000OOO0 ,_OO00000OO0O0OO00O ):#line:329
        OOO0O00000O0OO0OO ={}#line:330
        O0O0OOO000OO0OO0O =0 #line:331
        for O000000OO00O00OOO in O0O0O0OO0O000OOO0 .task_actinfo ['cedents']:#line:332
            OOO0O00000O0OO0OO [O000000OO00O00OOO ['cedent_type']]=O000000OO00O00OOO ['filter_value']#line:334
            O0O0OOO000OO0OO0O =O0O0OOO000OO0OO0O +1 #line:335
        O0OOO0O00OOO00O0O =bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")#line:337
        OOO000O000OO000OO =bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")#line:338
        O0O00O00OO00O0OOO =None #line:339
        OO00000O0000000OO =0 #line:340
        O000OO0OO0OOO0OOO =0 #line:341
        if O0OOO0O00OOO00O0O >0 :#line:350
            OO00000O0000000OO =bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")*1.0 /bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")#line:351
        if OOO000O000OO000OO >0 :#line:352
            O000OO0OO0OOO0OOO =bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")*1.0 /bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")#line:353
        OO0O00O0000O0OOO0 =1 <<O0O0O0OO0O000OOO0 .data ["rows_count"]#line:355
        O00000O0OO0O0O000 =bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")#line:356
        OOOO0O000OO000O00 =bin (OOO0O00000O0OO0OO ['ante']&~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['succ'])&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")#line:357
        O0OOO00000OO0O00O =bin (~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['ante'])&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")#line:358
        O00O0O00O0OOOOOOO =bin (~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['ante'])&~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['succ'])&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['frst']).count ("1")#line:359
        O0OOOOOO000000OOO =bin (OOO0O00000O0OO0OO ['ante']&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")#line:360
        OOO0O0OOOOOO0OO0O =bin (OOO0O00000O0OO0OO ['ante']&~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['succ'])&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")#line:361
        OOO0O000O00O00OO0 =bin (~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['ante'])&OOO0O00000O0OO0OO ['succ']&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")#line:362
        O00O000O000OO00OO =bin (~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['ante'])&~(OO0O00O0000O0OOO0 |OOO0O00000O0OO0OO ['succ'])&OOO0O00000O0OO0OO ['cond']&OOO0O00000O0OO0OO ['scnd']).count ("1")#line:363
        O0O000000000OO00O =True #line:364
        for O000O000O0O0O000O in O0O0O0OO0O000OOO0 .quantifiers .keys ():#line:365
            if (O000O000O0O0O000O .upper ()=='FRSTBASE')|(O000O000O0O0O000O .upper ()=='BASE1'):#line:366
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=O0OOO0O00OOO00O0O )#line:367
            if (O000O000O0O0O000O .upper ()=='SCNDBASE')|(O000O000O0O0O000O .upper ()=='BASE2'):#line:368
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=OOO000O000OO000OO )#line:369
            if (O000O000O0O0O000O .upper ()=='FRSTRELBASE')|(O000O000O0O0O000O .upper ()=='RELBASE1'):#line:370
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=O0OOO0O00OOO00O0O *1.0 /O0O0O0OO0O000OOO0 .data ["rows_count"])#line:371
            if (O000O000O0O0O000O .upper ()=='SCNDRELBASE')|(O000O000O0O0O000O .upper ()=='RELBASE2'):#line:372
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=OOO000O000OO000OO *1.0 /O0O0O0OO0O000OOO0 .data ["rows_count"])#line:373
            if (O000O000O0O0O000O .upper ()=='FRSTPIM')|(O000O000O0O0O000O .upper ()=='PIM1')|(O000O000O0O0O000O .upper ()=='FRSTCONF')|(O000O000O0O0O000O .upper ()=='CONF1'):#line:374
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=OO00000O0000000OO )#line:375
            if (O000O000O0O0O000O .upper ()=='SCNDPIM')|(O000O000O0O0O000O .upper ()=='PIM2')|(O000O000O0O0O000O .upper ()=='SCNDCONF')|(O000O000O0O0O000O .upper ()=='CONF2'):#line:376
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=O000OO0OO0OOO0OOO )#line:377
            if (O000O000O0O0O000O .upper ()=='DELTAPIM')|(O000O000O0O0O000O .upper ()=='DELTACONF'):#line:378
                O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=OO00000O0000000OO -O000OO0OO0OOO0OOO )#line:379
            if (O000O000O0O0O000O .upper ()=='RATIOPIM')|(O000O000O0O0O000O .upper ()=='RATIOCONF'):#line:382
                if (O000OO0OO0OOO0OOO >0 ):#line:383
                    O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )<=OO00000O0000000OO *1.0 /O000OO0OO0OOO0OOO )#line:384
                else :#line:385
                    O0O000000000OO00O =False #line:386
            if (O000O000O0O0O000O .upper ()=='RATIOPIM_LEQ')|(O000O000O0O0O000O .upper ()=='RATIOCONF_LEQ'):#line:387
                if (O000OO0OO0OOO0OOO >0 ):#line:388
                    O0O000000000OO00O =O0O000000000OO00O and (O0O0O0OO0O000OOO0 .quantifiers .get (O000O000O0O0O000O )>=OO00000O0000000OO *1.0 /O000OO0OO0OOO0OOO )#line:389
                else :#line:390
                    O0O000000000OO00O =False #line:391
        OO0O00OO000O0OO0O ={}#line:392
        if O0O000000000OO00O ==True :#line:393
            O0O0O0OO0O000OOO0 .stats ['total_valid']+=1 #line:395
            OO0O00OO000O0OO0O ["base1"]=O0OOO0O00OOO00O0O #line:396
            OO0O00OO000O0OO0O ["base2"]=OOO000O000OO000OO #line:397
            OO0O00OO000O0OO0O ["rel_base1"]=O0OOO0O00OOO00O0O *1.0 /O0O0O0OO0O000OOO0 .data ["rows_count"]#line:398
            OO0O00OO000O0OO0O ["rel_base2"]=OOO000O000OO000OO *1.0 /O0O0O0OO0O000OOO0 .data ["rows_count"]#line:399
            OO0O00OO000O0OO0O ["conf1"]=OO00000O0000000OO #line:400
            OO0O00OO000O0OO0O ["conf2"]=O000OO0OO0OOO0OOO #line:401
            OO0O00OO000O0OO0O ["deltaconf"]=OO00000O0000000OO -O000OO0OO0OOO0OOO #line:402
            if (O000OO0OO0OOO0OOO >0 ):#line:403
                OO0O00OO000O0OO0O ["ratioconf"]=OO00000O0000000OO *1.0 /O000OO0OO0OOO0OOO #line:404
            else :#line:405
                OO0O00OO000O0OO0O ["ratioconf"]=None #line:406
            OO0O00OO000O0OO0O ["fourfold1"]=[O00000O0OO0O0O000 ,OOOO0O000OO000O00 ,O0OOO00000OO0O00O ,O00O0O00O0OOOOOOO ]#line:407
            OO0O00OO000O0OO0O ["fourfold2"]=[O0OOOOOO000000OOO ,OOO0O0OOOOOO0OO0O ,OOO0O000O00O00OO0 ,O00O000O000OO00OO ]#line:408
        return O0O000000000OO00O ,OO0O00OO000O0OO0O #line:412
    def _verifynewact4ft (O0OO00OO00O0OOO00 ,_OO000OO0000O00OO0 ):#line:414
        O0OO0OOO00O0O0OOO ={}#line:415
        for O000OOO0O0O0O0OO0 in O0OO00OO00O0OOO00 .task_actinfo ['cedents']:#line:416
            O0OO0OOO00O0O0OOO [O000OOO0O0O0O0OO0 ['cedent_type']]=O000OOO0O0O0O0OO0 ['filter_value']#line:418
        O00O0O00O00OO0OO0 =bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:420
        O00O0000O0O0000OO =bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']&O0OO0OOO00O0O0OOO ['antv']&O0OO0OOO00O0O0OOO ['sucv']).count ("1")#line:421
        O00O000O0O0OOO00O =None #line:422
        OOO0000O000OOO00O =0 #line:423
        OOO00O00OO0O00OOO =0 #line:424
        if O00O0O00O00OO0OO0 >0 :#line:433
            OOO0000O000OOO00O =bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']).count ("1")*1.0 /bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:435
        if O00O0000O0O0000OO >0 :#line:436
            OOO00O00OO0O00OOO =bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']&O0OO0OOO00O0O0OOO ['antv']&O0OO0OOO00O0O0OOO ['sucv']).count ("1")*1.0 /bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['cond']&O0OO0OOO00O0O0OOO ['antv']).count ("1")#line:438
        O0OOO0OOO0O00O0O0 =1 <<O0OO00OO00O0OOO00 .rows_count #line:440
        OO0O000OOOOOOOO0O =bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:441
        OOOO000OO0000O0O0 =bin (O0OO0OOO00O0O0OOO ['ante']&~(O0OOO0OOO0O00O0O0 |O0OO0OOO00O0O0OOO ['succ'])&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:442
        O00O0OOOO0OOOO0O0 =bin (~(O0OOO0OOO0O00O0O0 |O0OO0OOO00O0O0OOO ['ante'])&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:443
        O000O00OO00OO00O0 =bin (~(O0OOO0OOO0O00O0O0 |O0OO0OOO00O0O0OOO ['ante'])&~(O0OOO0OOO0O00O0O0 |O0OO0OOO00O0O0OOO ['succ'])&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:444
        O0OOOOOOO0O00O0OO =bin (O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']&O0OO0OOO00O0O0OOO ['antv']&O0OO0OOO00O0O0OOO ['sucv']).count ("1")#line:445
        O0000OO0O0OOOOO00 =bin (O0OO0OOO00O0O0OOO ['ante']&~(O0OOO0OOO0O00O0O0 |(O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['sucv']))&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:446
        O000O00OO00OO0OO0 =bin (~(O0OOO0OOO0O00O0O0 |(O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['antv']))&O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['cond']&O0OO0OOO00O0O0OOO ['sucv']).count ("1")#line:447
        OOO00OO00000OO0OO =bin (~(O0OOO0OOO0O00O0O0 |(O0OO0OOO00O0O0OOO ['ante']&O0OO0OOO00O0O0OOO ['antv']))&~(O0OOO0OOO0O00O0O0 |(O0OO0OOO00O0O0OOO ['succ']&O0OO0OOO00O0O0OOO ['sucv']))&O0OO0OOO00O0O0OOO ['cond']).count ("1")#line:448
        O00000OO000OO0O00 =True #line:449
        for O00O00OOOOOO0O000 in O0OO00OO00O0OOO00 .quantifiers .keys ():#line:450
            if (O00O00OOOOOO0O000 =='PreBase')|(O00O00OOOOOO0O000 =='Base1'):#line:451
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=O00O0O00O00OO0OO0 )#line:452
            if (O00O00OOOOOO0O000 =='PostBase')|(O00O00OOOOOO0O000 =='Base2'):#line:453
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=O00O0000O0O0000OO )#line:454
            if (O00O00OOOOOO0O000 =='PreRelBase')|(O00O00OOOOOO0O000 =='RelBase1'):#line:455
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=O00O0O00O00OO0OO0 *1.0 /O0OO00OO00O0OOO00 .data ["rows_count"])#line:456
            if (O00O00OOOOOO0O000 =='PostRelBase')|(O00O00OOOOOO0O000 =='RelBase2'):#line:457
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=O00O0000O0O0000OO *1.0 /O0OO00OO00O0OOO00 .data ["rows_count"])#line:458
            if (O00O00OOOOOO0O000 =='Prepim')|(O00O00OOOOOO0O000 =='pim1')|(O00O00OOOOOO0O000 =='PreConf')|(O00O00OOOOOO0O000 =='conf1'):#line:459
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=OOO0000O000OOO00O )#line:460
            if (O00O00OOOOOO0O000 =='Postpim')|(O00O00OOOOOO0O000 =='pim2')|(O00O00OOOOOO0O000 =='PostConf')|(O00O00OOOOOO0O000 =='conf2'):#line:461
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=OOO00O00OO0O00OOO )#line:462
            if (O00O00OOOOOO0O000 =='Deltapim')|(O00O00OOOOOO0O000 =='DeltaConf'):#line:463
                O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=OOO0000O000OOO00O -OOO00O00OO0O00OOO )#line:464
            if (O00O00OOOOOO0O000 =='Ratiopim')|(O00O00OOOOOO0O000 =='RatioConf'):#line:467
                if (OOO00O00OO0O00OOO >0 ):#line:468
                    O00000OO000OO0O00 =O00000OO000OO0O00 and (O0OO00OO00O0OOO00 .quantifiers .get (O00O00OOOOOO0O000 )<=OOO0000O000OOO00O *1.0 /OOO00O00OO0O00OOO )#line:469
                else :#line:470
                    O00000OO000OO0O00 =False #line:471
        O0OOO00O0O00O00OO ={}#line:472
        if O00000OO000OO0O00 ==True :#line:473
            O0OO00OO00O0OOO00 .stats ['total_valid']+=1 #line:475
            O0OOO00O0O00O00OO ["base1"]=O00O0O00O00OO0OO0 #line:476
            O0OOO00O0O00O00OO ["base2"]=O00O0000O0O0000OO #line:477
            O0OOO00O0O00O00OO ["rel_base1"]=O00O0O00O00OO0OO0 *1.0 /O0OO00OO00O0OOO00 .data ["rows_count"]#line:478
            O0OOO00O0O00O00OO ["rel_base2"]=O00O0000O0O0000OO *1.0 /O0OO00OO00O0OOO00 .data ["rows_count"]#line:479
            O0OOO00O0O00O00OO ["conf1"]=OOO0000O000OOO00O #line:480
            O0OOO00O0O00O00OO ["conf2"]=OOO00O00OO0O00OOO #line:481
            O0OOO00O0O00O00OO ["deltaconf"]=OOO0000O000OOO00O -OOO00O00OO0O00OOO #line:482
            if (OOO00O00OO0O00OOO >0 ):#line:483
                O0OOO00O0O00O00OO ["ratioconf"]=OOO0000O000OOO00O *1.0 /OOO00O00OO0O00OOO #line:484
            else :#line:485
                O0OOO00O0O00O00OO ["ratioconf"]=None #line:486
            O0OOO00O0O00O00OO ["fourfoldpre"]=[OO0O000OOOOOOOO0O ,OOOO000OO0000O0O0 ,O00O0OOOO0OOOO0O0 ,O000O00OO00OO00O0 ]#line:487
            O0OOO00O0O00O00OO ["fourfoldpost"]=[O0OOOOOOO0O00O0OO ,O0000OO0O0OOOOO00 ,O000O00OO00OO0OO0 ,OOO00OO00000OO0OO ]#line:488
        return O00000OO000OO0O00 ,O0OOO00O0O00O00OO #line:490
    def _verifyact4ft (O0O000O0OOOOO000O ,_O00O00O0OO0O0OO00 ):#line:492
        OO00O0000O0OOOO0O ={}#line:493
        for O00O0O00O0O000000 in O0O000O0OOOOO000O .task_actinfo ['cedents']:#line:494
            OO00O0000O0OOOO0O [O00O0O00O0O000000 ['cedent_type']]=O00O0O00O0O000000 ['filter_value']#line:496
        OO0O00OO0O0O0000O =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv-']&OO00O0000O0OOOO0O ['sucv-']).count ("1")#line:498
        OO0O00000O0OO0OO0 =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv+']&OO00O0000O0OOOO0O ['sucv+']).count ("1")#line:499
        O00OOO00000O00000 =None #line:500
        O00O000O00O0O0OO0 =0 #line:501
        O00OOOOO00OOOO0O0 =0 #line:502
        if OO0O00OO0O0O0000O >0 :#line:511
            O00O000O00O0O0OO0 =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv-']&OO00O0000O0OOOO0O ['sucv-']).count ("1")*1.0 /bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv-']).count ("1")#line:513
        if OO0O00000O0OO0OO0 >0 :#line:514
            O00OOOOO00OOOO0O0 =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv+']&OO00O0000O0OOOO0O ['sucv+']).count ("1")*1.0 /bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv+']).count ("1")#line:516
        O00000OOO0O00O0O0 =1 <<O0O000O0OOOOO000O .data ["rows_count"]#line:518
        O0O000OOOO0O00OO0 =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv-']&OO00O0000O0OOOO0O ['sucv-']).count ("1")#line:519
        O0O000O0OOOO0OO00 =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['antv-']&~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['sucv-']))&OO00O0000O0OOOO0O ['cond']).count ("1")#line:520
        OOO0OOOOOO0O0O0OO =bin (~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['antv-']))&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['sucv-']).count ("1")#line:521
        O0O0O0000O000OO00 =bin (~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['antv-']))&~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['sucv-']))&OO00O0000O0OOOO0O ['cond']).count ("1")#line:522
        O0000OOO0OO0O0OOO =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['antv+']&OO00O0000O0OOOO0O ['sucv+']).count ("1")#line:523
        OOO0O0O00000OO000 =bin (OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['antv+']&~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['sucv+']))&OO00O0000O0OOOO0O ['cond']).count ("1")#line:524
        O00O0OO0OOOO0O0O0 =bin (~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['antv+']))&OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['cond']&OO00O0000O0OOOO0O ['sucv+']).count ("1")#line:525
        O0OO00000O0O0000O =bin (~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['ante']&OO00O0000O0OOOO0O ['antv+']))&~(O00000OOO0O00O0O0 |(OO00O0000O0OOOO0O ['succ']&OO00O0000O0OOOO0O ['sucv+']))&OO00O0000O0OOOO0O ['cond']).count ("1")#line:526
        O0OO0O00O00OO0OO0 =True #line:527
        for OOO0O000000000OOO in O0O000O0OOOOO000O .quantifiers .keys ():#line:528
            if (OOO0O000000000OOO =='PreBase')|(OOO0O000000000OOO =='Base1'):#line:529
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=OO0O00OO0O0O0000O )#line:530
            if (OOO0O000000000OOO =='PostBase')|(OOO0O000000000OOO =='Base2'):#line:531
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=OO0O00000O0OO0OO0 )#line:532
            if (OOO0O000000000OOO =='PreRelBase')|(OOO0O000000000OOO =='RelBase1'):#line:533
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=OO0O00OO0O0O0000O *1.0 /O0O000O0OOOOO000O .data ["rows_count"])#line:534
            if (OOO0O000000000OOO =='PostRelBase')|(OOO0O000000000OOO =='RelBase2'):#line:535
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=OO0O00000O0OO0OO0 *1.0 /O0O000O0OOOOO000O .data ["rows_count"])#line:536
            if (OOO0O000000000OOO =='Prepim')|(OOO0O000000000OOO =='pim1')|(OOO0O000000000OOO =='PreConf')|(OOO0O000000000OOO =='conf1'):#line:537
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=O00O000O00O0O0OO0 )#line:538
            if (OOO0O000000000OOO =='Postpim')|(OOO0O000000000OOO =='pim2')|(OOO0O000000000OOO =='PostConf')|(OOO0O000000000OOO =='conf2'):#line:539
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=O00OOOOO00OOOO0O0 )#line:540
            if (OOO0O000000000OOO =='Deltapim')|(OOO0O000000000OOO =='DeltaConf'):#line:541
                O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=O00O000O00O0O0OO0 -O00OOOOO00OOOO0O0 )#line:542
            if (OOO0O000000000OOO =='Ratiopim')|(OOO0O000000000OOO =='RatioConf'):#line:545
                if (O00O000O00O0O0OO0 >0 ):#line:546
                    O0OO0O00O00OO0OO0 =O0OO0O00O00OO0OO0 and (O0O000O0OOOOO000O .quantifiers .get (OOO0O000000000OOO )<=O00OOOOO00OOOO0O0 *1.0 /O00O000O00O0O0OO0 )#line:547
                else :#line:548
                    O0OO0O00O00OO0OO0 =False #line:549
        OO000O0O0O0000O0O ={}#line:550
        if O0OO0O00O00OO0OO0 ==True :#line:551
            O0O000O0OOOOO000O .stats ['total_valid']+=1 #line:553
            OO000O0O0O0000O0O ["base1"]=OO0O00OO0O0O0000O #line:554
            OO000O0O0O0000O0O ["base2"]=OO0O00000O0OO0OO0 #line:555
            OO000O0O0O0000O0O ["rel_base1"]=OO0O00OO0O0O0000O *1.0 /O0O000O0OOOOO000O .data ["rows_count"]#line:556
            OO000O0O0O0000O0O ["rel_base2"]=OO0O00000O0OO0OO0 *1.0 /O0O000O0OOOOO000O .data ["rows_count"]#line:557
            OO000O0O0O0000O0O ["conf1"]=O00O000O00O0O0OO0 #line:558
            OO000O0O0O0000O0O ["conf2"]=O00OOOOO00OOOO0O0 #line:559
            OO000O0O0O0000O0O ["deltaconf"]=O00O000O00O0O0OO0 -O00OOOOO00OOOO0O0 #line:560
            if (O00O000O00O0O0OO0 >0 ):#line:561
                OO000O0O0O0000O0O ["ratioconf"]=O00OOOOO00OOOO0O0 *1.0 /O00O000O00O0O0OO0 #line:562
            else :#line:563
                OO000O0O0O0000O0O ["ratioconf"]=None #line:564
            OO000O0O0O0000O0O ["fourfoldpre"]=[O0O000OOOO0O00OO0 ,O0O000O0OOOO0OO00 ,OOO0OOOOOO0O0O0OO ,O0O0O0000O000OO00 ]#line:565
            OO000O0O0O0000O0O ["fourfoldpost"]=[O0000OOO0OO0O0OOO ,OOO0O0O00000OO000 ,O00O0OO0OOOO0O0O0 ,O0OO00000O0O0000O ]#line:566
        return O0OO0O00O00OO0OO0 ,OO000O0O0O0000O0O #line:568
    def _verify_opt (OO00OOOOOO0OO0O0O ,OO00O0OOO00O00O0O ,O000O00O00OOOO000 ):#line:570
        OOOOO0OO000O0000O =False #line:571
        if not (OO00O0OOO00O00O0O ['optim'].get ('only_con')):#line:574
            return False #line:575
        OOO0OOOOOOO0O00O0 ={}#line:576
        for OOO000OO0OO0O00OO in OO00OOOOOO0OO0O0O .task_actinfo ['cedents']:#line:577
            OOO0OOOOOOO0O00O0 [OOO000OO0OO0O00OO ['cedent_type']]=OOO000OO0OO0O00OO ['filter_value']#line:579
        O000OO0OO0000O0O0 =1 <<OO00OOOOOO0OO0O0O .data ["rows_count"]#line:581
        O000O0O000O0OO0O0 =O000OO0OO0000O0O0 -1 #line:582
        OOO00O000O0O000OO =""#line:583
        OOOOOOOOOOO00OOOO =0 #line:584
        if (OOO0OOOOOOO0O00O0 .get ('ante')!=None ):#line:585
            O000O0O000O0OO0O0 =O000O0O000O0OO0O0 &OOO0OOOOOOO0O00O0 ['ante']#line:586
        if (OOO0OOOOOOO0O00O0 .get ('succ')!=None ):#line:587
            O000O0O000O0OO0O0 =O000O0O000O0OO0O0 &OOO0OOOOOOO0O00O0 ['succ']#line:588
        if (OOO0OOOOOOO0O00O0 .get ('cond')!=None ):#line:589
            O000O0O000O0OO0O0 =O000O0O000O0OO0O0 &OOO0OOOOOOO0O00O0 ['cond']#line:590
        OOOO00O00O000O000 =None #line:593
        if (OO00OOOOOO0OO0O0O .proc =='CFMiner')|(OO00OOOOOO0OO0O0O .proc =='4ftMiner'):#line:618
            OO0O0OO000OO0O00O =bin (O000O0O000O0OO0O0 ).count ("1")#line:619
            for OO0OOO00OO0OOOOOO in OO00OOOOOO0OO0O0O .quantifiers .keys ():#line:620
                if OO0OOO00OO0OOOOOO =='Base':#line:621
                    if not (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O ):#line:622
                        OOOOO0OO000O0000O =True #line:623
                if OO0OOO00OO0OOOOOO =='RelBase':#line:625
                    if not (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O *1.0 /OO00OOOOOO0OO0O0O .data ["rows_count"]):#line:626
                        OOOOO0OO000O0000O =True #line:627
        return OOOOO0OO000O0000O #line:630
        if OO00OOOOOO0OO0O0O .proc =='CFMiner':#line:633
            if (O000O00O00OOOO000 ['cedent_type']=='cond')&(O000O00O00OOOO000 ['defi'].get ('type')=='con'):#line:634
                OO0O0OO000OO0O00O =bin (OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:635
                O0O0OOO00OOOO00O0 =True #line:636
                for OO0OOO00OO0OOOOOO in OO00OOOOOO0OO0O0O .quantifiers .keys ():#line:637
                    if OO0OOO00OO0OOOOOO =='Base':#line:638
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O )#line:639
                        if not (O0O0OOO00OOOO00O0 ):#line:640
                            print (f"...optimization : base is {OO0O0OO000OO0O00O} for {O000O00O00OOOO000['generated_string']}")#line:641
                    if OO0OOO00OO0OOOOOO =='RelBase':#line:642
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O *1.0 /OO00OOOOOO0OO0O0O .data ["rows_count"])#line:643
                        if not (O0O0OOO00OOOO00O0 ):#line:644
                            print (f"...optimization : base is {OO0O0OO000OO0O00O} for {O000O00O00OOOO000['generated_string']}")#line:645
                OOOOO0OO000O0000O =not (O0O0OOO00OOOO00O0 )#line:646
        elif OO00OOOOOO0OO0O0O .proc =='4ftMiner':#line:647
            if (O000O00O00OOOO000 ['cedent_type']=='cond')&(O000O00O00OOOO000 ['defi'].get ('type')=='con'):#line:648
                OO0O0OO000OO0O00O =bin (OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:649
                O0O0OOO00OOOO00O0 =True #line:650
                for OO0OOO00OO0OOOOOO in OO00OOOOOO0OO0O0O .quantifiers .keys ():#line:651
                    if OO0OOO00OO0OOOOOO =='Base':#line:652
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O )#line:653
                        if not (O0O0OOO00OOOO00O0 ):#line:654
                            print (f"...optimization : base is {OO0O0OO000OO0O00O} for {O000O00O00OOOO000['generated_string']}")#line:655
                    if OO0OOO00OO0OOOOOO =='RelBase':#line:656
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O *1.0 /OO00OOOOOO0OO0O0O .data ["rows_count"])#line:657
                        if not (O0O0OOO00OOOO00O0 ):#line:658
                            print (f"...optimization : base is {OO0O0OO000OO0O00O} for {O000O00O00OOOO000['generated_string']}")#line:659
                OOOOO0OO000O0000O =not (O0O0OOO00OOOO00O0 )#line:660
            if (O000O00O00OOOO000 ['cedent_type']=='ante')&(O000O00O00OOOO000 ['defi'].get ('type')=='con'):#line:661
                OO0O0OO000OO0O00O =bin (OOO0OOOOOOO0O00O0 ['ante']&OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:662
                O0O0OOO00OOOO00O0 =True #line:663
                for OO0OOO00OO0OOOOOO in OO00OOOOOO0OO0O0O .quantifiers .keys ():#line:664
                    if OO0OOO00OO0OOOOOO =='Base':#line:665
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O )#line:666
                        if not (O0O0OOO00OOOO00O0 ):#line:667
                            print (f"...optimization : ANTE: base is {OO0O0OO000OO0O00O} for {O000O00O00OOOO000['generated_string']}")#line:668
                    if OO0OOO00OO0OOOOOO =='RelBase':#line:669
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OO0O0OO000OO0O00O *1.0 /OO00OOOOOO0OO0O0O .data ["rows_count"])#line:670
                        if not (O0O0OOO00OOOO00O0 ):#line:671
                            print (f"...optimization : ANTE:  base is {OO0O0OO000OO0O00O} for {O000O00O00OOOO000['generated_string']}")#line:672
                OOOOO0OO000O0000O =not (O0O0OOO00OOOO00O0 )#line:673
            if (O000O00O00OOOO000 ['cedent_type']=='succ')&(O000O00O00OOOO000 ['defi'].get ('type')=='con'):#line:674
                OO0O0OO000OO0O00O =bin (OOO0OOOOOOO0O00O0 ['ante']&OOO0OOOOOOO0O00O0 ['cond']&OOO0OOOOOOO0O00O0 ['succ']).count ("1")#line:675
                OOOO00O00O000O000 =0 #line:676
                if OO0O0OO000OO0O00O >0 :#line:677
                    OOOO00O00O000O000 =bin (OOO0OOOOOOO0O00O0 ['ante']&OOO0OOOOOOO0O00O0 ['succ']&OOO0OOOOOOO0O00O0 ['cond']).count ("1")*1.0 /bin (OOO0OOOOOOO0O00O0 ['ante']&OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:678
                O000OO0OO0000O0O0 =1 <<OO00OOOOOO0OO0O0O .data ["rows_count"]#line:679
                O00O00O0OO0OO0OO0 =bin (OOO0OOOOOOO0O00O0 ['ante']&OOO0OOOOOOO0O00O0 ['succ']&OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:680
                O00OOOO0OOO0O0O0O =bin (OOO0OOOOOOO0O00O0 ['ante']&~(O000OO0OO0000O0O0 |OOO0OOOOOOO0O00O0 ['succ'])&OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:681
                OOO000OO0OO0O00OO =bin (~(O000OO0OO0000O0O0 |OOO0OOOOOOO0O00O0 ['ante'])&OOO0OOOOOOO0O00O0 ['succ']&OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:682
                OOOO0O0O000OO00O0 =bin (~(O000OO0OO0000O0O0 |OOO0OOOOOOO0O00O0 ['ante'])&~(O000OO0OO0000O0O0 |OOO0OOOOOOO0O00O0 ['succ'])&OOO0OOOOOOO0O00O0 ['cond']).count ("1")#line:683
                O0O0OOO00OOOO00O0 =True #line:684
                for OO0OOO00OO0OOOOOO in OO00OOOOOO0OO0O0O .quantifiers .keys ():#line:685
                    if OO0OOO00OO0OOOOOO =='pim':#line:686
                        O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=OOOO00O00O000O000 )#line:687
                    if not (O0O0OOO00OOOO00O0 ):#line:688
                        print (f"...optimization : SUCC:  pim is {OOOO00O00O000O000} for {O000O00O00OOOO000['generated_string']}")#line:689
                    if OO0OOO00OO0OOOOOO =='aad':#line:691
                        if (O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O )*(O00O00O0OO0OO0OO0 +OOO000OO0OO0O00OO )>0 :#line:692
                            O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=O00O00O0OO0OO0OO0 *(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O +OOO000OO0OO0O00OO +OOOO0O0O000OO00O0 )/(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O )/(O00O00O0OO0OO0OO0 +OOO000OO0OO0O00OO )-1 )#line:693
                        else :#line:694
                            O0O0OOO00OOOO00O0 =False #line:695
                        if not (O0O0OOO00OOOO00O0 ):#line:696
                            OOO000000OO00O00O =O00O00O0OO0OO0OO0 *(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O +OOO000OO0OO0O00OO +OOOO0O0O000OO00O0 )/(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O )/(O00O00O0OO0OO0OO0 +OOO000OO0OO0O00OO )-1 #line:697
                            print (f"...optimization : SUCC:  aad is {OOO000000OO00O00O} for {O000O00O00OOOO000['generated_string']}")#line:698
                    if OO0OOO00OO0OOOOOO =='bad':#line:699
                        if (O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O )*(O00O00O0OO0OO0OO0 +OOO000OO0OO0O00OO )>0 :#line:700
                            O0O0OOO00OOOO00O0 =O0O0OOO00OOOO00O0 and (OO00OOOOOO0OO0O0O .quantifiers .get (OO0OOO00OO0OOOOOO )<=1 -O00O00O0OO0OO0OO0 *(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O +OOO000OO0OO0O00OO +OOOO0O0O000OO00O0 )/(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O )/(O00O00O0OO0OO0OO0 +OOO000OO0OO0O00OO ))#line:701
                        else :#line:702
                            O0O0OOO00OOOO00O0 =False #line:703
                        if not (O0O0OOO00OOOO00O0 ):#line:704
                            OOOO0O0OOO0OOOO00 =1 -O00O00O0OO0OO0OO0 *(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O +OOO000OO0OO0O00OO +OOOO0O0O000OO00O0 )/(O00O00O0OO0OO0OO0 +O00OOOO0OOO0O0O0O )/(O00O00O0OO0OO0OO0 +OOO000OO0OO0O00OO )#line:705
                            print (f"...optimization : SUCC:  bad is {OOOO0O0OOO0OOOO00} for {O000O00O00OOOO000['generated_string']}")#line:706
                OOOOO0OO000O0000O =not (O0O0OOO00OOOO00O0 )#line:707
        if (OOOOO0OO000O0000O ):#line:708
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O000O00O00OOOO000['cedent_type']}")#line:709
        return OOOOO0OO000O0000O #line:710
    def _print (OO0OO0OO0OOO0O000 ,OO000OOO0O00OOOO0 ,_OOOOOO0000OOO0000 ,_O00OO00O0OO00OO0O ):#line:713
        if (len (_OOOOOO0000OOO0000 ))!=len (_O00OO00O0OO00OO0O ):#line:714
            print ("DIFF IN LEN for following cedent : "+str (len (_OOOOOO0000OOO0000 ))+" vs "+str (len (_O00OO00O0OO00OO0O )))#line:715
            print ("trace cedent : "+str (_OOOOOO0000OOO0000 )+", traces "+str (_O00OO00O0OO00OO0O ))#line:716
        O0O0OO0O0O0OO0OOO =''#line:717
        for O0OOO0OOOOO0OOOO0 in range (len (_OOOOOO0000OOO0000 )):#line:718
            O0OOOOOO0O00OO00O =OO0OO0OO0OOO0O000 .data ["varname"].index (OO000OOO0O00OOOO0 ['defi'].get ('attributes')[_OOOOOO0000OOO0000 [O0OOO0OOOOO0OOOO0 ]].get ('name'))#line:719
            O0O0OO0O0O0OO0OOO =O0O0OO0O0O0OO0OOO +OO0OO0OO0OOO0O000 .data ["varname"][O0OOOOOO0O00OO00O ]+'('#line:721
            for OO0OOOOO0OOO0000O in _O00OO00O0OO00OO0O [O0OOO0OOOOO0OOOO0 ]:#line:722
                O0O0OO0O0O0OO0OOO =O0O0OO0O0O0OO0OOO +str (OO0OO0OO0OOO0O000 .data ["catnames"][O0OOOOOO0O00OO00O ][OO0OOOOO0OOO0000O ])+" "#line:723
            O0O0OO0O0O0OO0OOO =O0O0OO0O0O0OO0OOO +')'#line:724
            if O0OOO0OOOOO0OOOO0 +1 <len (_OOOOOO0000OOO0000 ):#line:725
                O0O0OO0O0O0OO0OOO =O0O0OO0O0O0OO0OOO +' & '#line:726
        return O0O0OO0O0O0OO0OOO #line:730
    def _print_hypo (OO00OOOOOO0O000O0 ,OOO0OO00OO000OOO0 ):#line:732
        OO00OOOOOO0O000O0 .print_rule (OOO0OO00OO000OOO0 )#line:733
    def _print_rule (O0O00OO0000OO0O00 ,OO0OOO0OO0OO0OO00 ):#line:735
        print ('Rules info : '+str (OO0OOO0OO0OO0OO00 ['params']))#line:736
        for O0000OOO0OOOO0OOO in O0O00OO0000OO0O00 .task_actinfo ['cedents']:#line:737
            print (O0000OOO0OOOO0OOO ['cedent_type']+' = '+O0000OOO0OOOO0OOO ['generated_string'])#line:738
    def _genvar (O0000O0OO00000OO0 ,O0O00OOO000OOO0OO ,OOOOOOOO0OO0OOO00 ,_OOO0O0OOO00OO00OO ,_OO0O00OOO0O0O0000 ,_OO0000OOOO0000000 ,_OO0000OOO0OO00O0O ,_O0000OOOOOO00OO0O ):#line:740
        for OOO00OO000O0000O0 in range (OOOOOOOO0OO0OOO00 ['num_cedent']):#line:741
            if len (_OOO0O0OOO00OO00OO )==0 or OOO00OO000O0000O0 >_OOO0O0OOO00OO00OO [-1 ]:#line:742
                _OOO0O0OOO00OO00OO .append (OOO00OO000O0000O0 )#line:743
                O0O0O00000OOOO000 =O0000O0OO00000OO0 .data ["varname"].index (OOOOOOOO0OO0OOO00 ['defi'].get ('attributes')[OOO00OO000O0000O0 ].get ('name'))#line:744
                _OOOOOO0O0O00OO00O =OOOOOOOO0OO0OOO00 ['defi'].get ('attributes')[OOO00OO000O0000O0 ].get ('minlen')#line:745
                _OO00O0O00O0OOOO00 =OOOOOOOO0OO0OOO00 ['defi'].get ('attributes')[OOO00OO000O0000O0 ].get ('maxlen')#line:746
                _O00OOOOO00O00000O =OOOOOOOO0OO0OOO00 ['defi'].get ('attributes')[OOO00OO000O0000O0 ].get ('type')#line:747
                OOO0000000O0O0O0O =len (O0000O0OO00000OO0 .data ["dm"][O0O0O00000OOOO000 ])#line:748
                _OOO0OO0000O00O00O =[]#line:749
                _OO0O00OOO0O0O0000 .append (_OOO0OO0000O00O00O )#line:750
                _OOO0O00OO0OO000OO =int (0 )#line:751
                O0000O0OO00000OO0 ._gencomb (O0O00OOO000OOO0OO ,OOOOOOOO0OO0OOO00 ,_OOO0O0OOO00OO00OO ,_OO0O00OOO0O0O0000 ,_OOO0OO0000O00O00O ,_OO0000OOOO0000000 ,_OOO0O00OO0OO000OO ,OOO0000000O0O0O0O ,_O00OOOOO00O00000O ,_OO0000OOO0OO00O0O ,_O0000OOOOOO00OO0O ,_OOOOOO0O0O00OO00O ,_OO00O0O00O0OOOO00 )#line:752
                _OO0O00OOO0O0O0000 .pop ()#line:753
                _OOO0O0OOO00OO00OO .pop ()#line:754
    def _gencomb (OO00O000O0OO00O0O ,OOO000OOO0O000OO0 ,OO000OOOO000O0000 ,_O000000O0OOO0O0O0 ,_O00000OO0OOOOO000 ,_OOO00O00O0OO0OO0O ,_O0000O0O00OOOOOO0 ,_O0O0O0OO0000OOOOO ,OOOOOOOO00O000OO0 ,_OO0000O00OO0OO0OO ,_O000O00O0O00OO0O0 ,_OOO00OOOO0OOO0O00 ,_O0000OO0O00000000 ,_OO0OOOOOO0O0O0O00 ):#line:756
        _OOOOO0OOO00OO0000 =[]#line:757
        if _OO0000O00OO0OO0OO =="subset":#line:758
            if len (_OOO00O00O0OO0OO0O )==0 :#line:759
                _OOOOO0OOO00OO0000 =range (OOOOOOOO00O000OO0 )#line:760
            else :#line:761
                _OOOOO0OOO00OO0000 =range (_OOO00O00O0OO0OO0O [-1 ]+1 ,OOOOOOOO00O000OO0 )#line:762
        elif _OO0000O00OO0OO0OO =="seq":#line:763
            if len (_OOO00O00O0OO0OO0O )==0 :#line:764
                _OOOOO0OOO00OO0000 =range (OOOOOOOO00O000OO0 -_O0000OO0O00000000 +1 )#line:765
            else :#line:766
                if _OOO00O00O0OO0OO0O [-1 ]+1 ==OOOOOOOO00O000OO0 :#line:767
                    return #line:768
                O000OO0O0O0O00000 =_OOO00O00O0OO0OO0O [-1 ]+1 #line:769
                _OOOOO0OOO00OO0000 .append (O000OO0O0O0O00000 )#line:770
        elif _OO0000O00OO0OO0OO =="lcut":#line:771
            if len (_OOO00O00O0OO0OO0O )==0 :#line:772
                O000OO0O0O0O00000 =0 ;#line:773
            else :#line:774
                if _OOO00O00O0OO0OO0O [-1 ]+1 ==OOOOOOOO00O000OO0 :#line:775
                    return #line:776
                O000OO0O0O0O00000 =_OOO00O00O0OO0OO0O [-1 ]+1 #line:777
            _OOOOO0OOO00OO0000 .append (O000OO0O0O0O00000 )#line:778
        elif _OO0000O00OO0OO0OO =="rcut":#line:779
            if len (_OOO00O00O0OO0OO0O )==0 :#line:780
                O000OO0O0O0O00000 =OOOOOOOO00O000OO0 -1 ;#line:781
            else :#line:782
                if _OOO00O00O0OO0OO0O [-1 ]==0 :#line:783
                    return #line:784
                O000OO0O0O0O00000 =_OOO00O00O0OO0OO0O [-1 ]-1 #line:785
            _OOOOO0OOO00OO0000 .append (O000OO0O0O0O00000 )#line:787
        elif _OO0000O00OO0OO0OO =="one":#line:788
            if len (_OOO00O00O0OO0OO0O )==0 :#line:789
                OOO00OOOOO0O0000O =OO00O000O0OO00O0O .data ["varname"].index (OO000OOOO000O0000 ['defi'].get ('attributes')[_O000000O0OOO0O0O0 [-1 ]].get ('name'))#line:790
                try :#line:791
                    O000OO0O0O0O00000 =OO00O000O0OO00O0O .data ["catnames"][OOO00OOOOO0O0000O ].index (OO000OOOO000O0000 ['defi'].get ('attributes')[_O000000O0OOO0O0O0 [-1 ]].get ('value'))#line:792
                except :#line:793
                    print (f"ERROR: attribute '{OO000OOOO000O0000['defi'].get('attributes')[_O000000O0OOO0O0O0[-1]].get('name')}' has not value '{OO000OOOO000O0000['defi'].get('attributes')[_O000000O0OOO0O0O0[-1]].get('value')}'")#line:794
                    exit (1 )#line:795
                _OOOOO0OOO00OO0000 .append (O000OO0O0O0O00000 )#line:796
                _O0000OO0O00000000 =1 #line:797
                _OO0OOOOOO0O0O0O00 =1 #line:798
            else :#line:799
                print ("DEBUG: one category should not have more categories")#line:800
                return #line:801
        else :#line:802
            print ("Attribute type "+_OO0000O00OO0OO0OO +" not supported.")#line:803
            return #line:804
        for OO0OO0O00OOO0O0O0 in _OOOOO0OOO00OO0000 :#line:807
                _OOO00O00O0OO0OO0O .append (OO0OO0O00OOO0O0O0 )#line:809
                _O00000OO0OOOOO000 .pop ()#line:810
                _O00000OO0OOOOO000 .append (_OOO00O00O0OO0OO0O )#line:811
                _O00O0OOOOOOOO00OO =_O0O0O0OO0000OOOOO |OO00O000O0OO00O0O .data ["dm"][OO00O000O0OO00O0O .data ["varname"].index (OO000OOOO000O0000 ['defi'].get ('attributes')[_O000000O0OOO0O0O0 [-1 ]].get ('name'))][OO0OO0O00OOO0O0O0 ]#line:815
                _O0O00OOO0O0O000O0 =1 #line:817
                if (len (_O000000O0OOO0O0O0 )<_O000O00O0O00OO0O0 ):#line:818
                    _O0O00OOO0O0O000O0 =-1 #line:819
                if (len (_O00000OO0OOOOO000 [-1 ])<_O0000OO0O00000000 ):#line:821
                    _O0O00OOO0O0O000O0 =0 #line:822
                _OO0O0OO0OO00000O0 =0 #line:824
                if OO000OOOO000O0000 ['defi'].get ('type')=='con':#line:825
                    _OO0O0OO0OO00000O0 =_O0000O0O00OOOOOO0 &_O00O0OOOOOOOO00OO #line:826
                else :#line:827
                    _OO0O0OO0OO00000O0 =_O0000O0O00OOOOOO0 |_O00O0OOOOOOOO00OO #line:828
                OO000OOOO000O0000 ['trace_cedent']=_O000000O0OOO0O0O0 #line:829
                OO000OOOO000O0000 ['traces']=_O00000OO0OOOOO000 #line:830
                OO000OOOO000O0000 ['generated_string']=OO00O000O0OO00O0O ._print (OO000OOOO000O0000 ,_O000000O0OOO0O0O0 ,_O00000OO0OOOOO000 )#line:831
                OO000OOOO000O0000 ['filter_value']=_OO0O0OO0OO00000O0 #line:832
                OOO000OOO0O000OO0 ['cedents'].append (OO000OOOO000O0000 )#line:833
                O0O000OO00000O0OO =OO00O000O0OO00O0O ._verify_opt (OOO000OOO0O000OO0 ,OO000OOOO000O0000 )#line:834
                if not (O0O000OO00000O0OO ):#line:840
                    if _O0O00OOO0O0O000O0 ==1 :#line:841
                        if len (OOO000OOO0O000OO0 ['cedents_to_do'])==len (OOO000OOO0O000OO0 ['cedents']):#line:843
                            if OO00O000O0OO00O0O .proc =='CFMiner':#line:844
                                O0O0O0OO000O0OOOO ,O000OO0O0OO0O0OO0 =OO00O000O0OO00O0O ._verifyCF (_OO0O0OO0OO00000O0 )#line:845
                            elif OO00O000O0OO00O0O .proc =='4ftMiner':#line:846
                                O0O0O0OO000O0OOOO ,O000OO0O0OO0O0OO0 =OO00O000O0OO00O0O ._verify4ft (_O00O0OOOOOOOO00OO )#line:847
                            elif OO00O000O0OO00O0O .proc =='SD4ftMiner':#line:848
                                O0O0O0OO000O0OOOO ,O000OO0O0OO0O0OO0 =OO00O000O0OO00O0O ._verifysd4ft (_O00O0OOOOOOOO00OO )#line:849
                            elif OO00O000O0OO00O0O .proc =='NewAct4ftMiner':#line:850
                                O0O0O0OO000O0OOOO ,O000OO0O0OO0O0OO0 =OO00O000O0OO00O0O ._verifynewact4ft (_O00O0OOOOOOOO00OO )#line:851
                            elif OO00O000O0OO00O0O .proc =='Act4ftMiner':#line:852
                                O0O0O0OO000O0OOOO ,O000OO0O0OO0O0OO0 =OO00O000O0OO00O0O ._verifyact4ft (_O00O0OOOOOOOO00OO )#line:853
                            else :#line:854
                                print ("Unsupported procedure : "+OO00O000O0OO00O0O .proc )#line:855
                                exit (0 )#line:856
                            if O0O0O0OO000O0OOOO ==True :#line:857
                                O0O0O0000O0OO0000 ={}#line:858
                                O0O0O0000O0OO0000 ["rule_id"]=OO00O000O0OO00O0O .stats ['total_valid']#line:859
                                O0O0O0000O0OO0000 ["cedents"]={}#line:860
                                for O00O0OO0O0O0O0OO0 in OOO000OOO0O000OO0 ['cedents']:#line:861
                                    O0O0O0000O0OO0000 ['cedents'][O00O0OO0O0O0O0OO0 ['cedent_type']]=O00O0OO0O0O0O0OO0 ['generated_string']#line:862
                                O0O0O0000O0OO0000 ["params"]=O000OO0O0OO0O0OO0 #line:864
                                O0O0O0000O0OO0000 ["trace_cedent"]=_O000000O0OOO0O0O0 #line:865
                                OO00O000O0OO00O0O ._print_rule (O0O0O0000O0OO0000 )#line:866
                                O0O0O0000O0OO0000 ["traces"]=_O00000OO0OOOOO000 #line:869
                                OO00O000O0OO00O0O .rulelist .append (O0O0O0000O0OO0000 )#line:870
                            OO00O000O0OO00O0O .stats ['total_cnt']+=1 #line:871
                    if _O0O00OOO0O0O000O0 >=0 :#line:872
                        if len (OOO000OOO0O000OO0 ['cedents_to_do'])>len (OOO000OOO0O000OO0 ['cedents']):#line:873
                            OO00O000O0OO00O0O ._start_cedent (OOO000OOO0O000OO0 )#line:874
                    OOO000OOO0O000OO0 ['cedents'].pop ()#line:875
                    if (len (_O000000O0OOO0O0O0 )<_OOO00OOOO0OOO0O00 ):#line:876
                        OO00O000O0OO00O0O ._genvar (OOO000OOO0O000OO0 ,OO000OOOO000O0000 ,_O000000O0OOO0O0O0 ,_O00000OO0OOOOO000 ,_OO0O0OO0OO00000O0 ,_O000O00O0O00OO0O0 ,_OOO00OOOO0OOO0O00 )#line:877
                else :#line:878
                    OOO000OOO0O000OO0 ['cedents'].pop ()#line:879
                if len (_OOO00O00O0OO0OO0O )<_OO0OOOOOO0O0O0O00 :#line:880
                    OO00O000O0OO00O0O ._gencomb (OOO000OOO0O000OO0 ,OO000OOOO000O0000 ,_O000000O0OOO0O0O0 ,_O00000OO0OOOOO000 ,_OOO00O00O0OO0OO0O ,_O0000O0O00OOOOOO0 ,_O00O0OOOOOOOO00OO ,OOOOOOOO00O000OO0 ,_OO0000O00OO0OO0OO ,_O000O00O0O00OO0O0 ,_OOO00OOOO0OOO0O00 ,_O0000OO0O00000000 ,_OO0OOOOOO0O0O0O00 )#line:881
                _OOO00O00O0OO0OO0O .pop ()#line:882
    def _start_cedent (OO00O0O000OOOO000 ,OO00000OOOO0OOO0O ):#line:884
        if len (OO00000OOOO0OOO0O ['cedents_to_do'])>len (OO00000OOOO0OOO0O ['cedents']):#line:885
            _O0O0O0O000O00O0O0 =[]#line:886
            _OOOO00OOOO000O00O =[]#line:887
            OO0O0O00OOOO0OOOO ={}#line:888
            OO0O0O00OOOO0OOOO ['cedent_type']=OO00000OOOO0OOO0O ['cedents_to_do'][len (OO00000OOOO0OOO0O ['cedents'])]#line:889
            O0OO0OO00O000OO0O =OO0O0O00OOOO0OOOO ['cedent_type']#line:890
            if ((O0OO0OO00O000OO0O [-1 ]=='-')|(O0OO0OO00O000OO0O [-1 ]=='+')):#line:891
                O0OO0OO00O000OO0O =O0OO0OO00O000OO0O [:-1 ]#line:892
            OO0O0O00OOOO0OOOO ['defi']=OO00O0O000OOOO000 .kwargs .get (O0OO0OO00O000OO0O )#line:894
            if (OO0O0O00OOOO0OOOO ['defi']==None ):#line:895
                print ("Error getting cedent ",OO0O0O00OOOO0OOOO ['cedent_type'])#line:896
            _O00000OO00O0000OO =int (0 )#line:897
            OO0O0O00OOOO0OOOO ['num_cedent']=len (OO0O0O00OOOO0OOOO ['defi'].get ('attributes'))#line:902
            if (OO0O0O00OOOO0OOOO ['defi'].get ('type')=='con'):#line:903
                _O00000OO00O0000OO =(1 <<OO00O0O000OOOO000 .data ["rows_count"])-1 #line:904
            OO00O0O000OOOO000 ._genvar (OO00000OOOO0OOO0O ,OO0O0O00OOOO0OOOO ,_O0O0O0O000O00O0O0 ,_OOOO00OOOO000O00O ,_O00000OO00O0000OO ,OO0O0O00OOOO0OOOO ['defi'].get ('minlen'),OO0O0O00OOOO0OOOO ['defi'].get ('maxlen'))#line:905
    def _calc_all (OO00O000OOOO0OOO0 ,**OO000O0000O0OOOO0 ):#line:908
        OO00O000OOOO0OOO0 ._prep_data (OO00O000OOOO0OOO0 .kwargs .get ("df"))#line:909
        OO00O000OOOO0OOO0 ._calculate (**OO000O0000O0OOOO0 )#line:910
    def _check_cedents (OO0OOO00O0OOO0000 ,O0OOO00OOOOO0OO00 ,**OOO000O00OOO0O00O ):#line:912
        OO0O000O0O00O0OO0 =True #line:913
        if (OOO000O00OOO0O00O .get ('quantifiers',None )==None ):#line:914
            print (f"Error: missing quantifiers.")#line:915
            OO0O000O0O00O0OO0 =False #line:916
            return OO0O000O0O00O0OO0 #line:917
        if (type (OOO000O00OOO0O00O .get ('quantifiers'))!=dict ):#line:918
            print (f"Error: quantifiers are not dictionary type.")#line:919
            OO0O000O0O00O0OO0 =False #line:920
            return OO0O000O0O00O0OO0 #line:921
        for OOO0000O0000OOO0O in O0OOO00OOOOO0OO00 :#line:923
            if (OOO000O00OOO0O00O .get (OOO0000O0000OOO0O ,None )==None ):#line:924
                print (f"Error: cedent {OOO0000O0000OOO0O} is missing in parameters.")#line:925
                OO0O000O0O00O0OO0 =False #line:926
                return OO0O000O0O00O0OO0 #line:927
            OOOO0O000000OOOO0 =OOO000O00OOO0O00O .get (OOO0000O0000OOO0O )#line:928
            if (OOOO0O000000OOOO0 .get ('minlen'),None )==None :#line:929
                print (f"Error: cedent {OOO0000O0000OOO0O} has no minimal length specified.")#line:930
                OO0O000O0O00O0OO0 =False #line:931
                return OO0O000O0O00O0OO0 #line:932
            if not (type (OOOO0O000000OOOO0 .get ('minlen'))is int ):#line:933
                print (f"Error: cedent {OOO0000O0000OOO0O} has invalid type of minimal length ({type(OOOO0O000000OOOO0.get('minlen'))}).")#line:934
                OO0O000O0O00O0OO0 =False #line:935
                return OO0O000O0O00O0OO0 #line:936
            if (OOOO0O000000OOOO0 .get ('maxlen'),None )==None :#line:937
                print (f"Error: cedent {OOO0000O0000OOO0O} has no maximal length specified.")#line:938
                OO0O000O0O00O0OO0 =False #line:939
                return OO0O000O0O00O0OO0 #line:940
            if not (type (OOOO0O000000OOOO0 .get ('maxlen'))is int ):#line:941
                print (f"Error: cedent {OOO0000O0000OOO0O} has invalid type of maximal length.")#line:942
                OO0O000O0O00O0OO0 =False #line:943
                return OO0O000O0O00O0OO0 #line:944
            if (OOOO0O000000OOOO0 .get ('type'),None )==None :#line:945
                print (f"Error: cedent {OOO0000O0000OOO0O} has no type specified.")#line:946
                OO0O000O0O00O0OO0 =False #line:947
                return OO0O000O0O00O0OO0 #line:948
            if not ((OOOO0O000000OOOO0 .get ('type'))in (['con','dis'])):#line:949
                print (f"Error: cedent {OOO0000O0000OOO0O} has invalid type. Allowed values are 'con' and 'dis'.")#line:950
                OO0O000O0O00O0OO0 =False #line:951
                return OO0O000O0O00O0OO0 #line:952
            if (OOOO0O000000OOOO0 .get ('attributes'),None )==None :#line:953
                print (f"Error: cedent {OOO0000O0000OOO0O} has no attributes specified.")#line:954
                OO0O000O0O00O0OO0 =False #line:955
                return OO0O000O0O00O0OO0 #line:956
            for O0O0O0OO0OO00O0O0 in OOOO0O000000OOOO0 .get ('attributes'):#line:957
                if (O0O0O0OO0OO00O0O0 .get ('name'),None )==None :#line:958
                    print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0} has no 'name' attribute specified.")#line:959
                    OO0O000O0O00O0OO0 =False #line:960
                    return OO0O000O0O00O0OO0 #line:961
                if not ((O0O0O0OO0OO00O0O0 .get ('name'))in OO0OOO00O0OOO0000 .data ["varname"]):#line:962
                    print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} not in variable list. Please check spelling.")#line:963
                    OO0O000O0O00O0OO0 =False #line:964
                    return OO0O000O0O00O0OO0 #line:965
                if (O0O0O0OO0OO00O0O0 .get ('type'),None )==None :#line:966
                    print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} has no 'type' attribute specified.")#line:967
                    OO0O000O0O00O0OO0 =False #line:968
                    return OO0O000O0O00O0OO0 #line:969
                if not ((O0O0O0OO0OO00O0O0 .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:970
                    print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} has unsupported type {O0O0O0OO0OO00O0O0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:971
                    OO0O000O0O00O0OO0 =False #line:972
                    return OO0O000O0O00O0OO0 #line:973
                if (O0O0O0OO0OO00O0O0 .get ('minlen'),None )==None :#line:974
                    print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} has no minimal length specified.")#line:975
                    OO0O000O0O00O0OO0 =False #line:976
                    return OO0O000O0O00O0OO0 #line:977
                if not (type (O0O0O0OO0OO00O0O0 .get ('minlen'))is int ):#line:978
                    if not (O0O0O0OO0OO00O0O0 .get ('type')=='one'):#line:979
                        print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} has invalid type of minimal length.")#line:980
                        OO0O000O0O00O0OO0 =False #line:981
                        return OO0O000O0O00O0OO0 #line:982
                if (O0O0O0OO0OO00O0O0 .get ('maxlen'),None )==None :#line:983
                    print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} has no maximal length specified.")#line:984
                    OO0O000O0O00O0OO0 =False #line:985
                    return OO0O000O0O00O0OO0 #line:986
                if not (type (O0O0O0OO0OO00O0O0 .get ('maxlen'))is int ):#line:987
                    if not (O0O0O0OO0OO00O0O0 .get ('type')=='one'):#line:988
                        print (f"Error: cedent {OOO0000O0000OOO0O} / attribute {O0O0O0OO0OO00O0O0.get('name')} has invalid type of maximal length.")#line:989
                        OO0O000O0O00O0OO0 =False #line:990
                        return OO0O000O0O00O0OO0 #line:991
        return OO0O000O0O00O0OO0 #line:992
    def _calculate (OOO0O00OOOO000000 ,**OOO0OO0OOO00OOO00 ):#line:994
        if OOO0O00OOOO000000 .data ["data_prepared"]==0 :#line:995
            print ("Error: data not prepared")#line:996
            return #line:997
        OOO0O00OOOO000000 .kwargs =OOO0OO0OOO00OOO00 #line:998
        OOO0O00OOOO000000 .proc =OOO0OO0OOO00OOO00 .get ('proc')#line:999
        OOO0O00OOOO000000 .quantifiers =OOO0OO0OOO00OOO00 .get ('quantifiers')#line:1000
        OOO0O00OOOO000000 ._init_task ()#line:1002
        OOO0O00OOOO000000 .stats ['start_proc_time']=time .time ()#line:1003
        OOO0O00OOOO000000 .task_actinfo ['cedents_to_do']=[]#line:1004
        OOO0O00OOOO000000 .task_actinfo ['cedents']=[]#line:1005
        if OOO0OO0OOO00OOO00 .get ("proc")=='CFMiner':#line:1008
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do']=['cond']#line:1009
            if OOO0OO0OOO00OOO00 .get ('target',None )==None :#line:1010
                print ("ERROR: no target variable defined for CF Miner")#line:1011
                return #line:1012
            if not (OOO0O00OOOO000000 ._check_cedents (['cond'],**OOO0OO0OOO00OOO00 )):#line:1013
                return #line:1014
            if not (OOO0OO0OOO00OOO00 .get ('target')in OOO0O00OOOO000000 .data ["varname"]):#line:1015
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1016
                return #line:1017
        elif OOO0OO0OOO00OOO00 .get ("proc")=='4ftMiner':#line:1019
            if not (OOO0O00OOOO000000 ._check_cedents (['ante','succ'],**OOO0OO0OOO00OOO00 )):#line:1020
                return #line:1021
            _O00OOOOOO0000OOO0 =OOO0OO0OOO00OOO00 .get ("cond")#line:1023
            if _O00OOOOOO0000OOO0 !=None :#line:1024
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1025
            else :#line:1026
                O00O0O0OOOOOOO0O0 =OOO0O00OOOO000000 .cedent #line:1027
                O00O0O0OOOOOOO0O0 ['cedent_type']='cond'#line:1028
                O00O0O0OOOOOOO0O0 ['filter_value']=(1 <<OOO0O00OOOO000000 .data ["rows_count"])-1 #line:1029
                O00O0O0OOOOOOO0O0 ['generated_string']='---'#line:1030
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1032
                OOO0O00OOOO000000 .task_actinfo ['cedents'].append (O00O0O0OOOOOOO0O0 )#line:1033
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1037
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1038
        elif OOO0OO0OOO00OOO00 .get ("proc")=='NewAct4ftMiner':#line:1039
            _O00OOOOOO0000OOO0 =OOO0OO0OOO00OOO00 .get ("cond")#line:1042
            if _O00OOOOOO0000OOO0 !=None :#line:1043
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1044
            else :#line:1045
                O00O0O0OOOOOOO0O0 =OOO0O00OOOO000000 .cedent #line:1046
                O00O0O0OOOOOOO0O0 ['cedent_type']='cond'#line:1047
                O00O0O0OOOOOOO0O0 ['filter_value']=(1 <<OOO0O00OOOO000000 .data ["rows_count"])-1 #line:1048
                O00O0O0OOOOOOO0O0 ['generated_string']='---'#line:1049
                print (O00O0O0OOOOOOO0O0 ['filter_value'])#line:1050
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1051
                OOO0O00OOOO000000 .task_actinfo ['cedents'].append (O00O0O0OOOOOOO0O0 )#line:1052
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('antv')#line:1053
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1054
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1055
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1056
        elif OOO0OO0OOO00OOO00 .get ("proc")=='Act4ftMiner':#line:1057
            _O00OOOOOO0000OOO0 =OOO0OO0OOO00OOO00 .get ("cond")#line:1060
            if _O00OOOOOO0000OOO0 !=None :#line:1061
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1062
            else :#line:1063
                O00O0O0OOOOOOO0O0 =OOO0O00OOOO000000 .cedent #line:1064
                O00O0O0OOOOOOO0O0 ['cedent_type']='cond'#line:1065
                O00O0O0OOOOOOO0O0 ['filter_value']=(1 <<OOO0O00OOOO000000 .data ["rows_count"])-1 #line:1066
                O00O0O0OOOOOOO0O0 ['generated_string']='---'#line:1067
                print (O00O0O0OOOOOOO0O0 ['filter_value'])#line:1068
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1069
                OOO0O00OOOO000000 .task_actinfo ['cedents'].append (O00O0O0OOOOOOO0O0 )#line:1070
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1071
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1072
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1073
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1074
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1075
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1076
        elif OOO0OO0OOO00OOO00 .get ("proc")=='SD4ftMiner':#line:1077
            if not (OOO0O00OOOO000000 ._check_cedents (['ante','succ','frst','scnd'],**OOO0OO0OOO00OOO00 )):#line:1080
                return #line:1081
            _O00OOOOOO0000OOO0 =OOO0OO0OOO00OOO00 .get ("cond")#line:1082
            if _O00OOOOOO0000OOO0 !=None :#line:1083
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1084
            else :#line:1085
                O00O0O0OOOOOOO0O0 =OOO0O00OOOO000000 .cedent #line:1086
                O00O0O0OOOOOOO0O0 ['cedent_type']='cond'#line:1087
                O00O0O0OOOOOOO0O0 ['filter_value']=(1 <<OOO0O00OOOO000000 .data ["rows_count"])-1 #line:1088
                O00O0O0OOOOOOO0O0 ['generated_string']='---'#line:1089
                OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1091
                OOO0O00OOOO000000 .task_actinfo ['cedents'].append (O00O0O0OOOOOOO0O0 )#line:1092
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('frst')#line:1093
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1094
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1095
            OOO0O00OOOO000000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1096
        else :#line:1097
            print ("Unsupported procedure")#line:1098
            return #line:1099
        print ("Will go for ",OOO0OO0OOO00OOO00 .get ("proc"))#line:1100
        OOO0O00OOOO000000 .task_actinfo ['optim']={}#line:1103
        OO000OO0OO00O00O0 =True #line:1104
        for O0OOO000O00O0O0O0 in OOO0O00OOOO000000 .task_actinfo ['cedents_to_do']:#line:1105
            try :#line:1106
                O0000OO0O0OO00O00 =OOO0O00OOOO000000 .kwargs .get (O0OOO000O00O0O0O0 )#line:1107
                if O0000OO0O0OO00O00 .get ('type')!='con':#line:1110
                    OO000OO0OO00O00O0 =False #line:1111
            except :#line:1112
                O0O0OOO0O0OOO00O0 =1 <2 #line:1113
        if "opts"in OOO0OO0OOO00OOO00 :#line:1115
            if "no_optimizations"in OOO0OO0OOO00OOO00 .get ('opts'):#line:1116
                OO000OO0OO00O00O0 =False #line:1117
                print ("No optimization will be made.")#line:1118
        O00O0O00O00OOO000 ={}#line:1120
        O00O0O00O00OOO000 ['only_con']=OO000OO0OO00O00O0 #line:1121
        OOO0O00OOOO000000 .task_actinfo ['optim']=O00O0O00O00OOO000 #line:1122
        print ("Starting to mine rules.")#line:1130
        OOO0O00OOOO000000 ._start_cedent (OOO0O00OOOO000000 .task_actinfo )#line:1131
        OOO0O00OOOO000000 .stats ['end_proc_time']=time .time ()#line:1133
        print ("Done. Total verifications : "+str (OOO0O00OOOO000000 .stats ['total_cnt'])+", rules "+str (OOO0O00OOOO000000 .stats ['total_valid'])+",control number:"+str (OOO0O00OOOO000000 .stats ['control_number'])+", times: prep "+str (OOO0O00OOOO000000 .stats ['end_prep_time']-OOO0O00OOOO000000 .stats ['start_prep_time'])+", processing "+str (OOO0O00OOOO000000 .stats ['end_proc_time']-OOO0O00OOOO000000 .stats ['start_proc_time']))#line:1136
        O0OOO00O00OO0O000 ={}#line:1137
        OO0O000O000O0000O ={}#line:1138
        OO0O000O000O0000O ["task_type"]=OOO0OO0OOO00OOO00 .get ('proc')#line:1139
        OO0O000O000O0000O ["target"]=OOO0OO0OOO00OOO00 .get ('target')#line:1141
        OO0O000O000O0000O ["self.quantifiers"]=OOO0O00OOOO000000 .quantifiers #line:1142
        if OOO0OO0OOO00OOO00 .get ('cond')!=None :#line:1144
            OO0O000O000O0000O ['cond']=OOO0OO0OOO00OOO00 .get ('cond')#line:1145
        if OOO0OO0OOO00OOO00 .get ('ante')!=None :#line:1146
            OO0O000O000O0000O ['ante']=OOO0OO0OOO00OOO00 .get ('ante')#line:1147
        if OOO0OO0OOO00OOO00 .get ('succ')!=None :#line:1148
            OO0O000O000O0000O ['succ']=OOO0OO0OOO00OOO00 .get ('succ')#line:1149
        if OOO0OO0OOO00OOO00 .get ('opts')!=None :#line:1150
            OO0O000O000O0000O ['opts']=OOO0OO0OOO00OOO00 .get ('opts')#line:1151
        O0OOO00O00OO0O000 ["taskinfo"]=OO0O000O000O0000O #line:1152
        O0O000OO0O0OOO0OO ={}#line:1153
        O0O000OO0O0OOO0OO ["total_verifications"]=OOO0O00OOOO000000 .stats ['total_cnt']#line:1154
        O0O000OO0O0OOO0OO ["valid_rules"]=OOO0O00OOOO000000 .stats ['total_valid']#line:1155
        O0O000OO0O0OOO0OO ["time_prep"]=OOO0O00OOOO000000 .stats ['end_prep_time']-OOO0O00OOOO000000 .stats ['start_prep_time']#line:1156
        O0O000OO0O0OOO0OO ["time_processing"]=OOO0O00OOOO000000 .stats ['end_proc_time']-OOO0O00OOOO000000 .stats ['start_proc_time']#line:1157
        O0O000OO0O0OOO0OO ["time_total"]=OOO0O00OOOO000000 .stats ['end_prep_time']-OOO0O00OOOO000000 .stats ['start_prep_time']+OOO0O00OOOO000000 .stats ['end_proc_time']-OOO0O00OOOO000000 .stats ['start_proc_time']#line:1158
        O0OOO00O00OO0O000 ["summary_statistics"]=O0O000OO0O0OOO0OO #line:1159
        O0OOO00O00OO0O000 ["rules"]=OOO0O00OOOO000000 .rulelist #line:1160
        O0O000OO0OO00O0O0 ={}#line:1161
        O0O000OO0OO00O0O0 ["varname"]=OOO0O00OOOO000000 .data ["varname"]#line:1162
        O0O000OO0OO00O0O0 ["catnames"]=OOO0O00OOOO000000 .data ["catnames"]#line:1163
        O0OOO00O00OO0O000 ["datalabels"]=O0O000OO0OO00O0O0 #line:1164
        OOO0O00OOOO000000 .result =O0OOO00O00OO0O000 #line:1167
    def print_summary (OO0O0O0O00OOOOOO0 ):#line:1169
        print ("")#line:1170
        print ("CleverMiner task processing summary:")#line:1171
        print ("")#line:1172
        print (f"Task type : {OO0O0O0O00OOOOOO0.result['taskinfo']['task_type']}")#line:1173
        print (f"Number of verifications : {OO0O0O0O00OOOOOO0.result['summary_statistics']['total_verifications']}")#line:1174
        print (f"Number of rules : {OO0O0O0O00OOOOOO0.result['summary_statistics']['valid_rules']}")#line:1175
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(OO0O0O0O00OOOOOO0.result['summary_statistics']['time_total']))}")#line:1176
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(OO0O0O0O00OOOOOO0.result['summary_statistics']['time_prep']))}")#line:1178
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(OO0O0O0O00OOOOOO0.result['summary_statistics']['time_processing']))}")#line:1179
        print ("")#line:1180
    def print_hypolist (O00OOOOO0O0O0OO00 ):#line:1182
        O00OOOOO0O0O0OO00 .print_rulelist ();#line:1183
    def print_rulelist (O0O0O0OO0OO00OO00 ):#line:1185
        print ("")#line:1187
        print ("List of rules:")#line:1188
        if O0O0O0OO0OO00OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1189
            print ("RULEID BASE  CONF  AAD    Rule")#line:1190
        elif O0O0O0OO0OO00OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1191
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1192
        elif O0O0O0OO0OO00OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1193
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1194
        else :#line:1195
            print ("Unsupported task type for rulelist")#line:1196
            return #line:1197
        for O000O0000O0OOO0O0 in O0O0O0OO0OO00OO00 .result ["rules"]:#line:1198
            OO0O0O0O00OOOOO0O ="{:6d}".format (O000O0000O0OOO0O0 ["rule_id"])#line:1199
            if O0O0O0OO0OO00OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1200
                OO0O0O0O00OOOOO0O =OO0O0O0O00OOOOO0O +" "+"{:5d}".format (O000O0000O0OOO0O0 ["params"]["base"])+" "+"{:.3f}".format (O000O0000O0OOO0O0 ["params"]["conf"])+" "+"{:+.3f}".format (O000O0000O0OOO0O0 ["params"]["aad"])#line:1201
                OO0O0O0O00OOOOO0O =OO0O0O0O00OOOOO0O +" "+O000O0000O0OOO0O0 ["cedents"]["ante"]+" => "+O000O0000O0OOO0O0 ["cedents"]["succ"]+" | "+O000O0000O0OOO0O0 ["cedents"]["cond"]#line:1202
            elif O0O0O0OO0OO00OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1203
                OO0O0O0O00OOOOO0O =OO0O0O0O00OOOOO0O +" "+"{:5d}".format (O000O0000O0OOO0O0 ["params"]["base"])+" "+"{:5d}".format (O000O0000O0OOO0O0 ["params"]["s_up"])+" "+"{:5d}".format (O000O0000O0OOO0O0 ["params"]["s_down"])#line:1204
                OO0O0O0O00OOOOO0O =OO0O0O0O00OOOOO0O +" "+O000O0000O0OOO0O0 ["cedents"]["cond"]#line:1205
            elif O0O0O0OO0OO00OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1206
                OO0O0O0O00OOOOO0O =OO0O0O0O00OOOOO0O +" "+"{:5d}".format (O000O0000O0OOO0O0 ["params"]["base1"])+" "+"{:5d}".format (O000O0000O0OOO0O0 ["params"]["base2"])+"    "+"{:.3f}".format (O000O0000O0OOO0O0 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O000O0000O0OOO0O0 ["params"]["deltaconf"])#line:1207
                OO0O0O0O00OOOOO0O =OO0O0O0O00OOOOO0O +"  "+O000O0000O0OOO0O0 ["cedents"]["ante"]+" => "+O000O0000O0OOO0O0 ["cedents"]["succ"]+" | "+O000O0000O0OOO0O0 ["cedents"]["cond"]+" : "+O000O0000O0OOO0O0 ["cedents"]["frst"]+" x "+O000O0000O0OOO0O0 ["cedents"]["scnd"]#line:1208
            print (OO0O0O0O00OOOOO0O )#line:1210
        print ("")#line:1211
    def print_hypo (OOOOOOO0OO0O00OOO ,O00OO000OO0O000O0 ):#line:1213
        OOOOOOO0OO0O00OOO .print_rule (O00OO000OO0O000O0 )#line:1214
    def print_rule (O0O0O0O0OOOO0OOOO ,O000O00000O0O00O0 ):#line:1217
        print ("")#line:1218
        if (O000O00000O0O00O0 <=len (O0O0O0O0OOOO0OOOO .result ["rules"])):#line:1219
            if O0O0O0O0OOOO0OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1220
                print ("")#line:1221
                O000O0OO000OOOO0O =O0O0O0O0OOOO0OOOO .result ["rules"][O000O00000O0O00O0 -1 ]#line:1222
                print (f"Rule id : {O000O0OO000OOOO0O['rule_id']}")#line:1223
                print ("")#line:1224
                print (f"Base : {'{:5d}'.format(O000O0OO000OOOO0O['params']['base'])}  Relative base : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['rel_base'])}  CONF : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['conf'])}  AAD : {'{:+.3f}'.format(O000O0OO000OOOO0O['params']['aad'])}  BAD : {'{:+.3f}'.format(O000O0OO000OOOO0O['params']['bad'])}")#line:1225
                print ("")#line:1226
                print ("Cedents:")#line:1227
                print (f"  antecedent : {O000O0OO000OOOO0O['cedents']['ante']}")#line:1228
                print (f"  succcedent : {O000O0OO000OOOO0O['cedents']['succ']}")#line:1229
                print (f"  condition  : {O000O0OO000OOOO0O['cedents']['cond']}")#line:1230
                print ("")#line:1231
                print ("Fourfold table")#line:1232
                print (f"    |  S  |  ¬S |")#line:1233
                print (f"----|-----|-----|")#line:1234
                print (f" A  |{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold'][0])}|{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold'][1])}|")#line:1235
                print (f"----|-----|-----|")#line:1236
                print (f"¬A  |{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold'][2])}|{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold'][3])}|")#line:1237
                print (f"----|-----|-----|")#line:1238
            elif O0O0O0O0OOOO0OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1239
                print ("")#line:1240
                O000O0OO000OOOO0O =O0O0O0O0OOOO0OOOO .result ["rules"][O000O00000O0O00O0 -1 ]#line:1241
                print (f"Rule id : {O000O0OO000OOOO0O['rule_id']}")#line:1242
                print ("")#line:1243
                print (f"Base : {'{:5d}'.format(O000O0OO000OOOO0O['params']['base'])}  Relative base : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O000O0OO000OOOO0O['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O000O0OO000OOOO0O['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O000O0OO000OOOO0O['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O000O0OO000OOOO0O['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O000O0OO000OOOO0O['params']['max'])}  Histogram minimum : {'{:5d}'.format(O000O0OO000OOOO0O['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['rel_min'])}")#line:1245
                print ("")#line:1246
                print (f"Condition  : {O000O0OO000OOOO0O['cedents']['cond']}")#line:1247
                print ("")#line:1248
                print (f"Histogram {O000O0OO000OOOO0O['params']['hist']}")#line:1249
            elif O0O0O0O0OOOO0OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1250
                print ("")#line:1251
                O000O0OO000OOOO0O =O0O0O0O0OOOO0OOOO .result ["rules"][O000O00000O0O00O0 -1 ]#line:1252
                print (f"Rule id : {O000O0OO000OOOO0O['rule_id']}")#line:1253
                print ("")#line:1254
                print (f"Base1 : {'{:5d}'.format(O000O0OO000OOOO0O['params']['base1'])} Base2 : {'{:5d}'.format(O000O0OO000OOOO0O['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O000O0OO000OOOO0O['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O000O0OO000OOOO0O['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O000O0OO000OOOO0O['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O000O0OO000OOOO0O['params']['ratioconf'])}")#line:1255
                print ("")#line:1256
                print ("Cedents:")#line:1257
                print (f"  antecedent : {O000O0OO000OOOO0O['cedents']['ante']}")#line:1258
                print (f"  succcedent : {O000O0OO000OOOO0O['cedents']['succ']}")#line:1259
                print (f"  condition  : {O000O0OO000OOOO0O['cedents']['cond']}")#line:1260
                print (f"  first set  : {O000O0OO000OOOO0O['cedents']['frst']}")#line:1261
                print (f"  second set : {O000O0OO000OOOO0O['cedents']['scnd']}")#line:1262
                print ("")#line:1263
                print ("Fourfold tables:")#line:1264
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1265
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1266
                print (f" A  |{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold1'][0])}|{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold2'][0])}|{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold2'][1])}|")#line:1267
                print (f"----|-----|-----|  ----|-----|-----|")#line:1268
                print (f"¬A  |{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold1'][2])}|{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold2'][2])}|{'{:5d}'.format(O000O0OO000OOOO0O['params']['fourfold2'][3])}|")#line:1269
                print (f"----|-----|-----|  ----|-----|-----|")#line:1270
            else :#line:1271
                print ("Unsupported task type for rule details")#line:1272
            print ("")#line:1276
        else :#line:1277
            print ("No such rule.")#line:1278
