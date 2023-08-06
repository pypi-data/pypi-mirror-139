/////////////////////////////////////////////////////////////////////////
///@author ��̩֤ȯ�ɷ����޹�˾
///@file xquote_api_struct.h
///@brief ����������������ݽṹ
/////////////////////////////////////////////////////////////////////////
#ifndef _XQUOTE_API_STRUCT_H_
#define _XQUOTE_API_STRUCT_H_

#include <stdint.h>
#include "xtp_api_data_type.h"

#pragma pack(8)

///ָ���ĺ�Լ
typedef struct XTPSpecificTickerStruct
{
    ///����������
    XTP_EXCHANGE_TYPE exchange_id;
    ///��Լ���루��������������Ϣ������"600000"�������ո���'\0'��β
	char	ticker[XTP_TICKER_LEN];
} XTPST;

///��Ʊ������ծȯ�ȶ�������
struct XTPMarketDataStockExData {
    ///ί����������(SH,SZ)
    int64_t total_bid_qty;
    ///ί����������(SH,SZ)
    int64_t total_ask_qty;
    ///��Ȩƽ��ί��۸�(SH,SZ)
    double ma_bid_price;
    ///��Ȩƽ��ί���۸�(SH,SZ)
    double ma_ask_price;
    ///ծȯ��Ȩƽ��ί��۸�(SH)
    double ma_bond_bid_price;
    ///ծȯ��Ȩƽ��ί���۸�(SH)
    double ma_bond_ask_price;
    ///ծȯ����������(SH)
    double yield_to_maturity;
    ///����ʵʱ�ο���ֵ(SH,SZ)
    double iopv;
    ///ETF�깺����(SH)
    int32_t etf_buy_count;
    ///ETF��ر���(SH)
    int32_t etf_sell_count;
    ///ETF�깺����(SH)
    double etf_buy_qty;
    ///ETF�깺���(SH)
    double etf_buy_money;
    ///ETF�������(SH)
    double etf_sell_qty;
    ///ETF��ؽ��(SH)
    double etf_sell_money;
    ///Ȩִ֤�е�������(SH)
    double total_warrant_exec_qty;
    ///Ȩ֤��ͣ�۸�Ԫ��(SH)
    double warrant_lower_price;
    ///Ȩ֤��ͣ�۸�Ԫ��(SH)
    double warrant_upper_price;
    ///���볷������(SH)
    int32_t cancel_buy_count;
    ///������������(SH)
    int32_t cancel_sell_count;
    ///���볷������(SH)
    double cancel_buy_qty;
    ///������������(SH)
    double cancel_sell_qty;
    ///���볷�����(SH)
    double cancel_buy_money;
    ///�����������(SH)
    double cancel_sell_money;
    ///�����ܱ���(SH)
    int64_t total_buy_count;
    ///�����ܱ���(SH)
    int64_t total_sell_count;
    ///����ί�гɽ����ȴ�ʱ��(SH)
    int32_t duration_after_buy;
    ///����ί�гɽ����ȴ�ʱ��(SH)
    int32_t duration_after_sell;
    ///��ί�м�λ��(SH)
    int32_t num_bid_orders;
    ///����ί�м�λ��(SH)
    int32_t num_ask_orders;

    ///����T-1�վ�ֵ(SZ)
    double pre_iopv;
    ///Ԥ��
    int64_t r1;
    ///Ԥ��
    int64_t r2;
};

/// ��Ȩ��������
struct XTPMarketDataOptionExData {
    ///�������жϲο���(SH)
    double  auction_price;
    ///�������жϼ��Ͼ�������ƥ����(SH)
    int64_t auction_qty;
    ///���ѯ��ʱ��(SH)
    int64_t last_enquiry_time;
};

/////////////////////////////////////////////////////////////////////////
///@brief XTP_MARKETDATA_TYPE�����������������
/////////////////////////////////////////////////////////////////////////
enum XTP_MARKETDATA_TYPE {
    XTP_MARKETDATA_ACTUAL = 0, // �ֻ�(��Ʊ/����/ծȯ��)
    XTP_MARKETDATA_OPTION = 1, // ��Ȩ
};

///����
typedef struct XTPMarketDataStruct
{
    // ����
    ///����������
    XTP_EXCHANGE_TYPE exchange_id;
    ///��Լ���루��������������Ϣ���������ո���'\0'��β
    char	ticker[XTP_TICKER_LEN];

    // �۸�
	///���¼�
	double	last_price;
	///������
	double	pre_close_price;
	///����
	double	open_price;
	///��߼�
	double	high_price;
	///��ͼ�
	double	low_price;
    ///������
    double	close_price;

    // ��Ȩ����
    ///���ճֲ���(��)(Ŀǰδ��д)
    int64_t pre_total_long_positon;
    ///�ֲ���(��)
	int64_t	total_long_positon;
    ///���ս����
    double	pre_settl_price;
    ///���ս����
	double	settl_price;

	// �ǵ�ͣ
	///��ͣ��
	double	upper_limit_price;
	///��ͣ��
	double	lower_limit_price;
	///Ԥ��
	double	pre_delta;
	///Ԥ��
	double	curr_delta;

    /// ʱ���࣬��ʽΪYYYYMMDDHHMMSSsss
    int64_t data_time;

    // ��������
    ///������Ϊ�ܳɽ�������λ�ɣ��뽻����һ�£�
    int64_t	qty;
    ///�ɽ���Ϊ�ܳɽ�����λԪ���뽻����һ�£�
    double	turnover;
    ///���վ���=(turnover/qty)
    double	avg_price;

    // ������
    ///ʮ�������
    double bid[10];
    ///ʮ��������
    double	ask[10];
    ///ʮ��������
    int64_t	bid_qty[10];
    ///ʮ��������
    int64_t	ask_qty[10];

    // ��������
    ///�ɽ�����
    int64_t trades_count;
    ///��ǰ����״̬˵�������ġ�XTP API��������.doc���ĵ�
    char ticker_status[8];
    ///����
    union {
        XTPMarketDataStockExData  stk;
        XTPMarketDataOptionExData opt;
    };
    ///������union��������������
    XTP_MARKETDATA_TYPE data_type;
    ///Ԥ��
    int32_t r4;
} XTPMD;


///��Ʊ���龲̬��Ϣ
typedef struct XTPQuoteStaticInfo {
    ///����������
    XTP_EXCHANGE_TYPE exchange_id;
    ///��Լ���루��������������Ϣ���������ո���'\0'��β
    char    ticker[XTP_TICKER_LEN];
    /// ��Լ����
    char    ticker_name[XTP_TICKER_NAME_LEN];
    /// ��Լ����
	XTP_TICKER_TYPE ticker_type;
    ///������
    double  pre_close_price;
    ///��ͣ���
    double  upper_limit_price;
    ///��ͣ���
    double  lower_limit_price;
	///��С�䶯��λ
	double  price_tick;
    /// ��Լ��С������(��)
    int32_t  buy_qty_unit;
    /// ��Լ��С������(��)
	int32_t sell_qty_unit;
} XTPQSI;


///������
typedef struct OrderBookStruct {
    ///����������
    XTP_EXCHANGE_TYPE exchange_id;
    ///��Լ���루��������������Ϣ���������ո���'\0'��β
    char    ticker[XTP_TICKER_LEN];

    ///���¼�
    double last_price;
    ///������Ϊ�ܳɽ���
    int64_t qty;
    ///�ɽ���Ϊ�ܳɽ����
    double  turnover;
    ///�ɽ�����
    int64_t trades_count;

    // ������
    ///ʮ�������
    double bid[10];
    ///ʮ��������
    double  ask[10];
    ///ʮ��������
    int64_t bid_qty[10];
    ///ʮ��������
    int64_t ask_qty[10];
    /// ʱ����
    int64_t data_time;
} XTPOB;

////////////////////////////////// �������


///���ί��(���������)
struct XTPTickByTickEntrust {
    ///Ƶ������
    int32_t channel_no;
    ///ί�����(��ͬһ��channel_no��Ψһ����1��ʼ����)
    int64_t seq;
    ///ί�м۸�
    double  price;
    ///ί������
    int64_t qty;
    ///'1':��; '2':��; 'G':����; 'F':����
    char  side;
    ///�������: '1': �м�; '2': �޼�; 'U': ��������
    char ord_type;
};

///��ʳɽ�
struct XTPTickByTickTrade {
    ///Ƶ������
    int32_t channel_no;
    ///ί�����(��ͬһ��channel_no��Ψһ����1��ʼ����)
    int64_t seq;
    ///�ɽ��۸�
    double price;
    ///�ɽ���
    int64_t qty;
    ///�ɽ����(�������Ͻ���)
    double money;
    ///�򷽶�����
    int64_t bid_no;
    ///����������
    int64_t ask_no;
    /// SH: �����̱�ʶ('B':������; 'S':������; 'N':δ֪)
    /// SZ: �ɽ���ʶ('4':��; 'F':�ɽ�)
    char trade_flag;
};

///���������Ϣ
typedef struct XTPTickByTickStruct {
    ///����������
    XTP_EXCHANGE_TYPE exchange_id;
    ///��Լ���루��������������Ϣ���������ո���'\0'��β
    char ticker[XTP_TICKER_LEN];
    ///Ԥ��
    int64_t seq;
    ///ί��ʱ�� or �ɽ�ʱ��
    int64_t data_time;
    ///ί�� or �ɽ�
    XTP_TBT_TYPE type;

    union {
        XTPTickByTickEntrust entrust;
        XTPTickByTickTrade     trade;
    };
} XTPTBT;


///����ѯ��������Ϣ
typedef struct XTPTickerPriceInfo {
    ///����������
    XTP_EXCHANGE_TYPE exchange_id;
    ///��Լ���루��������������Ϣ���������ո���'\0'��β
    char ticker[XTP_TICKER_LEN];
    ///���¼�
    double last_price;
} XTPTPI;

///��Ʊ����ȫ����̬��Ϣ
typedef struct XTPQuoteFullInfo {
	XTP_EXCHANGE_TYPE  exchange_id;							///<����������
	char               ticker[XTP_TICKER_LEN];				///<֤ȯ����
	char               ticker_name[XTP_TICKER_NAME_LEN];	///<֤ȯ����
	XTP_SECURITY_TYPE      security_type;					///<��Լ��ϸ����
	XTP_QUALIFICATION_TYPE ticker_qualification_class;		///<��Լ�ʵ������
	bool is_registration;									///<�Ƿ�ע����(�����ô�ҵ���Ʊ��������ҵ��Ʊ������ƾ֤)
	bool is_VIE;											///<�Ƿ����Э����Ƽܹ�(�����ô�ҵ���Ʊ��������ҵ��Ʊ������ƾ֤)
	bool is_noprofit;										///<�Ƿ���δӯ��(�����ô�ҵ���Ʊ��������ҵ��Ʊ������ƾ֤)
	bool is_weighted_voting_rights;							///<�Ƿ����ͶƱȨ����(�����ô�ҵ���Ʊ��������ҵ��Ʊ������ƾ֤)
	bool is_have_price_limit;								///<�Ƿ����ǵ�������(ע�����ṩ������ȣ���ͨ���ǵ�ͣ�ۺ����ռ����������)
	double upper_limit_price;								///<��ͣ�ۣ��������ǵ�������ʱ��Ч��
	double lower_limit_price;								///<��ͣ�ۣ��������ǵ�������ʱ��Ч��
	double pre_close_price;									///<���ռ�
	double price_tick;										///<�۸���С�䶯��λ
	int32_t bid_qty_upper_limit;							///<�޼���ί����������
	int32_t bid_qty_lower_limit;							///<�޼���ί����������
	int32_t bid_qty_unit;									///<�޼���������λ
	int32_t ask_qty_upper_limit;							///<�޼���ί����������
	int32_t ask_qty_lower_limit;							///<�޼���ί����������
	int32_t ask_qty_unit;									///<�޼���������λ
	int32_t market_bid_qty_upper_limit;						///<�м���ί����������
	int32_t market_bid_qty_lower_limit;						///<�м���ί����������
	int32_t market_bid_qty_unit;							///<�м���������λ
	int32_t market_ask_qty_upper_limit;						///<�м���ί����������
	int32_t market_ask_qty_lower_limit;						///<�м���ί����������
	int32_t market_ask_qty_unit;							///<�м���������λ
	uint64_t unknown[4];									///<�����ֶ�
}XTPQFI;

#pragma pack()

#endif
