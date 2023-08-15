# Copyright (c) 2022 Darren Erik Vengroff

"""
This module contains abbreviated names for commonly used data sets.

These are typically used as the first argument to :py:func:`censudis.data.download`.

There are a lot more data sets available than there are symbolic names here.
But you can always use raw strings. For example, even for `ACS5` you can use
`"acs/acs5"` instead.
"""

# Many more can be added here. We should do a pass of all the demo
# notebooks and put in names for all the data sets we us.

import censusdis.data as ced
import censusdis.symbolic as sym

df_datasets = ced.variables.all_data_sets()
dataset_names = df_datasets["DATASET"].to_list()
dataset_url = df_datasets["API BASE URL"].to_list()
create_symbolic = sym.symbolic()
symbolic_names = create_symbolic.store_dataset(dataset_names, dataset_url)
create_symbolic.write_file("datasets.py")

ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DECENNIAL_AIAN = "dec/aian"

DECENNIAL_AIAN_PROFILE = "dec/aianprofile"

DECENNIAL_AS = "dec/as"

DECENNIAL_AS_YEAR_OF_ENTRY = "dec/asyoe"

DECENNIAL_CD_110H = "dec/cd110h"

DECENNIAL_CD_110H_PROFILE = "dec/cd110hprofile"

DECENNIAL_CD_110H_SAMPLE = "dec/cd110s"

DECENNIAL_CD_110H_PROFILE_SAMPLE = "dec/cd110sprofile"

DECENNIAL_CD_113 = "dec/cd113"

DECENNIAL_CD_113_PROFILE = "dec/cd113profile"

DECENNIAL_CD_115 = "dec/cd115"

DECENNIAL_CD_115_PROFILE = "dec/cd115profile"

DECENNIAL_CD_116 = "dec/cd116"

DECENNIAL_COUNT_QUESTION_RESOLUTION = "dec/cqr"

DECENNIAL_DHC = "dec/dhc"

DECENNIAL_DHC_AS = "dec/dhcas"

DECENNIAL_DHC_GU = "dec/dhcgu"

DECENNIAL_DHC_MP = "dec/dhcmp"

DECENNIAL_DHC_VI = "dec/dhcvi"

DECENNIAL_DP = "dec/dp"

DECENNIAL_DP_AS = "dec/dpas"

DECENNIAL_DP_GU = "dec/dpgu"

DECENNIAL_DP_MP = "dec/dpmp"

DECENNIAL_DP_VI = "dec/dpvi"

DECENNIAL_GU = "dec/gu"

DECENNIAL_GU_YEAR_OF_ENTRY = "dec/guyoe"

DECENNIAL_MP = "dec/mp"

DECENNIAL_MP_YEAR_OF_ENTRY = "dec/mpyoe"

DECENNIAL_POST_ENUMERATION_SURVEY = "dec/pes"

DECENNIAL_PUBLIC_LAW_94_171 = "dec/pl"

DECENNIAL_PUBLIC_LAW_NAT = "dec/plnat"

DECENNIAL_RESPONSE_RATE = "dec/responserate"

DECENNIAL_SF1 = "dec/sf1"

DECENNIAL_SF2 = "dec/sf2"

DECENNIAL_SF2_PROFILE = "dec/sf2profile"

DECENNIAL_SF3 = "dec/sf3"

DECENNIAL_SF3_PROFILE = "dec/sf3profile"

DECENNIAL_SF4 = "dec/sf4"

DECENNIAL_SF4_PROFILE = "dec/sf4profile"

DECENNIAL_SLDH = "dec/sldh"

DECENNIAL_SLDH_PROFILE = "dec/sldhprofile"

DECENNIAL_SLD_SAMPLE = "dec/slds"

DECENNIAL_SLD_PROFILE_SAMPLE = "dec/sldsprofile"

DECENNIAL_SURNAME = "surname"

DECENNIAL_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBLIC_PK12_EDUCATION_FINANCE = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "https://www.census.gov/data/developers/data-sets/acs-5year.html",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DECENNIAL_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DECENNIAL_AIAN_PROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DECENNIAL_AS: "http://api.census.gov/data/2000/dec/as",
    DECENNIAL_AS_YEAR_OF_ENTRY: "http://api.census.gov/data/2010/dec/asyoe",
    DECENNIAL_CD_110H: "http://api.census.gov/data/2000/dec/cd110h",
    DECENNIAL_CD_110H_PROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DECENNIAL_CD_110H_SAMPLE: "http://api.census.gov/data/2000/dec/cd110s",
    DECENNIAL_CD_110H_PROFILE_SAMPLE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DECENNIAL_CD_113: "http://api.census.gov/data/2010/dec/cd113",
    DECENNIAL_CD_113_PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DECENNIAL_CD_115: "http://api.census.gov/data/2010/dec/cd115",
    DECENNIAL_CD_115_PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DECENNIAL_CD_116: "http://api.census.gov/data/2010/dec/cd116",
    DECENNIAL_COUNT_QUESTION_RESOLUTION: "http://api.census.gov/data/2000/dec/cqr",
    DECENNIAL_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DECENNIAL_DHC_AS: "http://api.census.gov/data/2020/dec/dhcas",
    DECENNIAL_DHC_GU: "http://api.census.gov/data/2020/dec/dhcgu",
    DECENNIAL_DHC_MP: "http://api.census.gov/data/2020/dec/dhcmp",
    DECENNIAL_DHC_VI: "http://api.census.gov/data/2020/dec/dhcvi",
    DECENNIAL_DP: "http://api.census.gov/data/2020/dec/dp",
    DECENNIAL_DP_AS: "http://api.census.gov/data/2020/dec/dpas",
    DECENNIAL_DP_GU: "http://api.census.gov/data/2020/dec/dpgu",
    DECENNIAL_DP_MP: "http://api.census.gov/data/2020/dec/dpmp",
    DECENNIAL_DP_VI: "http://api.census.gov/data/2020/dec/dpvi",
    DECENNIAL_GU: "http://api.census.gov/data/2000/dec/gu",
    DECENNIAL_GU_YEAR_OF_ENTRY: "http://api.census.gov/data/2010/dec/guyoe",
    DECENNIAL_MP: "http://api.census.gov/data/2000/dec/mp",
    DECENNIAL_MP_YEAR_OF_ENTRY: "http://api.census.gov/data/2010/dec/mpyoe",
    DECENNIAL_POST_ENUMERATION_SURVEY: "http://api.census.gov/data/2020/dec/pes",
    DECENNIAL_PUBLIC_LAW_94_171: "https://www.census.gov/programs-surveys/decennial-census/data/datasets.html",
    DECENNIAL_PUBLIC_LAW_NAT: "http://api.census.gov/data/2010/dec/plnat",
    DECENNIAL_RESPONSE_RATE: "http://api.census.gov/data/2010/dec/responserate",
    DECENNIAL_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DECENNIAL_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DECENNIAL_SF2_PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DECENNIAL_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DECENNIAL_SF3_PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DECENNIAL_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DECENNIAL_SF4_PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DECENNIAL_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DECENNIAL_SLDH_PROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DECENNIAL_SLD_SAMPLE: "http://api.census.gov/data/2000/dec/slds",
    DECENNIAL_SLD_PROFILE_SAMPLE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DECENNIAL_SURNAME: "http://api.census.gov/data/2000/surname",
    DECENNIAL_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBLIC_PK12_EDUCATION_FINANCE: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}
"""A set of useful documentation links for data sets."""

ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}


ABS_CB = "abscb"

ABS_CBO = "abscbo"

ABS_CS = "abscs"

ABS_MCB = "absmcb"

ABS_NESD = "absnesd"

ABS_NESDO = "absnesdo"

ABS_TCB = "abstcb"

ACS1 = "acs/acs1"

ACS1_CD113 = "acs1/cd113"

ACS1_CD115 = "acs1/cd115"

ACS1_CPROFILE = "acs/acs1/cprofile"

ACS1_PROFILE = "acs/acs1/profile"

ACS1_PUMS = "acs/acs1/pums"

ACS1_PUMSPR = "acs/acs1/pumspr"

ACS1_SPP = "acs/acs1/spp"

ACS1_SUBJECT = "acs/acs1/subject"

ACS3 = "acs/acs3"

ACS3_CPROFILE = "acs/acs3/cprofile"

ACS3_PROFILE = "acs/acs3/profile"

ACS3_SPP = "acs/acs3/spp"

ACS3_SUBJECT = "acs/acs3/subject"

ACS5 = "acs/acs5"

ACS5_AIAN = "acs/acs5/aian"

ACS5_AIANPROFILE = "acs/acs5/aianprofile"

ACS5_CPROFILE = "acs/acs5/cprofile"

ACS5_EEO = "acs/acs5/eeo"

ACS5_PROFILE = "acs/acs5/profile"

ACS5_PUMS = "acs/acs5/pums"

ACS5_PUMSPR = "acs/acs5/pumspr"

ACS5_SPT = "acs/acs5/spt"

ACS5_SPTPROFILE = "acs/acs5/sptprofile"

ACS5_SUBJECT = "acs/acs5/subject"

ACSSE = "acs/acsse"

ACS_FLOWS = "acs/flows"

ASE_CSA = "ase/csa"

ASE_CSCB = "ase/cscb"

ASE_CSCBO = "ase/cscbo"

CBP = "cbp"

CFSAREA = "cfsarea"

CFSEXPORT = "cfsexport"

CFSHAZMAT = "cfshazmat"

CFSPRELIM = "cfsprelim"

CFSTEMP = "cfstemp"

CPS_ARTS = "cps/arts/feb"

CPS_ASEC = "cps/asec/mar"

CPS_BASIC = "cps/basic/may"

CPS_CIVIC = "cps/civic/nov"

CPS_CONTWORKER = "cps/contworker/may"

CPS_DISABILITY = "cps/disability/jul"

CPS_DWJT = "cps/dwjt/jan"

CPS_FERTILITY = "cps/fertility/jun"

CPS_FOODSEC = "cps/foodsec/dec"

CPS_IMMIGRATION = "cps/immigration/aug"

CPS_INTERNET = "cps/internet/nov"

CPS_LIBRARY = "cps/library/oct"

CPS_MARITAL = "cps/marital/jun"

CPS_PUBARTS = "cps/pubarts/jul"

CPS_RACE = "cps/race/may"

CPS_SCHOOL = "cps/school/oct"

CPS_TOBACCO = "cps/tobacco/may"

CPS_UNBANK = "cps/unbank/jun"

CPS_VETS = "cps/vets/aug"

CPS_VOLUNTEER = "cps/volunteer/sep"

CPS_VOTING = "cps/voting/nov"

CPS_WORKSCHED = "cps/worksched/may"

CRE = "cre"

DEC_AIAN = "dec/aian"

DEC_AIANPROFILE = "dec/aianprofile"

DEC_AS = "dec/as"

DEC_ASYOE = "dec/asyoe"

DEC_CD110H = "dec/cd110h"

DEC_CD110HPROFILE = "dec/cd110hprofile"

DEC_CD110S = "dec/cd110s"

DEC_CD110SPROFILE = "dec/cd110sprofile"

DEC_CD113 = "dec/cd113"

DEC_CD113PROFILE = "dec/cd113profile"

DEC_CD115 = "dec/cd115"

DEC_CD115PROFILE = "dec/cd115profile"

DEC_CD116 = "dec/cd116"

DEC_CQR = "dec/cqr"

DEC_DHC = "dec/dhc"

DEC_DHCAS = "dec/dhcas"

DEC_DHCGU = "dec/dhcgu"

DEC_DHCMP = "dec/dhcmp"

DEC_DHCVI = "dec/dhcvi"

DEC_DP = "dec/dp"

DEC_DPAS = "dec/dpas"

DEC_DPGU = "dec/dpgu"

DEC_DPMP = "dec/dpmp"

DEC_DPVI = "dec/dpvi"

DEC_GU = "dec/gu"

DEC_GUYOE = "dec/guyoe"

DEC_MP = "dec/mp"

DEC_MPYOE = "dec/mpyoe"

DEC_PES = "dec/pes"

DEC_PL = "dec/pl"

DEC_PLNAT = "dec/plnat"

DEC_RESPONSERATE = "dec/responserate"

DEC_SF1 = "dec/sf1"

DEC_SF2 = "dec/sf2"

DEC_SF2PROFILE = "dec/sf2profile"

DEC_SF3 = "dec/sf3"

DEC_SF3PROFILE = "dec/sf3profile"

DEC_SF4 = "dec/sf4"

DEC_SF4PROFILE = "dec/sf4profile"

DEC_SLDH = "dec/sldh"

DEC_SLDHPROFILE = "dec/sldhprofile"

DEC_SLDS = "dec/slds"

DEC_SLDSPROFILE = "dec/sldsprofile"

DEC_VI = "dec/vi"

ECN_ADBNPROP = "ecnadbnprop"

ECN_ADMBEN = "ecnadmben"

ECN_BASIC = "ecnbasic"

ECN_BRANDDEAL = "ecnbranddeal"

ECN_BRIDGE1 = "ecnbridge1"

ECN_BRIDGE2 = "ecnbridge2"

ECN_BRORDEAL = "ecnbrordeal"

ECN_CASHADV = "ecncashadv"

ECN_CCARD = "ecnccard"

ECN_CLCUST = "ecnclcust"

ECN_COMM = "ecncomm"

ECN_COMP = "ecncomp"

ECN_CONACT = "ecnconact"

ECN_CONCESS = "ecnconcess"

ECN_CRFIN = "ecncrfin"

ECN_DIRPREM = "ecndirprem"

ECN_DISSMED = "ecndissmed"

ECN_ELMENU = "ecnelmenu"

ECN_EMPFUNC = "ecnempfunc"

ECN_ENTSUP = "ecnentsup"

ECN_EOYINV = "ecneoyinv"

ECN_EOYINVWH = "ecneoyinvwh"

ECN_EQUIP = "ecnequip"

ECN_EXPNRG = "ecnexpnrg"

ECN_EXPSVC = "ecnexpsvc"

ECN_FLSPACE = "ecnflspace"

ECN_FOODSVC = "ecnfoodsvc"

ECN_FRAN = "ecnfran"

ECN_GRANT = "ecngrant"

ECN_GUEST = "ecnguest"

ECN_GUESTSIZE = "ecnguestsize"

ECN_HOSP = "ecnhosp"

ECN_HOTEL = "ecnhotel"

ECN_INSTR = "ecninstr"

ECN_INVVAL = "ecninvval"

ECN_IPA = "ecnipa"

ECN_ISLANDAREAS = "ecn/islandareas/napcs"

ECN_KOB = "ecnkob"

ECN_LABOR = "ecnlabor"

ECN_LIFOMFG = "ecnlifomfg"

ECN_LIFOMINE = "ecnlifomine"

ECN_LIFOVAL = "ecnlifoval"

ECN_LINES = "ecnlines"

ECN_LOAN = "ecnloan"

ECN_LOCCONS = "ecnloccons"

ECN_LOCMFG = "ecnlocmfg"

ECN_LOCMINE = "ecnlocmine"

ECN_MARGIN = "ecnmargin"

ECN_MATFUEL = "ecnmatfuel"

ECN_MEALCOST = "ecnmealcost"

ECN_MENUTYPE = "ecnmenutype"

ECN_NAPCSIND = "ecnnapcsind"

ECN_NAPCSPRD = "ecnnapcsprd"

ECN_PATIENT = "ecnpatient"

ECN_PETRFAC = "ecnpetrfac"

ECN_PETRPROD = "ecnpetrprod"

ECN_PETRREC = "ecnpetrrec"

ECN_PETRSTAT = "ecnpetrstat"

ECN_PROFIT = "ecnprofit"

ECN_PURELEC = "ecnpurelec"

ECN_PURGAS = "ecnpurgas"

ECN_PURMODE = "ecnpurmode"

ECN_RDACQ = "ecnrdacq"

ECN_RDOFC = "ecnrdofc"

ECN_SEAT = "ecnseat"

ECN_SIZE = "ecnsize"

ECN_SOCIAL = "ecnsocial"

ECN_TYPE = "ecntype"

ECN_TYPEPAYER = "ecntypepayer"

ECN_TYPOP = "ecntypop"

ECN_VALCON = "ecnvalcon"

EWKS = "ewks"

INTLTRADE_IMP_EXP = "intltrade/imp_exp"

LANGUAGE = "language"

NONEMP = "nonemp"

PDB_BLOCKGROUP = "pdb/blockgroup"

PDB_STATECOUNTY = "pdb/statecounty"

PDB_TRACT = "pdb/tract"

PEP_AGESEX = "pep/agesex"

PEP_AGESPECIAL5 = "pep/agespecial5"

PEP_AGESPECIAL6 = "pep/agespecial6"

PEP_AGESPECIALPR = "pep/agespecialpr"

PEP_CHARAGE = "pep/charage"

PEP_CHARAGEGROUPS = "pep/charagegroups"

PEP_COCHAR5 = "pep/cochar5"

PEP_COCHAR6 = "pep/cochar6"

PEP_COMPONENTS = "pep/components"

PEP_CTY = "pep/cty"

PEP_HOUSING = "pep/housing"

PEP_INT_CHARAGE = "pep/int_charage"

PEP_INT_CHARAGEGROUPS = "pep/int_charagegroups"

PEP_INT_HOUSINGUNITS = "pep/int_housingunits"

PEP_INT_NATCIVPOP = "pep/int_natcivpop"

PEP_INT_NATMONTHLY = "pep/int_natmonthly"

PEP_INT_NATRESAFO = "pep/int_natresafo"

PEP_INT_NATRESPOP = "pep/int_natrespop"

PEP_INT_POPULATION = "pep/int_population"

PEP_MONTHLYNATCHAR5 = "pep/monthlynatchar5"

PEP_MONTHLYNATCHAR6 = "pep/monthlynatchar6"

PEP_NATMONTHLY = "pep/natmonthly"

PEP_NATSTPRC = "pep/natstprc"

PEP_NATSTPRC18 = "pep/natstprc18"

PEP_POPULATION = "pep/population"

PEP_PRCAGESEX = "pep/prcagesex"

PEP_PRM = "pep/prm"

PEP_PRMAGESEX = "pep/prmagesex"

PEP_PROJAGEGROUPS = "pep/projagegroups"

PEP_PROJBIRTHS = "pep/projbirths"

PEP_PROJDEATHS = "pep/projdeaths"

PEP_PROJNAT = "pep/projnat"

PEP_PROJNIM = "pep/projnim"

PEP_PROJPOP = "pep/projpop"

PEP_STCHAR5 = "pep/stchar5"

PEP_STCHAR6 = "pep/stchar6"

PEP_SUBCTY = "pep/subcty"

POP = "popproj/pop"

POPPROJ_AGEGROUPS = "popproj/agegroups"

POPPROJ_BIRTHS = "popproj/births"

POPPROJ_DEATHS = "popproj/deaths"

POPPROJ_NAT = "popproj/nat"

POPPROJ_NIM = "popproj/nim"

PUBSCHLFIN = "pubschlfin"

SBO_CS = "sbo/cs"

SBO_CSCB = "sbo/cscb"

SBO_CSCBO = "sbo/cscbo"

SURNAME = "surname"

TIMESERIES_ASM = "timeseries/asm/value2017"

TIMESERIES_BDS = "timeseries/bds"

TIMESERIES_EITS = "timeseries/eits/vip"

TIMESERIES_GOVS = "timeseries/govs"

TIMESERIES_HEALTHINS = "timeseries/healthins/sahie"

TIMESERIES_HPS = "timeseries/hps"

TIMESERIES_IDB = "timeseries/idb/5year"

TIMESERIES_INTLTRADE = "timeseries/intltrade/imports/usda"

TIMESERIES_POVERTY = "timeseries/poverty/saipe/schdist"

TIMESERIES_PSEO = "timeseries/pseo/flows"

TIMESERIES_QWI = "timeseries/qwi/se"

ZBP = "zbp"


DATASET_REFERENCE_URLS = {
    ABS_CB: "http://api.census.gov/data/2017/abscb",
    ABS_CBO: "http://api.census.gov/data/2017/abscbo",
    ABS_CS: "http://api.census.gov/data/2017/abscs",
    ABS_MCB: "http://api.census.gov/data/2020/absmcb",
    ABS_NESD: "http://api.census.gov/data/2018/absnesd",
    ABS_NESDO: "http://api.census.gov/data/2018/absnesdo",
    ABS_TCB: "http://api.census.gov/data/2018/abstcb",
    ACS1: "http://api.census.gov/data/2005/acs/acs1",
    ACS1_CD113: "http://api.census.gov/data/2011/acs1/cd113",
    ACS1_CD115: "http://api.census.gov/data/2015/acs1/cd115",
    ACS1_CPROFILE: "http://api.census.gov/data/2010/acs/acs1/cprofile",
    ACS1_PROFILE: "http://api.census.gov/data/2005/acs/acs1/profile",
    ACS1_PUMS: "http://api.census.gov/data/2004/acs/acs1/pums",
    ACS1_PUMSPR: "http://api.census.gov/data/2005/acs/acs1/pumspr",
    ACS1_SPP: "http://api.census.gov/data/2008/acs/acs1/spp",
    ACS1_SUBJECT: "http://api.census.gov/data/2010/acs/acs1/subject",
    ACS3: "http://api.census.gov/data/2007/acs/acs3",
    ACS3_CPROFILE: "http://api.census.gov/data/2012/acs/acs3/cprofile",
    ACS3_PROFILE: "http://api.census.gov/data/2007/acs/acs3/profile",
    ACS3_SPP: "http://api.census.gov/data/2009/acs/acs3/spp",
    ACS3_SUBJECT: "http://api.census.gov/data/2010/acs/acs3/subject",
    ACS5: "http://api.census.gov/data/2009/acs/acs5",
    ACS5_AIAN: "http://api.census.gov/data/2010/acs/acs5/aian",
    ACS5_AIANPROFILE: "http://api.census.gov/data/2010/acs/acs5/aianprofile",
    ACS5_CPROFILE: "http://api.census.gov/data/2015/acs/acs5/cprofile",
    ACS5_EEO: "http://api.census.gov/data/2018/acs/acs5/eeo",
    ACS5_PROFILE: "http://api.census.gov/data/2009/acs/acs5/profile",
    ACS5_PUMS: "http://api.census.gov/data/2009/acs/acs5/pums",
    ACS5_PUMSPR: "http://api.census.gov/data/2009/acs/acs5/pumspr",
    ACS5_SPT: "http://api.census.gov/data/2010/acs/acs5/spt",
    ACS5_SPTPROFILE: "http://api.census.gov/data/2010/acs/acs5/sptprofile",
    ACS5_SUBJECT: "http://api.census.gov/data/2010/acs/acs5/subject",
    ACSSE: "http://api.census.gov/data/2014/acs/acsse",
    ACS_FLOWS: "http://api.census.gov/data/2010/acs/flows",
    ASE_CSA: "http://api.census.gov/data/2014/ase/csa",
    ASE_CSCB: "http://api.census.gov/data/2014/ase/cscb",
    ASE_CSCBO: "http://api.census.gov/data/2014/ase/cscbo",
    CBP: "http://api.census.gov/data/1986/cbp",
    CFSAREA: "http://api.census.gov/data/2012/cfsarea",
    CFSEXPORT: "http://api.census.gov/data/2012/cfsexport",
    CFSHAZMAT: "http://api.census.gov/data/2012/cfshazmat",
    CFSPRELIM: "http://api.census.gov/data/2012/cfsprelim",
    CFSTEMP: "http://api.census.gov/data/2017/cfstemp",
    CPS_ARTS: "http://api.census.gov/data/2013/cps/arts/feb",
    CPS_ASEC: "http://api.census.gov/data/1992/cps/asec/mar",
    CPS_BASIC: "http://api.census.gov/data/1989/cps/basic/may",
    CPS_CIVIC: "http://api.census.gov/data/2008/cps/civic/nov",
    CPS_CONTWORKER: "http://api.census.gov/data/2017/cps/contworker/may",
    CPS_DISABILITY: "http://api.census.gov/data/2019/cps/disability/jul",
    CPS_DWJT: "http://api.census.gov/data/2002/cps/dwjt/jan",
    CPS_FERTILITY: "http://api.census.gov/data/1998/cps/fertility/jun",
    CPS_FOODSEC: "http://api.census.gov/data/2001/cps/foodsec/dec",
    CPS_IMMIGRATION: "http://api.census.gov/data/2008/cps/immigration/aug",
    CPS_INTERNET: "http://api.census.gov/data/1994/cps/internet/nov",
    CPS_LIBRARY: "http://api.census.gov/data/2002/cps/library/oct",
    CPS_MARITAL: "http://api.census.gov/data/1995/cps/marital/jun",
    CPS_PUBARTS: "http://api.census.gov/data/2012/cps/pubarts/jul",
    CPS_RACE: "http://api.census.gov/data/1995/cps/race/may",
    CPS_SCHOOL: "http://api.census.gov/data/1994/cps/school/oct",
    CPS_TOBACCO: "http://api.census.gov/data/2006/cps/tobacco/may",
    CPS_UNBANK: "http://api.census.gov/data/2011/cps/unbank/jun",
    CPS_VETS: "http://api.census.gov/data/1995/cps/vets/aug",
    CPS_VOLUNTEER: "http://api.census.gov/data/2002/cps/volunteer/sep",
    CPS_VOTING: "http://api.census.gov/data/1994/cps/voting/nov",
    CPS_WORKSCHED: "http://api.census.gov/data/1997/cps/worksched/may",
    CRE: "http://api.census.gov/data/2019/cre",
    DEC_AIAN: "http://api.census.gov/data/2000/dec/aian",
    DEC_AIANPROFILE: "http://api.census.gov/data/2000/dec/aianprofile",
    DEC_AS: "http://api.census.gov/data/2000/dec/as",
    DEC_ASYOE: "http://api.census.gov/data/2010/dec/asyoe",
    DEC_CD110H: "http://api.census.gov/data/2000/dec/cd110h",
    DEC_CD110HPROFILE: "http://api.census.gov/data/2000/dec/cd110hprofile",
    DEC_CD110S: "http://api.census.gov/data/2000/dec/cd110s",
    DEC_CD110SPROFILE: "http://api.census.gov/data/2000/dec/cd110sprofile",
    DEC_CD113: "http://api.census.gov/data/2010/dec/cd113",
    DEC_CD113PROFILE: "http://api.census.gov/data/2010/dec/cd113profile",
    DEC_CD115: "http://api.census.gov/data/2010/dec/cd115",
    DEC_CD115PROFILE: "http://api.census.gov/data/2010/dec/cd115profile",
    DEC_CD116: "http://api.census.gov/data/2010/dec/cd116",
    DEC_CQR: "http://api.census.gov/data/2000/dec/cqr",
    DEC_DHC: "http://api.census.gov/data/2020/dec/dhc",
    DEC_DHCAS: "http://api.census.gov/data/2020/dec/dhcas",
    DEC_DHCGU: "http://api.census.gov/data/2020/dec/dhcgu",
    DEC_DHCMP: "http://api.census.gov/data/2020/dec/dhcmp",
    DEC_DHCVI: "http://api.census.gov/data/2020/dec/dhcvi",
    DEC_DP: "http://api.census.gov/data/2020/dec/dp",
    DEC_DPAS: "http://api.census.gov/data/2020/dec/dpas",
    DEC_DPGU: "http://api.census.gov/data/2020/dec/dpgu",
    DEC_DPMP: "http://api.census.gov/data/2020/dec/dpmp",
    DEC_DPVI: "http://api.census.gov/data/2020/dec/dpvi",
    DEC_GU: "http://api.census.gov/data/2000/dec/gu",
    DEC_GUYOE: "http://api.census.gov/data/2010/dec/guyoe",
    DEC_MP: "http://api.census.gov/data/2000/dec/mp",
    DEC_MPYOE: "http://api.census.gov/data/2010/dec/mpyoe",
    DEC_PES: "http://api.census.gov/data/2020/dec/pes",
    DEC_PL: "http://api.census.gov/data/2000/dec/pl",
    DEC_PLNAT: "http://api.census.gov/data/2010/dec/plnat",
    DEC_RESPONSERATE: "http://api.census.gov/data/2010/dec/responserate",
    DEC_SF1: "http://api.census.gov/data/2000/dec/sf1",
    DEC_SF2: "http://api.census.gov/data/2000/dec/sf2",
    DEC_SF2PROFILE: "http://api.census.gov/data/2000/dec/sf2profile",
    DEC_SF3: "http://api.census.gov/data/2000/dec/sf3",
    DEC_SF3PROFILE: "http://api.census.gov/data/2000/dec/sf3profile",
    DEC_SF4: "http://api.census.gov/data/2000/dec/sf4",
    DEC_SF4PROFILE: "http://api.census.gov/data/2000/dec/sf4profile",
    DEC_SLDH: "http://api.census.gov/data/2000/dec/sldh",
    DEC_SLDHPROFILE: "http://api.census.gov/data/2000/dec/sldhprofile",
    DEC_SLDS: "http://api.census.gov/data/2000/dec/slds",
    DEC_SLDSPROFILE: "http://api.census.gov/data/2000/dec/sldsprofile",
    DEC_VI: "http://api.census.gov/data/2000/dec/vi",
    ECN_ADBNPROP: "http://api.census.gov/data/2017/ecnadbnprop",
    ECN_ADMBEN: "http://api.census.gov/data/2012/ecnadmben",
    ECN_BASIC: "http://api.census.gov/data/2012/ecnbasic",
    ECN_BRANDDEAL: "http://api.census.gov/data/2012/ecnbranddeal",
    ECN_BRIDGE1: "http://api.census.gov/data/2012/ecnbridge1",
    ECN_BRIDGE2: "http://api.census.gov/data/2012/ecnbridge2",
    ECN_BRORDEAL: "http://api.census.gov/data/2012/ecnbrordeal",
    ECN_CASHADV: "http://api.census.gov/data/2012/ecncashadv",
    ECN_CCARD: "http://api.census.gov/data/2012/ecnccard",
    ECN_CLCUST: "http://api.census.gov/data/2012/ecnclcust",
    ECN_COMM: "http://api.census.gov/data/2012/ecncomm",
    ECN_COMP: "http://api.census.gov/data/2012/ecncomp",
    ECN_CONACT: "http://api.census.gov/data/2012/ecnconact",
    ECN_CONCESS: "http://api.census.gov/data/2012/ecnconcess",
    ECN_CRFIN: "http://api.census.gov/data/2012/ecncrfin",
    ECN_DIRPREM: "http://api.census.gov/data/2017/ecndirprem",
    ECN_DISSMED: "http://api.census.gov/data/2012/ecndissmed",
    ECN_ELMENU: "http://api.census.gov/data/2017/ecnelmenu",
    ECN_EMPFUNC: "http://api.census.gov/data/2012/ecnempfunc",
    ECN_ENTSUP: "http://api.census.gov/data/2012/ecnentsup",
    ECN_EOYINV: "http://api.census.gov/data/2012/ecneoyinv",
    ECN_EOYINVWH: "http://api.census.gov/data/2012/ecneoyinvwh",
    ECN_EQUIP: "http://api.census.gov/data/2012/ecnequip",
    ECN_EXPNRG: "http://api.census.gov/data/2012/ecnexpnrg",
    ECN_EXPSVC: "http://api.census.gov/data/2012/ecnexpsvc",
    ECN_FLSPACE: "http://api.census.gov/data/2012/ecnflspace",
    ECN_FOODSVC: "http://api.census.gov/data/2012/ecnfoodsvc",
    ECN_FRAN: "http://api.census.gov/data/2012/ecnfran",
    ECN_GRANT: "http://api.census.gov/data/2012/ecngrant",
    ECN_GUEST: "http://api.census.gov/data/2012/ecnguest",
    ECN_GUESTSIZE: "http://api.census.gov/data/2012/ecnguestsize",
    ECN_HOSP: "http://api.census.gov/data/2012/ecnhosp",
    ECN_HOTEL: "http://api.census.gov/data/2017/ecnhotel",
    ECN_INSTR: "http://api.census.gov/data/2017/ecninstr",
    ECN_INVVAL: "http://api.census.gov/data/2012/ecninvval",
    ECN_IPA: "http://api.census.gov/data/2012/ecnipa",
    ECN_ISLANDAREAS: "http://api.census.gov/data/2017/ecn/islandareas/napcs",
    ECN_KOB: "http://api.census.gov/data/2012/ecnkob",
    ECN_LABOR: "http://api.census.gov/data/2012/ecnlabor",
    ECN_LIFOMFG: "http://api.census.gov/data/2012/ecnlifomfg",
    ECN_LIFOMINE: "http://api.census.gov/data/2012/ecnlifomine",
    ECN_LIFOVAL: "http://api.census.gov/data/2012/ecnlifoval",
    ECN_LINES: "http://api.census.gov/data/2012/ecnlines",
    ECN_LOAN: "http://api.census.gov/data/2012/ecnloan",
    ECN_LOCCONS: "http://api.census.gov/data/2017/ecnloccons",
    ECN_LOCMFG: "http://api.census.gov/data/2012/ecnlocmfg",
    ECN_LOCMINE: "http://api.census.gov/data/2012/ecnlocmine",
    ECN_MARGIN: "http://api.census.gov/data/2012/ecnmargin",
    ECN_MATFUEL: "http://api.census.gov/data/2012/ecnmatfuel",
    ECN_MEALCOST: "http://api.census.gov/data/2012/ecnmealcost",
    ECN_MENUTYPE: "http://api.census.gov/data/2012/ecnmenutype",
    ECN_NAPCSIND: "http://api.census.gov/data/2017/ecnnapcsind",
    ECN_NAPCSPRD: "http://api.census.gov/data/2017/ecnnapcsprd",
    ECN_PATIENT: "http://api.census.gov/data/2012/ecnpatient",
    ECN_PETRFAC: "http://api.census.gov/data/2012/ecnpetrfac",
    ECN_PETRPROD: "http://api.census.gov/data/2012/ecnpetrprod",
    ECN_PETRREC: "http://api.census.gov/data/2012/ecnpetrrec",
    ECN_PETRSTAT: "http://api.census.gov/data/2012/ecnpetrstat",
    ECN_PROFIT: "http://api.census.gov/data/2012/ecnprofit",
    ECN_PURELEC: "http://api.census.gov/data/2012/ecnpurelec",
    ECN_PURGAS: "http://api.census.gov/data/2017/ecnpurgas",
    ECN_PURMODE: "http://api.census.gov/data/2012/ecnpurmode",
    ECN_RDACQ: "http://api.census.gov/data/2012/ecnrdacq",
    ECN_RDOFC: "http://api.census.gov/data/2012/ecnrdofc",
    ECN_SEAT: "http://api.census.gov/data/2012/ecnseat",
    ECN_SIZE: "http://api.census.gov/data/2012/ecnsize",
    ECN_SOCIAL: "http://api.census.gov/data/2012/ecnsocial",
    ECN_TYPE: "http://api.census.gov/data/2012/ecntype",
    ECN_TYPEPAYER: "http://api.census.gov/data/2017/ecntypepayer",
    ECN_TYPOP: "http://api.census.gov/data/2012/ecntypop",
    ECN_VALCON: "http://api.census.gov/data/2012/ecnvalcon",
    EWKS: "http://api.census.gov/data/1997/ewks",
    INTLTRADE_IMP_EXP: "http://api.census.gov/data/2014/intltrade/imp_exp",
    LANGUAGE: "http://api.census.gov/data/2013/language",
    NONEMP: "http://api.census.gov/data/1997/nonemp",
    PDB_BLOCKGROUP: "http://api.census.gov/data/2015/pdb/blockgroup",
    PDB_STATECOUNTY: "http://api.census.gov/data/2020/pdb/statecounty",
    PDB_TRACT: "http://api.census.gov/data/2015/pdb/tract",
    PEP_AGESEX: "http://api.census.gov/data/2014/pep/agesex",
    PEP_AGESPECIAL5: "http://api.census.gov/data/2014/pep/agespecial5",
    PEP_AGESPECIAL6: "http://api.census.gov/data/2014/pep/agespecial6",
    PEP_AGESPECIALPR: "http://api.census.gov/data/2014/pep/agespecialpr",
    PEP_CHARAGE: "http://api.census.gov/data/2015/pep/charage",
    PEP_CHARAGEGROUPS: "http://api.census.gov/data/2015/pep/charagegroups",
    PEP_COCHAR5: "http://api.census.gov/data/2013/pep/cochar5",
    PEP_COCHAR6: "http://api.census.gov/data/2013/pep/cochar6",
    PEP_COMPONENTS: "http://api.census.gov/data/2015/pep/components",
    PEP_CTY: "http://api.census.gov/data/2013/pep/cty",
    PEP_HOUSING: "http://api.census.gov/data/2013/pep/housing",
    PEP_INT_CHARAGE: "http://api.census.gov/data/2000/pep/int_charage",
    PEP_INT_CHARAGEGROUPS: "http://api.census.gov/data/1990/pep/int_charagegroups",
    PEP_INT_HOUSINGUNITS: "http://api.census.gov/data/2000/pep/int_housingunits",
    PEP_INT_NATCIVPOP: "http://api.census.gov/data/1990/pep/int_natcivpop",
    PEP_INT_NATMONTHLY: "http://api.census.gov/data/2000/pep/int_natmonthly",
    PEP_INT_NATRESAFO: "http://api.census.gov/data/1990/pep/int_natresafo",
    PEP_INT_NATRESPOP: "http://api.census.gov/data/1990/pep/int_natrespop",
    PEP_INT_POPULATION: "http://api.census.gov/data/2000/pep/int_population",
    PEP_MONTHLYNATCHAR5: "http://api.census.gov/data/2013/pep/monthlynatchar5",
    PEP_MONTHLYNATCHAR6: "http://api.census.gov/data/2013/pep/monthlynatchar6",
    PEP_NATMONTHLY: "http://api.census.gov/data/2015/pep/natmonthly",
    PEP_NATSTPRC: "http://api.census.gov/data/2013/pep/natstprc",
    PEP_NATSTPRC18: "http://api.census.gov/data/2013/pep/natstprc18",
    PEP_POPULATION: "http://api.census.gov/data/2015/pep/population",
    PEP_PRCAGESEX: "http://api.census.gov/data/2013/pep/prcagesex",
    PEP_PRM: "http://api.census.gov/data/2013/pep/prm",
    PEP_PRMAGESEX: "http://api.census.gov/data/2013/pep/prmagesex",
    PEP_PROJAGEGROUPS: "http://api.census.gov/data/2014/pep/projagegroups",
    PEP_PROJBIRTHS: "http://api.census.gov/data/2014/pep/projbirths",
    PEP_PROJDEATHS: "http://api.census.gov/data/2014/pep/projdeaths",
    PEP_PROJNAT: "http://api.census.gov/data/2014/pep/projnat",
    PEP_PROJNIM: "http://api.census.gov/data/2014/pep/projnim",
    PEP_PROJPOP: "http://api.census.gov/data/2014/pep/projpop",
    PEP_STCHAR5: "http://api.census.gov/data/2013/pep/stchar5",
    PEP_STCHAR6: "http://api.census.gov/data/2013/pep/stchar6",
    PEP_SUBCTY: "http://api.census.gov/data/2013/pep/subcty",
    POP: "http://api.census.gov/data/2012/popproj/pop",
    POPPROJ_AGEGROUPS: "http://api.census.gov/data/2017/popproj/agegroups",
    POPPROJ_BIRTHS: "http://api.census.gov/data/2012/popproj/births",
    POPPROJ_DEATHS: "http://api.census.gov/data/2012/popproj/deaths",
    POPPROJ_NAT: "http://api.census.gov/data/2017/popproj/nat",
    POPPROJ_NIM: "http://api.census.gov/data/2012/popproj/nim",
    PUBSCHLFIN: "http://api.census.gov/data/2012/pubschlfin",
    SBO_CS: "http://api.census.gov/data/2012/sbo/cs",
    SBO_CSCB: "http://api.census.gov/data/2012/sbo/cscb",
    SBO_CSCBO: "http://api.census.gov/data/2012/sbo/cscbo",
    SURNAME: "http://api.census.gov/data/2000/surname",
    TIMESERIES_ASM: "http://api.census.gov/data/timeseries/asm/value2017",
    TIMESERIES_BDS: "http://api.census.gov/data/timeseries/bds",
    TIMESERIES_EITS: "http://api.census.gov/data/timeseries/eits/vip",
    TIMESERIES_GOVS: "http://api.census.gov/data/timeseries/govs",
    TIMESERIES_HEALTHINS: "http://api.census.gov/data/timeseries/healthins/sahie",
    TIMESERIES_HPS: "http://api.census.gov/data/timeseries/hps",
    TIMESERIES_IDB: "http://api.census.gov/data/timeseries/idb/5year",
    TIMESERIES_INTLTRADE: "http://api.census.gov/data/timeseries/intltrade/imports/usda",
    TIMESERIES_POVERTY: "http://api.census.gov/data/timeseries/poverty/saipe/schdist",
    TIMESERIES_PSEO: "http://api.census.gov/data/timeseries/pseo/flows",
    TIMESERIES_QWI: "http://api.census.gov/data/timeseries/qwi/se",
    ZBP: "http://api.census.gov/data/1994/zbp",
}
