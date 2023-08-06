/////////////////////////////////////////////////////////////////////////
///@author ��̩֤ȯ�ɷ����޹�˾
///@file xoms_api_struct.h
///@brief ���彻����������ݽṹ
/////////////////////////////////////////////////////////////////////////
#ifndef _XOMS_API_STRUCT_H_
#define _XOMS_API_STRUCT_H_

#include "xtp_api_data_type.h"
#include "stddef.h"
#include "xtp_api_struct_common.h"

#pragma pack(8)

//=====================�ͻ��˽ӿڶ���=================================
///�¶�������
struct XTPOrderInsertInfo
{
    ///XTPϵͳ����ID�������û���д����XTPϵͳ��Ψһ
    uint64_t                order_xtp_id;
    ///�������ã��ɿͻ��Զ���
    uint32_t	            order_client_id;
    ///��Լ���� �ͻ������󲻴��ո���'\0'��β
    char                    ticker[XTP_TICKER_LEN];
    ///�����г�
    XTP_MARKET_TYPE         market;
    ///�۸�
    double                  price;
    ///ֹ��ۣ������ֶΣ�
    double                  stop_price;
    ///����(��Ʊ��λΪ�ɣ���ع���λΪ��)
    int64_t                 quantity;
    ///�����۸�
    XTP_PRICE_TYPE          price_type;
    union{
		///32λ�ֶΣ����������ϰ汾api���û��������
        uint32_t            u32;
        struct {
            ///��������
            XTP_SIDE_TYPE               side;
            ///��ƽ��־
            XTP_POSITION_EFFECT_TYPE    position_effect;
			///Ԥ���ֶ�1
            uint8_t                     reserved1;
			///Ԥ���ֶ�2
			uint8_t                     reserved2;
        };
    };
	///ҵ������
	XTP_BUSINESS_TYPE       business_type;
 };


///����ʧ����Ӧ��Ϣ
struct XTPOrderCancelInfo
{
    ///����XTPID
    uint64_t                 order_cancel_xtp_id;
    ///ԭʼ����XTPID
    uint64_t                 order_xtp_id;
};


///������Ӧ�ṹ��
struct XTPOrderInfo
{
    ///XTPϵͳ����ID����XTPϵͳ��Ψһ
	uint64_t                order_xtp_id;
	///�������ã��û��Զ���
	uint32_t	            order_client_id;
    ///�����������ã��û��Զ��壨��δʹ�ã�
    uint32_t                order_cancel_client_id;
    ///������XTPϵͳ�е�id����XTPϵͳ��Ψһ
    uint64_t                order_cancel_xtp_id;
	///��Լ����
	char                    ticker[XTP_TICKER_LEN];
	///�����г�
	XTP_MARKET_TYPE         market;
	///�۸�
	double                  price;
	///�������˶����ı�������
	int64_t                 quantity;
	///�����۸�����
	XTP_PRICE_TYPE          price_type;
    union{
		///32λ�ֶΣ����������ϰ汾api���û��������
        uint32_t            u32;
        struct {
            ///��������
            XTP_SIDE_TYPE               side;
            ///��ƽ��־����Ȩ�û���ע�ֶΣ������û���0����
            XTP_POSITION_EFFECT_TYPE    position_effect;
			///Ԥ���ֶ�1
			uint8_t                     reserved1;
			///Ԥ���ֶ�2
			uint8_t                     reserved2;
        };
    };
	///ҵ������
	XTP_BUSINESS_TYPE       business_type;
	///��ɽ�������Ϊ�˶����ۼƳɽ�����
	int64_t                 qty_traded;
	///ʣ���������������ɹ�ʱ����ʾ��������
	int64_t                 qty_left;
	///ί��ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
	int64_t                 insert_time;
	///����޸�ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
	int64_t                 update_time;
	///����ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
	int64_t                 cancel_time;
	///�ɽ���Ϊ�˶����ĳɽ��ܽ��
	double                  trade_amount;
	///���ر������ OMS���ɵĵ��ţ�����ͬ��order_xtp_id��Ϊ�������������̵ĵ���
	char                    order_local_id[XTP_LOCAL_ORDER_LEN];
	///����״̬��������Ӧ��û�в��ֳɽ�״̬�����ͣ��ڲ�ѯ��������У����в��ֳɽ�״̬
	XTP_ORDER_STATUS_TYPE   order_status;
	///�����ύ״̬��OMS�ڲ�ʹ�ã��û����ô��ֶ������ֳ����ͱ���
	XTP_ORDER_SUBMIT_STATUS_TYPE   order_submit_status;
	///��������
	TXTPOrderTypeType       order_type;
};



///�����ɽ��ṹ��
struct XTPTradeReport
{
    ///XTPϵͳ����ID���˳ɽ��ر���صĶ���ID����XTPϵͳ��Ψһ
    uint64_t                 order_xtp_id;
    ///��������
    uint32_t                 order_client_id;
    ///��Լ����
    char                     ticker[XTP_TICKER_LEN];
    ///�����г�
    XTP_MARKET_TYPE          market;
    ///�����ţ�����XTPID�󣬸��ֶ�ʵ�ʺ�order_xtp_id�ظ����ӿ�����ʱ������
    uint64_t                 local_order_id;
    ///�ɽ���ţ����Ψһ���Ͻ���ÿ�ʽ���Ψһ��������2�ʳɽ��ر�ӵ����ͬ��exec_id���������Ϊ�˱ʽ����Գɽ�
    char                     exec_id[XTP_EXEC_ID_LEN];
    ///�۸񣬴˴γɽ��ļ۸�
    double                   price;
    ///�������˴γɽ��������������ۼ�����
    int64_t                  quantity;
    ///�ɽ�ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
    int64_t                  trade_time;
    ///�ɽ����˴γɽ����ܽ�� = price*quantity
    double                   trade_amount;
    ///�ɽ���� --�ر���¼�ţ����ڵ����˻���˵�����ÿ��ƽ̨����ͬ����Ʒ�֣�Ψһ���Ͻ���Ψһ�����ڶ��˻���˵����Ψһ
    uint64_t                 report_index;
    ///������� --���������ţ��Ͻ���Ϊ�գ�����д��ֶ�
    char                     order_exch_id[XTP_ORDER_EXCH_LEN];
    ///�ɽ�����  --�ɽ��ر��е�ִ������
    TXTPTradeTypeType        trade_type;
    union{
		///32λ�ֶΣ����������ϰ汾api���û��������
        uint32_t            u32;
        struct {
            ///��������
            XTP_SIDE_TYPE               side;
            ///��ƽ��־
            XTP_POSITION_EFFECT_TYPE    position_effect;
			///Ԥ���ֶ�1
			uint8_t                     reserved1;
			///Ԥ���ֶ�2
			uint8_t                     reserved2;
        };
    };
	///ҵ������
	XTP_BUSINESS_TYPE        business_type;
    ///����������Ա���� 
    char                     branch_pbu[XTP_BRANCH_PBU_LEN];
};


//////////////////////////////////////////////////////////////////////////
///������ѯ
//////////////////////////////////////////////////////////////////////////
///������ѯ����-������ѯ
struct XTPQueryOrderReq
{
    ///֤ȯ���룬����Ϊ�գ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����гɽ��ر�
    char      ticker[XTP_TICKER_LEN];
    ///��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0��
    int64_t   begin_time;
    ///��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
    int64_t   end_time;  
};

///������ѯ��Ӧ�ṹ��
typedef struct XTPOrderInfo XTPQueryOrderRsp;


///��ѯ��������-��ҳ��ѯ
struct XTPQueryOrderByPageReq
{
	///��Ҫ��ѯ�Ķ�������
    int64_t         req_count;
	///��һ���յ��Ĳ�ѯ��������д�����������������Ǵ�ͷ��ѯ������0
    int64_t         reference;
	///�����ֶ�
    int64_t         reserved;
};

//////////////////////////////////////////////////////////////////////////
///�ɽ��ر���ѯ
//////////////////////////////////////////////////////////////////////////
///��ѯ�ɽ���������-����ִ�б�Ų�ѯ�������ֶΣ�
struct XTPQueryReportByExecIdReq
{
    ///XTP����ϵͳID
    uint64_t  order_xtp_id;  
    ///�ɽ�ִ�б��
    char  exec_id[XTP_EXEC_ID_LEN];
};

///��ѯ�ɽ��ر�����-��ѯ����
struct XTPQueryTraderReq
{
    ///֤ȯ���룬����Ϊ�գ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����гɽ��ر�
    char      ticker[XTP_TICKER_LEN];
    ///��ʼʱ�䣬��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0��
    int64_t   begin_time; 
    ///����ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
    int64_t   end_time;  
};

///�ɽ��ر���ѯ��Ӧ�ṹ��
typedef struct XTPTradeReport  XTPQueryTradeRsp;

///��ѯ�ɽ��ر�����-��ҳ��ѯ
struct XTPQueryTraderByPageReq
{
	///��Ҫ��ѯ�ĳɽ��ر�����
	int64_t         req_count;
	///��һ���յ��Ĳ�ѯ�ɽ��ر�����д�����������������Ǵ�ͷ��ѯ������0
	int64_t         reference;
	///�����ֶ�
	int64_t         reserved;
};

//////////////////////////////////////////////////////////////////////////
///�˻��ʽ��ѯ��Ӧ�ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryAssetRsp
{
    ///���ʲ����ֻ��˻�/��Ȩ�˻��ο���ʽ�����ʲ� = �����ʽ� + ֤ȯ�ʲ���ĿǰΪ0��+ Ԥ�۵��ʽ𣩣��������˻��ο���ʽ�����ʲ� = �����ʽ� + ��ȯ���������ʽ���� + ֤ȯ�ʲ�+ Ԥ�۵��ʽ�
    double total_asset;
    ///�����ʽ�
    double buying_power;
    ///֤ȯ�ʲ��������ֶΣ�ĿǰΪ0��
    double security_asset;
    ///�ۼ�����ɽ�֤ȯռ���ʽ𣨽����ֻ��˻�/��Ȩ�˻��������˻��ݲ����ã�
    double fund_buy_amount;
    ///�ۼ�����ɽ����׷��ã������ֻ��˻�/��Ȩ�˻��������˻��ݲ����ã�
    double fund_buy_fee;
    ///�ۼ������ɽ�֤ȯ�����ʽ𣨽����ֻ��˻�/��Ȩ�˻��������˻��ݲ����ã�
    double fund_sell_amount;
    ///�ۼ������ɽ����׷��ã������ֻ��˻�/��Ȩ�˻��������˻��ݲ����ã�
    double fund_sell_fee;
    ///XTPϵͳԤ�۵��ʽ𣨰���������ƱʱԤ�۵Ľ����ʽ�+Ԥ�������ѣ�
    double withholding_amount;
    ///�˻�����
    XTP_ACCOUNT_TYPE account_type;

    ///����ı�֤�𣨽�����Ȩ�˻���
    double frozen_margin;
    ///��Ȩ�����ʽ𣨽�����Ȩ�˻���
    double frozen_exec_cash;
    ///��Ȩ���ã�������Ȩ�˻���
    double frozen_exec_fee;
    ///�渶�ʽ𣨽�����Ȩ�˻���
    double pay_later;
    ///Ԥ�渶�ʽ𣨽�����Ȩ�˻���
    double preadva_pay;
    ///������������Ȩ�˻���
    double orig_banlance;
    ///��ǰ��������Ȩ�˻���
    double banlance;
    ///�������𣨽�����Ȩ�˻���
    double deposit_withdraw;
    ///���ս����ʽ����������Ȩ�˻���
    double trade_netting;
    ///�ʽ��ʲ���������Ȩ�˻���
    double captial_asset;

    ///ǿ���ʽ𣨽�����Ȩ�˻���
    double force_freeze_amount;
    ///��ȡ�ʽ𣨽�����Ȩ�˻���
    double preferred_amount;

    // ����ҵ�������ֶο�ʼ������1��
    ///��ȯ���������ʽ������������˻���ֻ��������ȯ��ȯ��
    double repay_stock_aval_banlance;

    // ����ҵ�������ֶν���������1��

    ///�ۼƶ���������
    double fund_order_data_charges;
    ///�ۼƳ���������
    double fund_cancel_data_charges;
    //������ͳ�������ֶν���������2��

    ///(�����ֶ�)
    uint64_t unknown[43 - 12 - 1 - 2];
};

//////////////////////////////////////////////////////////////////////////
///��ѯ��Ʊ�ֲ��������ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryStkPositionReq
{
    ///֤ȯ����
    char                ticker[XTP_TICKER_LEN];
    ///�����г�
    XTP_MARKET_TYPE     market;
};

//////////////////////////////////////////////////////////////////////////
///��ѯ��Ʊ�ֲ����
//////////////////////////////////////////////////////////////////////////
struct XTPQueryStkPositionRsp
{
    ///֤ȯ����
    char                ticker[XTP_TICKER_LEN];
    ///֤ȯ����
    char                ticker_name[XTP_TICKER_NAME_LEN];
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///�ֲܳ�
    int64_t             total_qty;
    ///�����ֲ�
    int64_t				sellable_qty;
    ///�ֲֳɱ�
    double              avg_price;
    ///����ӯ���������ֶΣ�
    double              unrealized_pnl;
    ///���ճֲ�
    int64_t             yesterday_position;
    ///�����깺����������깺���������������ͬʱ���ڣ���˿��Թ���һ���ֶΣ�
    int64_t				purchase_redeemable_qty;

	//����Ϊ��Ȩ�û������ֶ�
    /// �ֲַ���
	XTP_POSITION_DIRECTION_TYPE      position_direction;
	///�����ֶ�1
	uint32_t			reserved1;
    /// ����Ȩ��Լ
    int64_t             executable_option;
    /// ���������
    int64_t             lockable_position;
    /// ����Ȩ���
    int64_t             executable_underlying;
    /// ���������
    int64_t             locked_position;
    /// �������������
    int64_t             usable_locked_position;

	//����Ϊ�ֻ��û������ֶ�
    ///ӯ���ɱ���
    double             profit_price;
    ///����ɱ�
    double             buy_cost;
    ///ӯ���ɱ�
    double             profit_cost;

    ///(�����ֶ�)
    uint64_t unknown[50 - 9];
};

/////////////////////////////////////////////////////////////////////////
///�û�չ�������֪ͨ
/////////////////////////////////////////////////////////////////////////
struct XTPCreditDebtExtendNotice
{
	uint64_t	xtpid;								///<XTPϵͳ����ID�������û���д����XTPϵͳ��Ψһ
	char		debt_id[XTP_CREDIT_DEBT_ID_LEN];	///<��ծ��Լ���
	XTP_DEBT_EXTEND_OPER_STATUS		oper_status;	///<չ���������״̬
	uint64_t	oper_time;							///<����ʱ��
};

/////////////////////////////////////////////////////////////////////////
///�ʽ���ת��ˮ֪ͨ
/////////////////////////////////////////////////////////////////////////
struct XTPFundTransferNotice
{
    ///�ʽ���ת���
    uint64_t	            serial_id;
    ///��ת����
    XTP_FUND_TRANSFER_TYPE	transfer_type;
    ///���
    double	                amount;
    ///������� 
    XTP_FUND_OPER_STATUS    oper_status;
    ///����ʱ��
    uint64_t	            transfer_time;
};



/////////////////////////////////////////////////////////////////////////
///�ʽ���ת��ˮ��ѯ��������Ӧ
/////////////////////////////////////////////////////////////////////////
struct XTPQueryFundTransferLogReq {
    ///�ʽ���ת���
    uint64_t	serial_id;

};

/////////////////////////////////////////////////////////////////////////
///�ʽ���ת��ˮ��¼�ṹ��
/////////////////////////////////////////////////////////////////////////
typedef struct XTPFundTransferNotice XTPFundTransferLog;

//////////////////////////////////////////////////////////////////////////
///��ѯ�ּ�������Ϣ�ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryStructuredFundInfoReq
{
	XTP_EXCHANGE_TYPE   exchange_id;  ///<���������룬����Ϊ��
	char                sf_ticker[XTP_TICKER_LEN];   ///<�ּ�����ĸ������룬����Ϊ�գ����Ϊ�գ���Ĭ�ϲ�ѯ���еķּ�����
};

//////////////////////////////////////////////////////////////////////////
///��ѯ�ּ�������Ϣ��Ӧ�ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPStructuredFundInfo
{
    XTP_EXCHANGE_TYPE   exchange_id;  ///<����������
	char                sf_ticker[XTP_TICKER_LEN];   ///<�ּ�����ĸ�������
	char                sf_ticker_name[XTP_TICKER_NAME_LEN]; ///<�ּ�����ĸ��������
    char                ticker[XTP_TICKER_LEN];   ///<�ּ������ӻ������
    char                ticker_name[XTP_TICKER_NAME_LEN]; ///<�ּ������ӻ�������
	XTP_SPLIT_MERGE_STATUS	split_merge_status;   ///<���������ֺϲ�״̬
    uint32_t            ratio; ///<��ֺϲ�����
    uint32_t            min_split_qty;///<��С�������
    uint32_t            min_merge_qty; ///<��С�ϲ�����
    double              net_price;///<����ֵ
};


//////////////////////////////////////////////////////////////////////////
///��ѯ��ƱETF��Լ�������--����ṹ��,
///�������Ϊ����������:1,�����򷵻������г���ETF��Լ��Ϣ��
///                  2,ֻ��дmarket,���ظý����г��½��
///                   3,��дmarket��ticker����,ֻ���ظ�etf��Ϣ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryETFBaseReq
{
    ///�����г�
    XTP_MARKET_TYPE    market;
    ///ETF��������
    char               ticker[XTP_TICKER_LEN];
};

//////////////////////////////////////////////////////////////////////////
///��ѯ��ƱETF��Լ�������--��Ӧ�ṹ��
//////////////////////////////////////////////////////////////////////////
typedef struct XTPQueryETFBaseRsp
{
    XTP_MARKET_TYPE     market;                             ///<�����г�
    char                etf[XTP_TICKER_LEN];                ///<etf����,����,����ͳһʹ�øô���
    char                subscribe_redemption_ticker[XTP_TICKER_LEN];    ///<etf�깺��ش���
    int32_t             unit;                               ///<��С�깺��ص�λ��Ӧ��ETF����,������֤"50ETF"����900000
    int32_t             subscribe_status;                   ///<�Ƿ������깺,1-����,0-��ֹ
    int32_t             redemption_status;                  ///<�Ƿ��������,1-����,0-��ֹ
    double              max_cash_ratio;                     ///<����ֽ��������,С��1����ֵ   TODO �Ƿ����double
    double              estimate_amount;                    ///<T��Ԥ�������
    double              cash_component;                     ///<T-X���ֽ���
    double              net_value;                          ///<����λ��ֵ
    double              total_amount;                       ///<��С���굥λ��ֵ�ܽ��=net_value*unit
}XTPQueryETFBaseRsp;



//////////////////////////////////////////////////////////////////////////
///��ѯ��ƱETF��Լ�ɷֹ���Ϣ--����ṹ��,�������Ϊ:�����г�+ETF��������
//////////////////////////////////////////////////////////////////////////
typedef struct XTPQueryETFComponentReq
{
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///ETF��������
    char                ticker[XTP_TICKER_LEN];
}XTPQueryETFComponentReq;


//////////////////////////////////////////////////////////////////////////
///��ѯ��ƱETF�ɷֹ���Ϣ--��Ӧ�ṹ�壬�ɰ汾��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryETFComponentRspV1
{
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///ETF����
    char                ticker[XTP_TICKER_LEN];
    ///�ɷݹɴ���
    char                component_ticker[XTP_TICKER_LEN];
    ///�ɷݹ�����
    char                component_name[XTP_TICKER_NAME_LEN];
    ///�ɷݹ�����
    int64_t             quantity;
    ///�ɷݹɽ����г�
    XTP_MARKET_TYPE     component_market;
    ///�ɷݹ������ʶ
    ETF_REPLACE_TYPE    replace_type;
    ///��۱���
    double              premium_ratio;
    ///�ɷֹ������ʶΪ�����ֽ����ʱ����ܽ��
    double              amount;

};

//////////////////////////////////////////////////////////////////////////
///��ѯ��ƱETF�ɷֹ���Ϣ--��Ӧ�ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryETFComponentRsp
{
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///ETF����
    char                ticker[XTP_TICKER_LEN];
    ///�ɷݹɴ���
    char                component_ticker[XTP_TICKER_LEN];
    ///�ɷݹ�����
    char                component_name[XTP_TICKER_NAME_LEN];
    ///�ɷݹ�����
    int64_t             quantity;
    ///�ɷݹɽ����г�
    XTP_MARKET_TYPE     component_market;
    ///�ɷݹ������ʶ
    ETF_REPLACE_TYPE    replace_type;
    ///��۱���
    double              premium_ratio;
    ///�ɷֹ������ʶΪ�����ֽ����ʱ����ܽ��
    double              amount;
    ///�깺��۱���
    double              creation_premium_ratio;
    ///�����۱���
    double              redemption_discount_ratio;
    ///�깺ʱ���ɷֹ������ʶΪ�����ֽ����ʱ����ܽ��
    double              creation_amount;
    ///���ʱ���ɷֹ������ʶΪ�����ֽ����ʱ����ܽ��
    double              redemption_amount;

};

//////////////////////////////////////////////////////////////////////////
///��ѯ���տ��깺�¹���Ϣ
//////////////////////////////////////////////////////////////////////////
struct XTPQueryIPOTickerRsp {
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///�깺����
    char                ticker[XTP_TICKER_LEN];
    ///�깺��Ʊ����
    char                ticker_name[XTP_TICKER_NAME_LEN]; 
    /// ֤ȯ���
    XTP_TICKER_TYPE     ticker_type;
    ///�깺�۸�
    double              price;
    ///�깺��Ԫ         
    int32_t             unit;
    ///��������깺����
    int32_t             qty_upper_limit;
};



//////////////////////////////////////////////////////////////////////////
///��ѯ�û��깺���-�ɰ�
//////////////////////////////////////////////////////////////////////////
struct XTPQueryIPOQuotaRspV1 {
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///���깺���
    int32_t             quantity;
};


//////////////////////////////////////////////////////////////////////////
///��ѯ�û��깺���-������ҵ����
//////////////////////////////////////////////////////////////////////////
struct XTPQueryIPOQuotaRsp {
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///���깺���
    int32_t             quantity;
    /// �Ϻ��ƴ�����
    int32_t             tech_quantity;
    /// ����
    int32_t             unused;
};

//////////////////////////////////////////////////////////////////////////
///�걨�û���ip��mac����Ϣ��������Ȩ�û�ʹ��
//////////////////////////////////////////////////////////////////////////
struct XTPUserTerminalInfoReq {
	char  local_ip[XTP_INET_ADDRESS_STR_LEN];			///<����IP��ַ
	char  mac_addr[XTP_MAC_ADDRESS_LEN];				///<MAC��ַ
	char  hd[XTP_HARDDISK_SN_LEN];						///<Ӳ�����к�
	XTPTerminalType term_type;							///<�ն�����
	char  internet_ip[XTP_INET_ADDRESS_STR_LEN];		///<����IP��ַ
	int32_t internet_port;								///<�����˿ں�
	XTPVersionType  client_version;						///<�ͻ��˰汾��
	char  macos_sno[XTP_MACOS_SNO_LEN];					///<MacOSϵͳ�����кţ���ΪMacOSϵͳ��Ҫ��д
	char  unused[27];									///<Ԥ��
};

//////////////////////////////////////////////////////////////////////////
///��ѯ��Ȩ���۽���ҵ��ο���Ϣ--����ṹ��,�������Ϊ:�����г�+8λ��Ȩ����
//////////////////////////////////////////////////////////////////////////
struct XTPQueryOptionAuctionInfoReq {
    ///�����г�
    XTP_MARKET_TYPE     market;
    ///8λ��Ȩ��Լ����
    char                ticker[XTP_TICKER_LEN];
};

//////////////////////////////////////////////////////////////////////////
///��ѯ��Ȩ���۽���ҵ��ο���Ϣ
//////////////////////////////////////////////////////////////////////////
struct XTPQueryOptionAuctionInfoRsp {
    char                ticker[XTP_TICKER_LEN];             ///<��Լ���룬����ticker���ñ��ֶ�
    XTP_MARKET_TYPE     security_id_source;                 ///<֤ȯ����Դ
    char                symbol[XTP_TICKER_NAME_LEN];        ///<��Լ���
    char                contract_id[XTP_TICKER_NAME_LEN];   ///<��Լ���״���
    char                underlying_security_id[XTP_TICKER_LEN]; ///<����֤ȯ����
	XTP_MARKET_TYPE     underlying_security_id_source;      ///<����֤ȯ����Դ

    uint32_t            list_date;                          ///<�������ڣ���ʽΪYYYYMMDD
    uint32_t            last_trade_date;                    ///<������գ���ʽΪYYYYMMDD
    XTP_TICKER_TYPE     ticker_type;                        ///<֤ȯ���
    int32_t             day_trading;                        ///<�Ƿ�֧�ֵ��ջ�ת���ף�1-����0-������

    XTP_OPT_CALL_OR_PUT_TYPE    call_or_put;                ///<�Ϲ����Ϲ�
    uint32_t            delivery_day;                       ///<��Ȩ�����գ���ʽΪYYYYMMDD
    uint32_t            delivery_month;                     ///<�����·ݣ���ʽΪYYYYMM

    XTP_OPT_EXERCISE_TYPE_TYPE  exercise_type;              ///<��Ȩ��ʽ
    uint32_t            exercise_begin_date;                ///<��Ȩ��ʼ���ڣ���ʽΪYYYYMMDD
    uint32_t            exercise_end_date;                  ///<��Ȩ�������ڣ���ʽΪYYYYMMDD
    double              exercise_price;                     ///<��Ȩ�۸�

    int64_t             qty_unit;                           ///<������λ������ĳһ֤ȯ�걨��ί�У���ί�������ֶα���Ϊ��֤ȯ������λ��������
    int64_t             contract_unit;                      ///<��Լ��λ
    int64_t             contract_position;                  ///<��Լ�ֲ���

    double              prev_close_price;                   ///<��Լǰ���̼�
    double              prev_clearing_price;                ///<��Լǰ�����

    int64_t             lmt_buy_max_qty;                    ///<�޼��������
    int64_t             lmt_buy_min_qty;                    ///<�޼�����С��
    int64_t             lmt_sell_max_qty;                   ///<�޼��������
    int64_t             lmt_sell_min_qty;                   ///<�޼�����С��
    int64_t             mkt_buy_max_qty;                    ///<�м��������
    int64_t             mkt_buy_min_qty;                    ///<�м�����С��
    int64_t             mkt_sell_max_qty;                   ///<�м��������
    int64_t             mkt_sell_min_qty;                   ///<�м�����С��

    double              price_tick;                         ///<��С���۵�λ
    double              upper_limit_price;                  ///<��ͣ��
    double              lower_limit_price;                  ///<��ͣ��
    double              sell_margin;                        ///<������ÿ�ű�֤��
    double              margin_ratio_param1;                ///<��������֤������������һ
    double              margin_ratio_param2;                ///<��������֤��������������

    uint64_t            unknown[20];                        ///<�������ֶΣ�
};

/// ��Ȩ��ϲ��Գ���������Ӧ�ṹ��
typedef struct XTPOrderCancelInfo XTPOptCombOrderCancelInfo;

/// ��Ȩ��ϲ��Եĳɷֺ�Լ��Ϣ
struct XTPCombLegStrategy {
    XTP_OPT_CALL_OR_PUT_TYPE    call_or_put;        ///< ��Լ���ͣ��Ϲ����Ϲ�
    XTP_POSITION_DIRECTION_TYPE position_side;      ///< Ȩ���ֻ�������ֻ򱸶������
    TXTPExerciseSeqType         exercise_price_seq; ///< ��Ȩ��˳��
    int32_t                     expire_date_seq;    ///< ������˳��
    int64_t                     leg_qty;            ///< ������ϲ����а����Ĵ˺�Լ����
};

/*/// ��Ȩ��ϲ��Բ�ѯ����ṹ��
typedef struct XTPQueryOptCombineReq
{
	char            strategy_id[XTP_STRATEGY_ID_LEN];	///< ��ϲ��Դ���
	XTP_MARKET_TYPE market;							    ///< �г�
}XTPQueryOptCombineReq;
*/
/// ��ѯ��Ȩ��ϲ�����Ϣ����Ӧ
struct XTPQueryCombineStrategyInfoRsp {
    char                    strategy_id[XTP_STRATEGY_ID_LEN];        ///< ��ϲ��Դ��룬CNSJC��PXSJC��PNSJC��CXSJC��KS��KKS
    char                    strategy_name[XTP_STRATEGY_NAME_LEN];    ///< ��ϲ������ƣ��Ϲ�ţ�м۲���ԡ��Ϲ����м۲���ԡ��Ϲ�ţ�м۲���ԡ��Ϲ����м۲���ԡ���ʽ��ͷ�����ʽ��ͷ
	XTP_MARKET_TYPE         market;                                  ///< �����г�

    int32_t                 leg_num;                                 ///< �ɷֺ�Լ������1-4���������������ʵ�ʴ�С
    XTPCombLegStrategy      leg_strategy[XTP_STRATEGE_LEG_NUM];      ///< �ɷֺ�Լ��Ϣ�����������

    XTP_EXPIRE_DATE_TYPE    expire_date_type;                        ///< ������Ҫ��ö��ֵΪ��ͬ�����գ���ͬ�����գ��޵�����Ҫ��
    XTP_UNDERLYING_TYPE     underlying_type;                         ///< ���Ҫ��ö��ֵΪ����ͬ��ģ���ͬ��ģ��ޱ��Ҫ��
    XTP_AUTO_SPLIT_TYPE     auto_sep_type;                           ///< �Զ�������͡�ö��ֵΪ��-1�������ã�0���������Զ������1��E-1���Զ��������������

    uint64_t                reserved[10];                            ///< Ԥ�����ֶ�
};

/// ��ϲ����Ⱥ�Լ��Ϣ�ṹ��
typedef struct XTPOptCombLegInfo {
    char                            leg_security_id[XTP_TICKER_LEN]; ///< �ɷֺ�Լ����
    XTP_OPT_CALL_OR_PUT_TYPE        leg_cntr_type;                   ///< ��Լ���ͣ��Ϲ����Ϲ���
    XTP_POSITION_DIRECTION_TYPE     leg_side;                        ///< �ֲַ���Ȩ���������񷽡�
    XTP_OPT_COVERED_OR_UNCOVERED    leg_covered;                     ///< ���ұ�ǩ
    int32_t                         leg_qty;                         ///< �ɷֺ�Լ�������ţ�
}XTPOptCombLegInfo;

///��Ȩ��ϲ��Ա���������Ϣ�ṹ��
typedef struct XTPOptCombPlugin {
    char                                strategy_id[XTP_STRATEGY_ID_LEN];               ///< ��ϲ��Դ��룬����CNSJC�Ϲ�ţ�м۲���Եȡ�
    char                                comb_num[XTP_SECONDARY_ORDER_ID_LEN];           ///< ��ϱ��룬����걨ʱ�����ֶ�Ϊ�գ�����걨ʱ����д������ϵ���ϱ��롣
    int32_t                             num_legs;                                       ///< �ɷֺ�Լ��
    XTPOptCombLegInfo                   leg_detail[XTP_STRATEGE_LEG_NUM];               ///< �ɷֺ�Լ���飬��������ȡ�
}XTPOptCombPlugin;

//////////////////////////////////////////////////////////////////////////
///��ѯ��Ȩ��ϲ��Գֲ��������ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryOptCombPositionReq
{
    ///��ϱ���
    char comb_num[XTP_SECONDARY_ORDER_ID_LEN];
    ///�����г�
    XTP_MARKET_TYPE     market;
};


/// ��ѯ��Ȩ��ϲ��Գֲ���Ϣ����Ӧ
struct XTPQueryOptCombPositionRsp {
    char                    strategy_id[XTP_STRATEGY_ID_LEN];           ///< ��ϲ��Դ���
    char                    strategy_name[XTP_STRATEGY_NAME_LEN];       ///< ��ϲ�������
    
    XTP_MARKET_TYPE         market;                                     ///< �����г�
    int64_t                 total_qty;                                  ///< �ֲܳ�
    int64_t                 available_qty;                              ///< �ɲ�ֲֳ�
    int64_t                 yesterday_position;                         ///< ���ճֲ�

    XTPOptCombPlugin        opt_comb_info;                              ///< ��Ȩ��ϲ�����Ϣ

    uint64_t                reserved[50];                               ///< �����ֶ�
};

/// ��ѯ��Ȩ��Լ��Ȩ��Ϣ����Ӧ
struct XTPQueryOptExecInfoRsp {
    XTP_MARKET_TYPE         market;                          ///< �г�
    char                    cntrt_code[XTP_TICKER_LEN];      ///< ��Լ����

    int64_t                 own_qty_long;                    ///< Ȩ��������
    int64_t                 own_qty_short;                   ///< ���������
    int64_t                 own_qty_short_cover;             ///< �������������
    int64_t                 net_qty;                         ///< ��ͷ��

    int64_t                 combed_qty_long;                 ///< Ȩ�������������
    int64_t                 combed_qty_short;                ///< ��������������
    int64_t                 combed_qty_short_cover;          ///< ������������������

    int64_t                 total_execute_gene_order_qty;    ///< �ۼ���ͨ��Ȩί������
    int64_t                 total_execute_gene_confirm_qty;  ///< �ۼ���ͨ��Ȩȷ������
    int64_t                 total_execute_comb_order_qty;    ///< �ۼ���Ȩ�ϲ�ί������
    int64_t                 total_execute_comb_confirm_qty;  ///< �ۼ���Ȩ�ϲ�ȷ������

    uint64_t                reserved[50];                    ///< �����ֶ�
};

//////////////////////////////////////////////////////////////////////////
///��ѯ��Ȩ��Ȩ�ϲ�ͷ������ṹ��
//////////////////////////////////////////////////////////////////////////
struct XTPQueryOptCombExecPosReq
{
    ///�г�
    XTP_MARKET_TYPE market;
    ///�ɷֺ�Լ1����
    char cntrt_code_1[XTP_TICKER_LEN];
    ///�ɷֺ�Լ2����
    char cntrt_code_2[XTP_TICKER_LEN];

};

/// ��ѯ��Ȩ��Ȩ�ϲ�ͷ�����Ӧ
struct XTPQueryOptCombExecPosRsp {

    XTP_MARKET_TYPE                 market;                             ///< �г�
    char                            cntrt_code_1[XTP_TICKER_LEN];       ///< �ɷֺ�Լ1����
    char                            cntrt_name_1[XTP_TICKER_NAME_LEN];  ///< �ɷֺ�Լ1����
    XTP_POSITION_DIRECTION_TYPE     position_side_1;                    ///< �ɷֺ�Լ1�ֲַ���
    XTP_OPT_CALL_OR_PUT_TYPE        call_or_put_1;                      ///< �ɷֺ�Լ1����
    int64_t                         avl_qty_1;                          ///< �ɷֺ�Լ1���óֲ�����
    int64_t                         orig_own_qty_1;                     ///< �ɷֺ�Լ1���ճֲ�����
    int64_t                         own_qty_1;                          ///< �ɷֺ�Լ1��ǰ�ֲ�����

    char                            cntrt_code_2[XTP_TICKER_LEN];       ///< �ɷֺ�Լ2����
    char                            cntrt_name_2[XTP_TICKER_NAME_LEN];  ///< �ɷֺ�Լ2����
    XTP_POSITION_DIRECTION_TYPE     position_side_2;                    ///< �ɷֺ�Լ2�ֲַ���
    XTP_OPT_CALL_OR_PUT_TYPE        call_or_put_2;                      ///< �ɷֺ�Լ2����
    int64_t                         avl_qty_2;                          ///< �ɷֺ�Լ2���óֲ�����
    int64_t                         orig_own_qty_2;                     ///< �ɷֺ�Լ2���ճֲ�����
    int64_t                         own_qty_2;                          ///< �ɷֺ�Լ2��ǰ�ֲ�����

    int64_t                         net_qty;                            ///< Ȩ���־�ͷ��

    int64_t                         order_qty;                          ///< ��Ȩ�ϲ�ί�������������Ѿܵ��ѳ�����
    int64_t                         confirm_qty;                        ///< ��Ȩ�ϲ���ȷ������
    int64_t                         avl_qty;                            ///< ����Ȩ�ϲ�����

    uint64_t                        reserved[49];                       ///< �����ֶ�
};


//////////////////////////////////////////////////////////////////////////
///������ȯֱ�ӻ�����Ӧ��Ϣ
//////////////////////////////////////////////////////////////////////////
struct XTPCrdCashRepayRsp
{
    int64_t xtp_id;             ///< ֱ�ӻ��������XTPID
    double  request_amount;     ///< ֱ�ӻ����������
    double  cash_repay_amount;  ///< ʵ�ʻ���ʹ�ý��
};

//////////////////////////////////////////////////////////////////////////
///������ȯ�ֽ�Ϣ����Ӧ��Ϣ
//////////////////////////////////////////////////////////////////////////
struct XTPCrdCashRepayDebtInterestFeeRsp
{
	int64_t xtp_id;             ///< ֱ�ӻ��������XTPID
	double  request_amount;     ///< ֱ�ӻ����������
	double  cash_repay_amount;  ///< ʵ�ʻ���ʹ�ý��
	char	debt_compact_id[XTP_CREDIT_DEBT_ID_LEN]; ///< ָ���ĸ�ծ��Լ���
	char	unknow[32];			///< �����ֶ�
};

//////////////////////////////////////////////////////////////////////////
///����������ȯֱ�ӻ����¼��Ϣ
//////////////////////////////////////////////////////////////////////////
struct XTPCrdCashRepayInfo
{
    int64_t                     xtp_id;             ///< ֱ�ӻ��������XTPID
    XTP_CRD_CR_STATUS           status;             ///< ֱ�ӻ����״̬
    double                      request_amount;     ///< ֱ�ӻ����������
    double                      cash_repay_amount;  ///< ʵ�ʻ���ʹ�ý��
    XTP_POSITION_EFFECT_TYPE    position_effect;    ///< ǿƽ��־
	XTPRI						error_info;			///< ֱ�ӻ��������ʱ�Ĵ�����Ϣ
};

//////////////////////////////////////////////////////////////////////////
///����������ȯ��ծ��¼��Ϣ
//////////////////////////////////////////////////////////////////////////
typedef struct XTPCrdDebtInfo
{
    int32_t             debt_type;              ///< ��ծ��Լ���ͣ�0Ϊ���ʣ�1Ϊ��ȯ��2δ֪
    char                debt_id[33];            ///< ��ծ��Լ���
    int64_t             position_id;            ///< ��ծ��Ӧ����ͷ����
    uint64_t            order_xtp_id;           ///< ���ɸ�ծ�Ķ�����ţ��ǵ��ո�ծ�޴���
    int32_t             debt_status;            ///< ��ծ��Լ״̬��0Ϊδ�����򲿷ֳ�����1Ϊ�ѳ�����2Ϊ����δƽ�֣�3δ֪
    XTP_MARKET_TYPE     market;                 ///< �г�
    char                ticker[XTP_TICKER_LEN]; ///< ֤ȯ����
    uint64_t            order_date;             ///< ί������
    uint64_t            end_date;               ///< ��ծ��ֹ����
    uint64_t            orig_end_date;          ///< ��ծԭʼ��ֹ����
    bool                is_extended;            ///< �����Ƿ���յ�չ������falseΪû�յ���trueΪ�յ�
    double              remain_amt;             ///< δ�������
    int64_t             remain_qty;             ///< δ������ȯ����
    double              remain_principal;       ///< δ����������
	int64_t				due_right_qty;			///< Ӧ����Ȩ������
	int64_t				unknown[2];				///< �����ֶ�
}XTPCrdDebtInfo;

//////////////////////////////////////////////////////////////////////////
///������ȯ�����ʻ�����
//////////////////////////////////////////////////////////////////////////
typedef struct XTPCrdFundInfo
{
    double maintenance_ratio;       ///< ά�ֵ���Ʒ����
    double all_asset;               ///< ���ʲ�
    double all_debt;                ///< �ܸ�ծ
    double line_of_credit;          ///< �������Ŷ��
    double guaranty;                ///< ���ڱ�֤�������
    double reserved;                ///< �����ֶ�
}XTPCrdFundInfo;

//////////////////////////////////////////////////////////////////////////
///������ȯָ��֤ȯ�ϵĸ�ծδ����������ṹ��
//////////////////////////////////////////////////////////////////////////
typedef struct XTPClientQueryCrdDebtStockReq
{
    XTP_MARKET_TYPE market;                 ///< �г�
    char            ticker[XTP_TICKER_LEN]; ///< ֤ȯ����
}XTPClientQueryCrdDebtStockReq;

//////////////////////////////////////////////////////////////////////////
///������ȯָ��֤ȯ����ȯ��ծ�����Ϣ
//////////////////////////////////////////////////////////////////////////
typedef struct XTPCrdDebtStockInfo
{
    XTP_MARKET_TYPE market;                     ///< �г�
    char            ticker[XTP_TICKER_LEN];     ///< ֤ȯ����
    int64_t         stock_repay_quantity;       ///< ��ȯ��ծ�ɻ�ȯ����
    int64_t         stock_total_quantity;       ///< ��ȯ��ծδ��������
}XTPCrdDebtStockInfo;

//////////////////////////////////////////////////////////////////////////
///��ȯͷ��֤ȯ��ѯ����ṹ��
//////////////////////////////////////////////////////////////////////////
typedef struct XTPClientQueryCrdPositionStockReq
{
    XTP_MARKET_TYPE market;                 ///< ֤ȯ�г�
    char            ticker[XTP_TICKER_LEN]; ///< ֤ȯ����
}XTPClientQueryCrdPositionStockReq;

//////////////////////////////////////////////////////////////////////////
///��ȯͷ��֤ȯ��Ϣ
//////////////////////////////////////////////////////////////////////////
typedef struct XTPClientQueryCrdPositionStkInfo 
{
    XTP_MARKET_TYPE market;                 ///< ֤ȯ�г�
    char            ticker[XTP_TICKER_LEN]; ///< ֤ȯ����
    int64_t         limit_qty;              ///< ��ȯ����
    int64_t         yesterday_qty;          ///< ��������ȯ����
    int64_t         left_qty;               ///< ʣ�����ȯ����
    int64_t         frozen_qty;             ///< ������ȯ����
}XTPClientQueryCrdPositionStkInfo;


//////////////////////////////////////////////////////////////////////////
/// ����ҵ����ȯ��ѯ����ṹ��
//////////////////////////////////////////////////////////////////////////
typedef struct XTPClientQueryCrdSurplusStkReqInfo
{
    XTP_MARKET_TYPE market;                 ///< ֤ȯ�г�
    char            ticker[XTP_TICKER_LEN]; ///< ֤ȯ����
}XTPClientQueryCrdSurplusStkReqInfo;

//////////////////////////////////////////////////////////////////////////
///����ҵ����ȯ��Ϣ
//////////////////////////////////////////////////////////////////////////
typedef struct XTPClientQueryCrdSurplusStkRspInfo
{
    XTP_MARKET_TYPE market;                 ///< ֤ȯ�г�
    char            ticker[XTP_TICKER_LEN]; ///< ֤ȯ����
    int64_t         transferable_quantity;  ///< �ɻ�ת����
    int64_t         transferred_quantity;   ///< �ѻ�ת����
}XTPClientQueryCrdSurplusStkRspInfo;

///�û��ʽ��˻��������ַ�������
#define XTP_ACCOUNT_PASSWORD_LEN 64  

/////////////////////////////////////////////////////////////////////////
///�û�չ������
/////////////////////////////////////////////////////////////////////////
struct XTPCreditDebtExtendReq
{
	uint64_t	xtpid;								///<xtpid
	char		debt_id[XTP_CREDIT_DEBT_ID_LEN];	///<��ծ��Լ���
	uint32_t	defer_days;							///<չ������
	char        fund_account[XTP_ACCOUNT_NAME_LEN];	///<�ʽ��˺�
	char	    password[XTP_ACCOUNT_PASSWORD_LEN];	///<�ʽ��˺�����
};

/////////////////////////////////////////////////////////////////////////
///�û�չ���������Ӧ�ṹ
/////////////////////////////////////////////////////////////////////////
typedef struct XTPCreditDebtExtendNotice XTPCreditDebtExtendAck;


//////////////////////////////////////////////////////////////////////////
/// ������ȯ�ʻ�������Ϣ
//////////////////////////////////////////////////////////////////////////
typedef struct XTPCrdFundExtraInfo
{
    double    mf_rs_avl_used;  ///<��ǰ�ʽ��˻�������һ���ʹ�õ���ȯ���������ʽ�ռ��
    char      reserve[64];     ///<Ԥ���ռ�
}XTPCrdFundExtraInfo;

//////////////////////////////////////////////////////////////////////////
///������ȯ�ʻ��ֲָ�����Ϣ
//////////////////////////////////////////////////////////////////////////
typedef struct XTPCrdPositionExtraInfo
{
    XTP_MARKET_TYPE market;                 ///<֤ȯ�г�
    char            ticker[XTP_TICKER_LEN]; ///<֤ȯ����
    double          mf_rs_avl_used;         ///<������һ���ʹ�õ���ȯ���������ʽ�ռ��
    char            reserve[64];            ///<Ԥ���ռ�
}XTPCrdPositionExtraInfo;

///��Ȩ��ϲ����¶�������
struct XTPOptCombOrderInsertInfo
{
    ///XTPϵͳ����ID�������û���д����XTPϵͳ��Ψһ
    uint64_t                order_xtp_id;
    ///�������ã��ɿͻ��Զ���
    uint32_t	            order_client_id;
    ///�����г�
    XTP_MARKET_TYPE         market;
    ///����(��λΪ��)
    int64_t                 quantity;

    ///��Ϸ���
    XTP_SIDE_TYPE           side;

    ///ҵ������
    XTP_BUSINESS_TYPE       business_type;

    ///��Ȩ��ϲ�����Ϣ
    XTPOptCombPlugin        opt_comb_info;
};

///��Ȩ��ϲ��Ա�����Ӧ�ṹ��
struct XTPOptCombOrderInfo
{
    ///XTPϵͳ����ID����XTPϵͳ��Ψһ
    uint64_t                order_xtp_id;
    ///�������ã��û��Զ���
    uint32_t	            order_client_id;
    ///�����������ã��û��Զ��壨��δʹ�ã�
    uint32_t                order_cancel_client_id;
    ///������XTPϵͳ�е�id����XTPϵͳ��Ψһ
    uint64_t                order_cancel_xtp_id;
    ///֤ȯ����
    ///char                    ticker[XTP_TICKER_LEN];
    ///�����г�
    XTP_MARKET_TYPE         market;
    ///�������˶����ı�������
    int64_t                 quantity;
    
    ///��Ϸ���
    XTP_SIDE_TYPE               side;
           
    ///ҵ������
    XTP_BUSINESS_TYPE       business_type;
    ///��ɽ�������Ϊ�˶����ۼƳɽ�����
    int64_t                 qty_traded;
    ///ʣ���������������ɹ�ʱ����ʾ��������
    int64_t                 qty_left;
    ///ί��ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
    int64_t                 insert_time;
    ///����޸�ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
    int64_t                 update_time;
    ///����ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
    int64_t                 cancel_time;
    ///�ɽ�����ϲ���漰�ı�֤��(�����ֶ�)
    double                  trade_amount;
    ///���ر������ OMS���ɵĵ��ţ�����ͬ��order_xtp_id��Ϊ�������������̵ĵ���
    char                    order_local_id[XTP_LOCAL_ORDER_LEN];
    ///����״̬��������Ӧ��û�в��ֳɽ�״̬�����ͣ��ڲ�ѯ��������У����в��ֳɽ�״̬
    XTP_ORDER_STATUS_TYPE   order_status;
    ///�����ύ״̬���û����ô��ֶ������ֳ����ͱ���
    XTP_ORDER_SUBMIT_STATUS_TYPE   order_submit_status;
    ///��������
    TXTPOrderTypeType       order_type;

    ///��Ȩ��ϲ�����Ϣ
    XTPOptCombPlugin        opt_comb_info;
};


///��Ȩ��ϲ��Ա����ɽ��ṹ��
struct XTPOptCombTradeReport
{
    ///XTPϵͳ����ID���˳ɽ��ر���صĶ���ID����XTPϵͳ��Ψһ
    uint64_t                 order_xtp_id;
    ///��������
    uint32_t                 order_client_id;
    ///�����г�
    XTP_MARKET_TYPE          market;
    ///�����ţ�����XTPID�󣬸��ֶ�ʵ�ʺ�order_xtp_id�ظ����ӿ�����ʱ������
    uint64_t                 local_order_id;
    ///�ɽ���ţ����Ψһ���Ͻ���ÿ�ʽ���Ψһ��������2�ʳɽ��ر�ӵ����ͬ��exec_id���������Ϊ�˱ʽ����Գɽ�
    char                     exec_id[XTP_EXEC_ID_LEN];
    ///�������˴γɽ��������������ۼ�����
    int64_t                  quantity;
    ///�ɽ�ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss
    int64_t                  trade_time;
    ///�ɽ�����ϲ���漰�ı�֤��
    double                   trade_amount;
    ///�ɽ���� --�ر���¼�ţ�ÿ��������Ψһ,report_index+market�ֶο������Ψһ��ʶ��ʾ�ɽ��ر�
    uint64_t                 report_index;
    ///������� --����������(�����ֶ�)
    char                     order_exch_id[XTP_ORDER_EXCH_LEN];
    ///�ɽ�����  --�ɽ��ر��е�ִ������
    TXTPTradeTypeType        trade_type;
    ///��Ϸ���
    XTP_SIDE_TYPE            side;
    ///ҵ������
    XTP_BUSINESS_TYPE        business_type;
    ///����������Ա���� 
    char                     branch_pbu[XTP_BRANCH_PBU_LEN];

    ///��Ȩ��ϲ�����Ϣ
    XTPOptCombPlugin         opt_comb_info;
};


//////////////////////////////////////////////////////////////////////////
///��Ȩ��ϲ��Ա�����ѯ
//////////////////////////////////////////////////////////////////////////
///��Ȩ��ϲ��Ա�����ѯ����-������ѯ
struct XTPQueryOptCombOrderReq
{
    ///��ϱ��루��ˮ�ţ�������Ϊ�գ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����гɽ��ر�
    char      comb_num[XTP_SECONDARY_ORDER_ID_LEN];
    ///��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0��
    int64_t   begin_time;
    ///��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
    int64_t   end_time;
};

///��Ȩ��ϲ��Ա�����ѯ��Ӧ�ṹ��
typedef struct XTPOptCombOrderInfo XTPQueryOptCombOrderRsp;

///��ѯ��Ȩ��ϲ��Զ�������-��ҳ��ѯ
struct XTPQueryOptCombOrderByPageReq
{
    ///��Ҫ��ѯ�Ķ�������
    int64_t         req_count;
    ///��һ���յ��Ĳ�ѯ��������д�����������������Ǵ�ͷ��ѯ������0
    int64_t         reference;
    ///�����ֶ�
    int64_t         reserved;
};

//////////////////////////////////////////////////////////////////////////
///��Ȩ��ϲ��Գɽ��ر���ѯ
//////////////////////////////////////////////////////////////////////////
///��ѯ��Ȩ��ϲ��Գɽ���������-����ִ�б�Ų�ѯ�������ֶΣ�
struct XTPQueryOptCombReportByExecIdReq
{
    ///XTP����ϵͳID
    uint64_t  order_xtp_id;
    ///�ɽ�ִ�б��
    char  exec_id[XTP_EXEC_ID_LEN];
};

///��ѯ��Ȩ��ϲ��Գɽ��ر�����-��ѯ����
struct XTPQueryOptCombTraderReq
{
    ///��ϱ��루��ˮ�ţ�������Ϊ�գ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����гɽ��ر�
    char      comb_num[XTP_SECONDARY_ORDER_ID_LEN];
    ///��ʼʱ�䣬��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0��
    int64_t   begin_time;
    ///����ʱ�䣬��ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
    int64_t   end_time;
};

///�ɽ��ر���ѯ��Ӧ�ṹ��
typedef struct XTPOptCombTradeReport  XTPQueryOptCombTradeRsp;

///��ѯ��Ȩ��ϲ��Գɽ��ر�����-��ҳ��ѯ
struct XTPQueryOptCombTraderByPageReq
{
    ///��Ҫ��ѯ�ĳɽ��ر�����
    int64_t         req_count;
    ///��һ���յ��Ĳ�ѯ�ɽ��ر�����д�����������������Ǵ�ͷ��ѯ������0
    int64_t         reference;
    ///�����ֶ�
    int64_t         reserved;
};



#pragma pack()
#endif //_XOMS_API_STRUCT_H_

