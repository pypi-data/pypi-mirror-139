"""NIKL Annotated Corpus Tagsets
"""
#
# written by Haseon
#
# part-of-speech tagset
POS_TAGS = {
    'NNG' : {'cat1' : '체언', 'cat2' : '명사', 'cat3' : '일반명사'},
    'NNP' : {'cat1' : '체언', 'cat2' : '명사', 'cat3' : '고유명사'},
    'NNB' : {'cat1' : '체언', 'cat2' : '명사', 'cat3' : '의존명사'},
    'NP' : {'cat1' : '체언', 'cat2' : '대명사', 'cat3' : '대명사'},
    'NR' : {'cat1' : '체언', 'cat2' : '수사', 'cat3' : '수사'},
    'VV' : {'cat1' : '용언', 'cat2' : '동사', 'cat3' : '동사'},
    'VA' : {'cat1' : '용언', 'cat2' : '형용사', 'cat3' : '형용사'},
    'VX' : {'cat1' : '용언', 'cat2' : '보조용언', 'cat3' : '보조용언'},
    'VCP' : {'cat1' : '용언', 'cat2' : '지정사', 'cat3' : '긍정지정사'},
    'VCN' : {'cat1' : '용언', 'cat2' : '지정사', 'cat3' : '부정지정사'},
    'MMA' : {'cat1' : '수식언', 'cat2' : '관형사', 'cat3' : '성상 관형사'},
    'MMD' : {'cat1' : '수식언', 'cat2' : '관형사', 'cat3' : '지시 관형사'},
    'MMN' : {'cat1' : '수식언', 'cat2' : '관형사', 'cat3' : '수 관형사'},
    'MAG' : {'cat1' : '수식언', 'cat2' : '부사', 'cat3' : '일반부사'},
    'MAJ' : {'cat1' : '수식언', 'cat2' : '부사', 'cat3' : '접속부사'},
    'IC' : {'cat1' : '독립언', 'cat2' : '감탄사', 'cat3' : '감탄사'},
    'JKS' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '주격조사'},
    'JKC' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '보격조사'},
    'JKG' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '관형격격조사'},
    'JKO' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '목적격조사'},
    'JKB' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '부사격조사'},
    'JKV' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '호격조사'},
    'JKQ' : {'cat1' : '관계언', 'cat2' : '격조사', 'cat3' : '인용격조사'},
    'JX' : {'cat1' : '관계언', 'cat2' : '보조사', 'cat3' : '보조사'},
    'JC' : {'cat1' : '관계언', 'cat2' : '접속조사', 'cat3' : '접속조사'},
    'EP' : {'cat1' : '의존형태', 'cat2' : '어미', 'cat3' : '선어말어미'},
    'EF' : {'cat1' : '의존형태', 'cat2' : '어미', 'cat3' : '종결어미'},
    'EC' : {'cat1' : '의존형태', 'cat2' : '어미', 'cat3' : '연결어미'},
    'ETN' : {'cat1' : '의존형태', 'cat2' : '어미', 'cat3' : '명사형전성어미'},
    'ETM' : {'cat1' : '의존형태', 'cat2' : '어미', 'cat3' : '관형형전성어미'},
    'XPN' : {'cat1' : '의존형태', 'cat2' : '접두사', 'cat3' : '체언접두사'},
    'XSN' : {'cat1' : '의존형태', 'cat2' : '접미사', 'cat3' : '명사파생접미사'},
    'XSV' : {'cat1' : '의존형태', 'cat2' : '접미사', 'cat3' : '동사파생접미사'},
    'XSA' : {'cat1' : '의존형태', 'cat2' : '접미사', 'cat3' : '형용사파생접미사'},
    'XR' : {'cat1' : '의존형태', 'cat2' : '어근', 'cat3' : '어근'},
    'SF' : {'cat1' : '기호', 'cat2' : '일반기호', 'cat3' : '마침표, 물음표, 느낌표'},
    'SP' : {'cat1' : '기호', 'cat2' : '일반기호', 'cat3' : '쉼표, 가운뎃점, 콜론, 빗금'},
    'SS' : {'cat1' : '기호', 'cat2' : '일반기호', 'cat3' : '따옴표, 괄호표, 줄표'},
    'SE' : {'cat1' : '기호', 'cat2' : '일반기호', 'cat3' : '줄임표'},
    'SO' : {'cat1' : '기호', 'cat2' : '일반기호', 'cat3' : '붙임표(물결)'},
    'SW' : {'cat1' : '기호', 'cat2' : '일반기호', 'cat3' : '기타 기호'},
    'SL' : {'cat1' : '기호', 'cat2' : '외국어', 'cat3' : '외국어'},
    'SH' : {'cat1' : '기호', 'cat2' : '한자', 'cat3' : '한자'},
    'SN' : {'cat1' : '기호', 'cat2' : '숫자', 'cat3' : '숫자'},
    'NA' : {'cat1' : '기호', 'cat2' : '분석불능범주', 'cat3' : '분석불능범주'},
    'NF' : {'cat1' : '기호', 'cat2' : '분석불능범주', 'cat3' : '명사추정범주'},
    'NV' : {'cat1' : '기호', 'cat2' : '분석불능범주', 'cat3' : '용언추정범주'},
    'NAP' : {'cat1' : '체언', 'cat2' : '명사', 'cat3' : '비식별화 대상'}
}


#
# written by Haseon
#
# named entity tagset
NE_TAGS = {
    'PS' : {'cat1' : 'PERSON', 'cat2' : '인명'},
    'FD' : {'cat1' : 'STUDY_FIELD', 'cat2' : '학문분야 및 학파'},
    'TR' : {'cat1' : 'THEORY', 'cat2' : '이론'},
    'AF' : {'cat1' : 'ARTIFACTS', 'cat2' : '인공물'},
    'OG' : {'cat1' : 'ORGANIZATION', 'cat2' : '기관 및 조직'},
    'LC' : {'cat1' : 'LOCATION', 'cat2' : '지명'},
    'CV' : {'cat1' : 'CIVILIZATION', 'cat2' : '문명'},
    'DT' : {'cat1' : 'DATE', 'cat2' : '날짜'},
    'TI' : {'cat1' : 'TIME', 'cat2' : '시간'},
    'QT' : {'cat1' : 'QUANTITY', 'cat2' : '수량'},
    'EV' : {'cat1' : 'EVENT', 'cat2' : '사건 및 사고'},
    'AM' : {'cat1' : 'ANIMAL', 'cat2' : '동물'},
    'PT' : {'cat1' : 'PLANT', 'cat2' : '식물'},
    'MT' : {'cat1' : 'MATERIAL', 'cat2' : '물질'},
    'TM' : {'cat1' : 'TERM', 'cat2' : '기타 용어'}
}




#
# written by Gyuhwan Lee
#
# syntatic tagset
SYN_TAGS = {
    'NP' : {'cat1' : 'NOUN_PHRASE', 'cat2' : '체언'},
    'VP' : {'cat1' : 'VERB_PHRASE', 'cat2' : '용언'},
    'VNP' : {'cat1' : 'VERBAL_NOUN_PHRASE', 'cat2' : '긍정지정사구'},
    'AP' : {'cat1' : 'ADVERBIAL_PHRASE', 'cat2' : '부사구'},
    'DP' : {'cat1' : 'DETERMINER_PHRASE', 'cat2' : '관형사구'},
    'IP' : {'cat1' : 'INTERJECTION_PHRASE', 'cat2' : '감탄사구'},
    'X' : {'cat1' : 'PSEUDO_PHRASE', 'cat2' : '의사구'},
    'L' : {'cat1' : 'LEFT_SYMBOL', 'cat2' : '왼쪽 부호'},
    'R' : {'cat1' : 'RIGHT_SYMBOL', 'cat2' : '오른쪽 부호'}    
}

#
# function tagset
#
FUN_TAGS = {
    'SBJ' : {'cat1' : 'SUBJECT', 'cat2' : '주어'},
    'OBJ' : {'cat1' : 'OBJECT', 'cat2' : '목적어'},
    'CMP' : {'cat1' : 'COMPLEMENT', 'cat2' : '보어'},
    'MOD' : {'cat1' : 'MODIFIER', 'cat2' : '체언수식어(관형어)'},
    'AJT' : {'cat1' : 'ADJUNCT', 'cat2' : '용언수식어(부사어)'},
    'CNJ' : {'cat1' : 'CONJUNCTION', 'cat2' : '접속어'},
    'INT' : {'cat1' : 'INDEPENDENT', 'cat2' : '독립어'}    
}


#
# written by Gyuhwan Lee
#
# semantic role tagset
SR_TAGS = {
    'ARG0' : {},
    'ARG1' : {},
    'ARG2' : {},
    'ARG3' : {},
    'ARGA' : {},
    'ARGM-LOC' : {},
    'ARGM-DIR' : {},
    'ARGM-CND' : {},
    'ARGM-MNR' : {},
    'ARGM-TMP' : {},
    'ARGM-EXT' : {},
    'ARGM-PRD' : {},
    'ARGM-PRP' : {},
    'ARGM-CAU' : {},
    'ARGM-DIS' : {},
    'ARGM-ADV' : {},
    'ARGM-NEG' : {},
    'ARGM-INS' : {},
    'AUX' : {}
}

