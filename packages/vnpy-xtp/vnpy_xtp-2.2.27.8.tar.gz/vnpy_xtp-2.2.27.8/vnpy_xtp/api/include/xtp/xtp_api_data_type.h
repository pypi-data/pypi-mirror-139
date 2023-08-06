/////////////////////////////////////////////////////////////////////////
///@author ��̩֤ȯ�ɷ����޹�˾
///@file xtp_api_data_type.h
///@brief ����������ݻ�������
/////////////////////////////////////////////////////////////////////////
#ifndef _XTP_API_DATA_TYPE_H_
#define _XTP_API_DATA_TYPE_H_

#pragma pack(8)

/// ÿ��PBU��౻10��TGWʹ�á�
#define MAX_TGW_CNT_PER_PBU             10

/// ��Ű汾�ŵ��ַ�������
#define XTP_VERSION_LEN 16
/// �汾������
typedef char XTPVersionType[XTP_VERSION_LEN];
/// �ɽ������ַ�������
#define XTP_TRADING_DAY_LEN 9
/// ���֤ȯ������ַ�������
#define XTP_TICKER_LEN 16
/// ���֤ȯ���Ƶ��ַ�������
#define XTP_TICKER_NAME_LEN 64
/// ���ر�����ŵ��ַ�������
#define XTP_LOCAL_ORDER_LEN         11
/// ���������ŵ��ַ�������
#define XTP_ORDER_EXCH_LEN          17
/// �ɽ�ִ�б�ŵ��ַ�������
#define XTP_EXEC_ID_LEN             18
/// ����������Ա�����ַ�������
#define XTP_BRANCH_PBU_LEN          7
/// �û��ʽ��˻����ַ�������
#define XTP_ACCOUNT_NAME_LEN        16
/// ����ҵ���Լ��ծ��ų���
#define XTP_CREDIT_DEBT_ID_LEN      33
/// IP��ַ���ַ�������
#define XTP_INET_ADDRESS_STR_LEN 64
/// MAC��ַ���ַ�������
#define XTP_MAC_ADDRESS_LEN 16
/// Ӳ�����кŵ��ַ�������
#define XTP_HARDDISK_SN_LEN 24
/// MacOSϵͳ���кŵ��ַ�������
#define XTP_MACOS_SNO_LEN 21

/// ��Ȩ��ϲ����������
#define XTP_STRATEGE_LEG_NUM        4
/// ��Ȩ��ϲ��Դ����ַ�������
#define XTP_STRATEGY_ID_LEN         10
/// ��Ȩ��ϲ��������ַ�������
#define XTP_STRATEGY_NAME_LEN       32
/// ��Ȩ��ϲ�����ϱ����ַ�������
#define XTP_SECONDARY_ORDER_ID_LEN  18

/// ��Ȩ��Լ��֧�ֵ���ϲ����б��ַ�������
#define XTP_CNTRT_COMB_STRA_LIST_LEN         2048

/// ��Ȩ��Ȩ�ϲ����ɷֺ�Լ����
#define XTP_COMBINED_EXECUTION_LEG_NUM       2

/////////////////////////////////////////////////////////////////////////
///@brief XTP_LOG_LEVEL����־�����������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_LOG_LEVEL {
	XTP_LOG_LEVEL_FATAL, ///<���ش��󼶱�
	XTP_LOG_LEVEL_ERROR, ///<���󼶱�
	XTP_LOG_LEVEL_WARNING, ///<���漶��
	XTP_LOG_LEVEL_INFO,   ///<info����
	XTP_LOG_LEVEL_DEBUG,  ///<debug����
	XTP_LOG_LEVEL_TRACE   ///<trace����
}XTP_LOG_LEVEL;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_PROTOCOL_TYPE��ͨѶ����Э�鷽ʽ
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_PROTOCOL_TYPE
{
	XTP_PROTOCOL_TCP = 1,	///<����TCP��ʽ����
	XTP_PROTOCOL_UDP		///<����UDP��ʽ����(������ӿ�֧��)
}XTP_PROTOCOL_TYPE;



/////////////////////////////////////////////////////////////////////////
///@brief XTP_EXCHANGE_TYPE�ǽ��������ͣ�������ʹ��
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_EXCHANGE_TYPE
{
	XTP_EXCHANGE_SH = 1,	///<��֤
	XTP_EXCHANGE_SZ,		///<��֤
    XTP_EXCHANGE_UNKNOWN	///<�����ڵĽ���������
}XTP_EXCHANGE_TYPE;

//////////////////////////////////////////////////////////////////////////
///@brief XTP_MARKET_TYPE�г����ͣ�������ʹ��
//////////////////////////////////////////////////////////////////////////
typedef enum XTP_MARKET_TYPE
{
    XTP_MKT_INIT = 0,///<��ʼ��ֵ����δ֪
    XTP_MKT_SZ_A = 1,///<����A��
    XTP_MKT_SH_A,    ///<�Ϻ�A��
    XTP_MKT_UNKNOWN   ///<δ֪�����г�����
}XTP_MARKET_TYPE;


/////////////////////////////////////////////////////////////////////////
///@brief XTP_PRICE_TYPE�Ǽ۸�����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_PRICE_TYPE
{
	XTP_PRICE_LIMIT = 1,           ///<�޼۵�-�� / �� / ����Ȩ / ����Ȩ ������ͨ��Ʊҵ���⣬����δ��ָ��ҵ���ʹ�ô������ͣ�
	XTP_PRICE_BEST_OR_CANCEL,      ///<��ʱ�ɽ�ʣ��ת�������м۵�-�� / ����Ȩ / ����Ȩ
	XTP_PRICE_BEST5_OR_LIMIT,      ///<�����嵵��ʱ�ɽ�ʣ��ת�޼ۣ��м۵�-��
	XTP_PRICE_BEST5_OR_CANCEL,     ///<����5����ʱ�ɽ�ʣ��ת�������м۵�-���� / ����Ȩ
	XTP_PRICE_ALL_OR_CANCEL,       ///<ȫ���ɽ�����,�м۵�-�� / ����Ȩ / ����Ȩ
	XTP_PRICE_FORWARD_BEST,        ///<�������ţ��м۵�-�� / ����Ȩ / ���ƴ���
	XTP_PRICE_REVERSE_BEST_LIMIT,  ///<�Է�����ʣ��ת�޼ۣ��м۵�-�� / ����Ȩ / ����Ȩ / ���ƴ���
	XTP_PRICE_LIMIT_OR_CANCEL,	   ///<��Ȩ�޼��걨FOK
	XTP_PRICE_TYPE_UNKNOWN,		   ///<δ֪������Ч�۸�����
}XTP_PRICE_TYPE;



/////////////////////////////////////////////////////////////////////////
///@brief XTP_SIDE_TYPE��������������
/////////////////////////////////////////////////////////////////////////
typedef uint8_t XTP_SIDE_TYPE;

///���¹��깺��ETF����ɣ����ý����е���Ʒ��
#define XTP_SIDE_BUY            1
///������ع���ETF�������ý����е���Ʒ����
#define XTP_SIDE_SELL           2
///�깺
#define XTP_SIDE_PURCHASE       7
///���
#define XTP_SIDE_REDEMPTION     8
///���
#define XTP_SIDE_SPLIT          9
///�ϲ�
#define XTP_SIDE_MERGE          10
///�İ�֮���side�ı��ң��ݲ�֧��
#define XTP_SIDE_COVER          11
///�İ�֮���side��������Ӧ��ƽ��ʶΪ����/��������Ӧ��ƽ��ʶΪƽ��
#define XTP_SIDE_FREEZE         12
/// ��������
#define XTP_SIDE_MARGIN_TRADE	21
/// ��ȯ����
#define XTP_SIDE_SHORT_SELL		22
/// ��ȯ����
#define XTP_SIDE_REPAY_MARGIN	23
/// ��ȯ��ȯ
#define XTP_SIDE_REPAY_STOCK	24
/// �ֽ𻹿��������ͨ����Э�飬�������Ͳ�ѯЭ�飩
//#define XTP_SIDE_CASH_REPAY_MARGIN	25
/// ��ȯ��ȯ
#define XTP_SIDE_STOCK_REPAY_STOCK	26
/// ��ȯ��ת
#define XTP_SIDE_SURSTK_TRANS       27
/// ����Ʒת��
#define XTP_SIDE_GRTSTK_TRANSIN     28
/// ����Ʒת��
#define XTP_SIDE_GRTSTK_TRANSOUT    29

///��ϲ��Ե����
#define XTP_SIDE_OPT_COMBINE        31 
///��ϲ��ԵĲ��
#define XTP_SIDE_OPT_SPLIT          32 
///��ϲ��ԵĹ���Աǿ�Ʋ��
#define XTP_SIDE_OPT_SPLIT_FORCE    33 
///��ϲ��ԵĽ�����ǿ�Ʋ��
#define XTP_SIDE_OPT_SPLIT_FORCE_EXCH    34

///δ֪������Ч��������
#define XTP_SIDE_UNKNOWN        50



/////////////////////////////////////////////////////////////////////////
///@brief XTP_POSITION_EFFECT_TYPE�ǿ�ƽ��ʶ����
/////////////////////////////////////////////////////////////////////////
typedef uint8_t XTP_POSITION_EFFECT_TYPE;

/// ��ʼֵ��δֵ֪��ƽ��ʶ������Ȩ�⣬��ʹ�ô�ֵ
#define XTP_POSITION_EFFECT_INIT                0
/// ��
#define XTP_POSITION_EFFECT_OPEN                1
/// ƽ
#define XTP_POSITION_EFFECT_CLOSE               2
/// ǿƽ
#define XTP_POSITION_EFFECT_FORCECLOSE          3
/// ƽ��
#define XTP_POSITION_EFFECT_CLOSETODAY          4
/// ƽ��
#define XTP_POSITION_EFFECT_CLOSEYESTERDAY      5
/// ǿ��
#define XTP_POSITION_EFFECT_FORCEOFF            6
/// ����ǿƽ
#define XTP_POSITION_EFFECT_LOCALFORCECLOSE     7
/// ����ҵ��׷��ǿƽ
#define XTP_POSITION_EFFECT_CREDIT_FORCE_COVER  8
/// ����ҵ���峥ǿƽ
#define XTP_POSITION_EFFECT_CREDIT_FORCE_CLEAR  9
/// ����ҵ���Լ����ǿƽ
#define XTP_POSITION_EFFECT_CREDIT_FORCE_DEBT   10
/// ����ҵ��������ǿƽ
#define XTP_POSITION_EFFECT_CREDIT_FORCE_UNCOND 11
/// δ֪�Ŀ�ƽ��ʶ����
#define XTP_POSITION_EFFECT_UNKNOWN             12


/////////////////////////////////////////////////////////////////////////
///@brief XTP_ORDER_ACTION_STATUS_TYPE�Ǳ�������״̬����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_ORDER_ACTION_STATUS_TYPE
{
	XTP_ORDER_ACTION_STATUS_SUBMITTED = 1,	///<�Ѿ��ύ
	XTP_ORDER_ACTION_STATUS_ACCEPTED,		///<�Ѿ�����
	XTP_ORDER_ACTION_STATUS_REJECTED		///<�Ѿ����ܾ�
}XTP_ORDER_ACTION_STATUS_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_ORDER_STATUS_TYPE�Ǳ���״̬����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_ORDER_STATUS_TYPE
{
    XTP_ORDER_STATUS_INIT = 0,///<��ʼ��
    XTP_ORDER_STATUS_ALLTRADED = 1,           ///<ȫ���ɽ�
    XTP_ORDER_STATUS_PARTTRADEDQUEUEING,  ///<���ֳɽ�
    XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING, ///<���ֳ���
    XTP_ORDER_STATUS_NOTRADEQUEUEING,   ///<δ�ɽ�
    XTP_ORDER_STATUS_CANCELED,  ///<�ѳ���
    XTP_ORDER_STATUS_REJECTED,  ///<�Ѿܾ�
    XTP_ORDER_STATUS_UNKNOWN  ///<δ֪����״̬
}XTP_ORDER_STATUS_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_ORDER_SUBMIT_STATUS_TYPE�Ǳ����ύ״̬����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_ORDER_SUBMIT_STATUS_TYPE
{
    XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED = 1, ///<�����Ѿ��ύ
    XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED,///<�����Ѿ�������
    XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED,///<�����Ѿ����ܾ�
    XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED,///<�����Ѿ��ύ
    XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED,///<�����Ѿ����ܾ�
    XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED ///<�����Ѿ�������
}XTP_ORDER_SUBMIT_STATUS_TYPE;


/////////////////////////////////////////////////////////////////////////
///@brief XTP_TE_RESUME_TYPE�ǹ�������������Ӧ���ɽ��ر����ش���ʽ
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_TE_RESUME_TYPE
{
	XTP_TERT_RESTART = 0,	///<�ӱ������տ�ʼ�ش�
	XTP_TERT_RESUME,		///<�Ӵ��ϴ��յ�����������δ֧�֣�
	XTP_TERT_QUICK			///<ֻ���͵�¼��������������Ӧ���ɽ��ر���������
}XTP_TE_RESUME_TYPE;


//////////////////////////////////////////////////////////////////////////
///@brief ETF_REPLACE_TYPE�ֽ������ʶ����
//////////////////////////////////////////////////////////////////////////
typedef enum ETF_REPLACE_TYPE
{
    ERT_CASH_FORBIDDEN = 0,             ///<��ֹ�ֽ����
    ERT_CASH_OPTIONAL,                  ///<�����ֽ����
    ERT_CASH_MUST,                      ///<�����ֽ����
    ERT_CASH_RECOMPUTE_INTER_SZ,        ///<�����˲��ֽ����
    ERT_CASH_MUST_INTER_SZ,             ///<���б����ֽ����
    ERT_CASH_RECOMPUTE_INTER_OTHER,     ///<�ǻ����г��ɷ�֤ȯ�˲��ֽ�������������ڿ绦���ETF��Ʒ��
    ERT_CASH_MUST_INTER_OTHER,          ///<��ʾ�ǻ����г��ɷ�֤ȯ�����ֽ�������������ڿ绦���ETF��Ʒ��
    ERT_CASH_RECOMPUTE_INTER_HK,	    ///�����˲��ֽ�������������ڿ绦���ETF��Ʒ��
    ERT_CASH_MUST_INTER_HK,		        ///���б����ֽ�������������ڿ绦���ETF��Ʒ��
    EPT_INVALID                         ///<��Чֵ
}ETF_REPLACE_TYPE;


//////////////////////////////////////////////////////////////////////////
///@brief XTP_TICKER_TYPE֤ȯ����
//////////////////////////////////////////////////////////////////////////
typedef enum XTP_TICKER_TYPE
{
	XTP_TICKER_TYPE_STOCK = 0,            ///<��ͨ��Ʊ
	XTP_TICKER_TYPE_INDEX,                ///<ָ��
	XTP_TICKER_TYPE_FUND,                 ///<����
	XTP_TICKER_TYPE_BOND,                 ///<ծȯ
	XTP_TICKER_TYPE_OPTION,               ///<��Ȩ
    XTP_TICKER_TYPE_TECH_STOCK,           ///<�ƴ����Ʊ���Ϻ���
	XTP_TICKER_TYPE_UNKNOWN               ///<δ֪����
	
}XTP_TICKER_TYPE;

//////////////////////////////////////////////////////////////////////////
///@brief XTP_BUSINESS_TYPE֤ȯҵ������
//////////////////////////////////////////////////////////////////////////
typedef enum XTP_BUSINESS_TYPE
{
	XTP_BUSINESS_TYPE_CASH = 0,            ///<��ͨ��Ʊҵ�񣨹�Ʊ������ETF���������н����ͻ��һ���ȣ�
	XTP_BUSINESS_TYPE_IPOS,                ///<�¹��깺ҵ�񣨶�Ӧ��price type��ѡ���޼����ͣ�
	XTP_BUSINESS_TYPE_REPO,                ///<�ع�ҵ�񣨹�ծ��ع�ҵ���Ӧ��price type��Ϊ�޼ۣ�side��Ϊ����
	XTP_BUSINESS_TYPE_ETF,                 ///<ETF����ҵ��
	XTP_BUSINESS_TYPE_MARGIN,              ///<������ȯҵ��
	XTP_BUSINESS_TYPE_DESIGNATION,         ///<ת�йܣ�δ֧�֣�
	XTP_BUSINESS_TYPE_ALLOTMENT,		   ///<���ҵ�񣨶�Ӧ��price type��ѡ���޼�����,side��Ϊ��
	XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION,	   ///<�ּ���������ҵ��
	XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE,	   ///<�ּ������ֺϲ�ҵ��
	XTP_BUSINESS_TYPE_MONEY_FUND,		   ///<���һ�������ҵ����δ֧�֣����н����ͻ��һ����������ʹ����ͨ��Ʊҵ��
    XTP_BUSINESS_TYPE_OPTION,              ///<��Ȩҵ��
    XTP_BUSINESS_TYPE_EXECUTE,             ///<��Ȩ
    XTP_BUSINESS_TYPE_FREEZE,              ///<�����������ݲ�֧��
    XTP_BUSINESS_TYPE_OPTION_COMBINE,      ///<��Ȩ��ϲ��� ��ϺͲ��ҵ��
    XTP_BUSINESS_TYPE_EXECUTE_COMBINE,     ///<��Ȩ��Ȩ�ϲ�ҵ��
    XTP_BUSINESS_TYPE_UNKNOWN,             ///<δ֪����
} XTP_BUSINESS_TYPE;

//////////////////////////////////////////////////////////////////////////
///@brief XTP_ACCOUNT_TYPE�˻�����
//////////////////////////////////////////////////////////////////////////
typedef enum XTP_ACCOUNT_TYPE
{
    XTP_ACCOUNT_NORMAL = 0,	///<��ͨ�˻�
    XTP_ACCOUNT_CREDIT,		///<�����˻�
    XTP_ACCOUNT_DERIVE,		///<����Ʒ�˻�
    XTP_ACCOUNT_UNKNOWN		///<δ֪�˻�����
}XTP_ACCOUNT_TYPE;


/////////////////////////////////////////////////////////////////////////
///@brief XTP_FUND_TRANSFER_TYPE���ʽ���ת��������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_FUND_TRANSFER_TYPE
{
    XTP_FUND_TRANSFER_OUT = 0,		///<ת�� ��XTPת������̨
    XTP_FUND_TRANSFER_IN,	        ///<ת�� �ӹ�̨ת��XTP
    XTP_FUND_INTER_TRANSFER_OUT,    ///<��ڵ�ת�� �ӱ�XTP�ڵ�1��ת�����Զ�XTP�ڵ�2��XTP������֮�仮����ֻ�ܿ��˻��û�ʹ��
    XTP_FUND_INTER_TRANSFER_IN,     ///<��ڵ�ת�� �ӶԶ�XTP�ڵ�2��ת�뵽��XTP�ڵ�1��XTP������֮�仮����ֻ�ܿ��˻��û�ʹ��
    XTP_FUND_TRANSFER_UNKNOWN		///<δ֪����
}XTP_FUND_TRANSFER_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_FUND_OPER_STATUS��̨�ʽ�������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_FUND_OPER_STATUS {
    XTP_FUND_OPER_PROCESSING = 0,	///<XTP���յ������ڴ�����
    XTP_FUND_OPER_SUCCESS,			///<�ɹ�
    XTP_FUND_OPER_FAILED,			///<ʧ��
    XTP_FUND_OPER_SUBMITTED,		///<���ύ�����й�̨����
    XTP_FUND_OPER_UNKNOWN			///<δ֪
}XTP_FUND_OPER_STATUS;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_DEBT_EXTEND_OPER_STATUS��̨��ծչ�ڲ���״̬
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_DEBT_EXTEND_OPER_STATUS {
	XTP_DEBT_EXTEND_OPER_PROCESSING = 0,	///<XTP���յ������ڴ�����
	XTP_DEBT_EXTEND_OPER_SUBMITTED,			///<���ύ�����й�̨����
	XTP_DEBT_EXTEND_OPER_SUCCESS,			///<�ɹ�
	XTP_DEBT_EXTEND_OPER_FAILED,			///<ʧ��
	XTP_DEBT_EXTEND_OPER_UNKNOWN			///<δ֪
}XTP_DEBT_EXTEND_OPER_STATUS;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_SPLIT_MERGE_STATUS��һ���������ֺϲ�״̬����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_SPLIT_MERGE_STATUS {
	XTP_SPLIT_MERGE_STATUS_ALLOW = 0,	///<�����ֺͺϲ�
	XTP_SPLIT_MERGE_STATUS_ONLY_SPLIT,	///<ֻ�����֣�������ϲ�
	XTP_SPLIT_MERGE_STATUS_ONLY_MERGE,	///<ֻ����ϲ�����������
	XTP_SPLIT_MERGE_STATUS_FORBIDDEN	///<�������ֺϲ�
}XTP_SPLIT_MERGE_STATUS;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_TBT_TYPE��һ����ʻر�����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_TBT_TYPE {
	XTP_TBT_ENTRUST = 1,	///<���ί��
	XTP_TBT_TRADE = 2,		///<��ʳɽ�
}XTP_TBT_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_OPT_CALL_OR_PUT_TYPE��һ���Ϲ����Ϲ�����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_OPT_CALL_OR_PUT_TYPE {
	XTP_OPT_CALL = 1,	    ///<�Ϲ�
	XTP_OPT_PUT = 2,		///<�Ϲ�
}XTP_OPT_CALL_OR_PUT_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_OPT_EXERCISE_TYPE_TYPE��һ����Ȩ��ʽ����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_OPT_EXERCISE_TYPE_TYPE {
	XTP_OPT_EXERCISE_TYPE_EUR = 1,	    ///<ŷʽ
	XTP_OPT_EXERCISE_TYPE_AME = 2,		///<��ʽ
}XTP_OPT_EXERCISE_TYPE_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_POSITION_DIRECTION_TYPE��һ���ֲַ�������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_POSITION_DIRECTION_TYPE {
	XTP_POSITION_DIRECTION_NET = 0,	    ///<��
	XTP_POSITION_DIRECTION_LONG,		///<�ࣨ��Ȩ��ΪȨ������
    XTP_POSITION_DIRECTION_SHORT,       ///<�գ���Ȩ��Ϊ���񷽣�
    XTP_POSITION_DIRECTION_COVERED,     ///<���ң���Ȩ��Ϊ�������񷽣�
}XTP_POSITION_DIRECTION_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_OPT_COVERED_OR_UNCOVERED�Ƿ񱸶ҵı�ǩ
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_OPT_COVERED_OR_UNCOVERED {
    XTP_POSITION_UNCOVERED = 0,     ///<�Ǳ���
    XTP_POSITION_COVERED,           ///<����
}XTP_OPT_COVERED_OR_UNCOVERED;


/////////////////////////////////////////////////////////////////////////
///@brief XTP_CRD_CASH_REPAY_STATUS��һ��������ȯֱ�ӻ���״̬����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_CRD_CR_STATUS {
    XTP_CRD_CR_INIT = 0,        ///< ��ʼ��δ����״̬
    XTP_CRD_CR_SUCCESS,         ///< �ѳɹ�����״̬
    XTP_CRD_CR_FAILED,          ///< ����ʧ��״̬
} XTP_CRD_CR_STATUS;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_OPT_POSITION_TYPE��һ����Ȩ�ֲ�����
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_OPT_POSITION_TYPE
{
	XTP_OPT_POSITION_TYPE_CONTRACT = 0,     ///< ����Լ�ֲ�
	XTP_OPT_POSITION_TYPE_COMBINED = 1      ///< ��ϲ��Գֲ�
}XTP_OPT_POSITION_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_ORDER_TYPE��һ������������
/////////////////////////////////////////////////////////////////////////
enum XTP_ORDER_DETAIL_TYPE
{
	XTP_ORDER_DETAIL_TYPE_NEW_ORDER = 0,				///< �¶���
	XTP_ORDER_DETAIL_TYPE_CANCEL_ORDER = 1,				///< �¶�������
	XTP_ORDER_DETAIL_TYPE_OPT_COMB_NEW_ORDER = 2,		///< ��϶���
	XTP_ORDER_DETAIL_TYPE_OPT_COMB_CANCEL_ORDER = 3     ///< ��϶�������
};

/////////////////////////////////////////////////////////////////////////
///TXTPTradeTypeType�ǳɽ���������
/////////////////////////////////////////////////////////////////////////
typedef char TXTPTradeTypeType;

///��ͨ�ɽ�
#define XTP_TRDT_COMMON '0'
///�ֽ����
#define XTP_TRDT_CASH '1'
///һ���г��ɽ�
#define XTP_TRDT_PRIMARY '2'
///���г��ʽ�ɽ�
#define XTP_TRDT_CROSS_MKT_CASH '3'


/////////////////////////////////////////////////////////////////////////
///TXTPOrderTypeType�Ǳ�����������
/////////////////////////////////////////////////////////////////////////
typedef char TXTPOrderTypeType;

///����
#define XTP_ORDT_Normal '0'
///��������
#define XTP_ORDT_DeriveFromQuote '1'
///�������
#define XTP_ORDT_DeriveFromCombination '2'
///��ϱ���
#define XTP_ORDT_Combination '3'
///������
#define XTP_ORDT_ConditionalOrder '4'
///������
#define XTP_ORDT_Swap '5'


//////////////////////////////////////////////////////////////////////////
///@brief XTPTerminalType��һ���ն�����ö�٣�������Ȩϵͳʹ��
//////////////////////////////////////////////////////////////////////////
enum XTPTerminalType
{
	XTP_TERMINAL_PC = 1,            ///<"PC",PC-windows��MacOS
	XTP_TERMINAL_ANDROID,           ///<"MA",Mobile-Android
	XTP_TERMINAL_IOS,               ///<"MI",Mobile-Ios
	XTP_TERMINAL_WP,                ///<"MW",Mobile-Windows Phone
	XTP_TERMINAL_STATION,           ///<"WP",����վ
	XTP_TERMINAL_TEL,               ///<"TO",�绰ί��
	XTP_TERMINAL_PC_LINUX           ///<"OH",PC-linux�������ն�
};

/////////////////////////////////////////////////////////////////////////
///@brief XTP_EXPIRE_DATE_TYPE��һ����Ȩ��ϲ��Ժ�Լ������Ҫ������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_EXPIRE_DATE_TYPE {
	XTP_EXP_DATE_SAME = 0,   ///< ��ͬ������
	XTP_EXP_DATE_DIFF,      ///< ��ͬ������
	XTP_EXP_DATE_NON         ///< �޵�����Ҫ��
}XTP_EXPIRE_DATE_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_UNDERLYING_TYPE��һ����Ȩ��ϲ��Ա��Ҫ������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_UNDERLYING_TYPE {
	XTP_UNDERLYING_SAME = 0,	///<��ͬ���
	XTP_UNDERLYING_DIFF,		///<��ͬ���
	XTP_UNDERLYING_NON			///<�ޱ��Ҫ��
}XTP_UNDERLYING_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_AUTO_SPLIT_TYPE��һ����Ȩ��ϲ����Զ����ö������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_AUTO_SPLIT_TYPE {
	XTP_AUTO_SPLIT_EXPDAY = 0,	///<�������Զ����
	XTP_AUTO_SPLIT_PREDAY,		///<E-1���Զ����
	XTP_AUTO_SPLIT_PRE2DAY,		///<E-2���Զ����
	XTP_AUTO_SPLIT_NON			///<��Чֵ
}XTP_AUTO_SPLIT_TYPE;


///��Ȩ��˳�����ͣ� ��1��ʼ��1��ʾ��Ȩ����ߣ�2��֮�������Ȩ����ͬ������д��ͬ���֣���A��ʾ��Ȩ�۴��ڵ���B��B���ڵ���C�������ƣ�C��D��
typedef char TXTPExerciseSeqType;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_QUALIFICATION_TYPE��һ��֤ȯ�ʵ���ö������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_QUALIFICATION_TYPE
{
	XTP_QUALIFICATION_PUBLIC = 0,			///<����Ͷ���ߣ��ϸ�Ͷ���������Ͷ���߾���
	XTP_QUALIFICATION_COMMON = 1,			///<���ϸ�Ͷ�����빫��Ͷ����
	XTP_QUALIFICATION_ORGANIZATION = 2,		///<���޻���Ͷ����
	XTP_QUALIFICATION_UNKNOWN = 3		///<δ֪����Ȩ�ȿ���Ϊ��������
}XTP_QUALIFICATION_TYPE;

/////////////////////////////////////////////////////////////////////////
///@brief XTP_SECURITY_TYPE��һ��֤ȯ��ϸ����ö������
/////////////////////////////////////////////////////////////////////////
typedef enum XTP_SECURITY_TYPE {
	/// �����Ʊ
	XTP_SECURITY_MAIN_BOARD = 0,
	/// ��С���Ʊ
	XTP_SECURITY_SECOND_BOARD,
	/// ��ҵ���Ʊ
	XTP_SECURITY_STARTUP_BOARD,
	/// ָ��
	XTP_SECURITY_INDEX,
	/// �ƴ����Ʊ(�Ϻ�)
	XTP_SECURITY_TECH_BOARD = 4,
	/// ��ծ
	XTP_SECURITY_STATE_BOND = 5,
	/// ��ҵծ
	XTP_SECURITY_ENTERPRICE_BOND = 6,
	/// ��˾ծ
	XTP_SECURITY_COMPANEY_BOND = 7,
	/// ת��ծȯ
	XTP_SECURITY_CONVERTABLE_BOND = 8,
	/// ��ծ��ع�
	XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO = 12,
	/// ���г���Ʊ ETF
	XTP_SECURITY_ETF_SINGLE_MARKET_STOCK = 14,
	/// ���г���Ʊ ETF
	XTP_SECURITY_ETF_INTER_MARKET_STOCK,
	/// ���г�ʵ��ծȯ ETF
	XTP_SECURITY_ETF_SINGLE_MARKET_BOND = 17,
	/// �ƽ� ETF
	XTP_SECURITY_ETF_GOLD = 19,
	/// �ּ������ӻ���
	XTP_SECURITY_STRUCTURED_FUND_CHILD = 24,
	/// ������������
	XTP_SECURITY_SZSE_RECREATION_FUND = 26,
	/// ������Ȩ
	XTP_SECURITY_STOCK_OPTION = 29,
	/// ETF��Ȩ
	XTP_SECURITY_ETF_OPTION = 30,
	/// ���
	XTP_SECURITY_ALLOTMENT = 100,

	/// �Ͻ��������ͻ��һ���
	XTP_SECURITY_MONETARY_FUND_SHCR = 110,
	/// �Ͻ��������ͻ��һ���
	XTP_SECURITY_MONETARY_FUND_SHTR = 111,
	/// ������һ���
	XTP_SECURITY_MONETARY_FUND_SZ = 112,

	/// ����
	XTP_SECURITY_OTHERS = 255
}XTP_SECURITY_TYPE;

#pragma pack()

#endif
