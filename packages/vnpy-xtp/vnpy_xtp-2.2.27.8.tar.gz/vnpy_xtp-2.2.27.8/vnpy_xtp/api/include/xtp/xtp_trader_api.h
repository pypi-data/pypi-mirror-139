/////////////////////////////////////////////////////////////////////////
///@author ��̩֤ȯ�ɷ����޹�˾
///@file xtp_trader_api.h
///@brief ����ͻ��˽��׽ӿ�
/////////////////////////////////////////////////////////////////////////

#ifndef _XTP_TRADER_API_H_
#define _XTP_TRADER_API_H_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "xtp_api_struct.h"

#if defined(ISLIB) && defined(WIN32)
#ifdef LIB_TRADER_API_EXPORT
#define TRADER_API_EXPORT __declspec(dllexport)
#else
#define TRADER_API_EXPORT __declspec(dllimport)
#endif
#else
#define TRADER_API_EXPORT 
#endif

/*!
* \class XTP::API::TraderSpi
*
* \brief ���׽ӿ���Ӧ��
*
* \author ��̩֤ȯ�ɷ����޹�˾
* \date ʮ�� 2015
*/
namespace XTP {
	namespace API {

		class TraderSpi
		{
		public:

			///���ͻ��˵�ĳ�������뽻�׺�̨ͨ�����ӶϿ�ʱ���÷��������á�
			///@param reason ����ԭ��������������Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark �û���������logout���µĶ��ߣ����ᴥ���˺�����api�����Զ������������߷���ʱ�����û�����ѡ����������������ڴ˺����е���Login���µ�¼��������session_id����ʱ�û��յ������ݸ�����֮ǰ��������
			virtual void OnDisconnected(uint64_t session_id, int reason) {};

			///����Ӧ��
			///@param error_info ����������Ӧ��������ʱ�ľ���Ĵ������ʹ�����Ϣ,��error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark �˺���ֻ���ڷ�������������ʱ�Ż���ã�һ�������û�����
			virtual void OnError(XTPRI *error_info) {};

			///����֪ͨ
			///@param order_info ������Ӧ������Ϣ���û�����ͨ��order_info.order_xtp_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ�����order_info.qty_left�ֶ��ڶ���Ϊδ�ɽ������ɡ�ȫ�ɡ��ϵ�״̬ʱ����ʾ�˶�����û�гɽ����������ڲ�����ȫ��״̬ʱ����ʾ�˶���������������order_info.order_cancel_xtp_idΪ������Ӧ�ĳ���ID����Ϊ0ʱ��ʾ�˵������ɹ�
			///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ÿ�ζ���״̬����ʱ�����ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ��ڶ���δ�ɽ���ȫ���ɽ���ȫ�����������ֳ������Ѿܾ���Щ״̬ʱ������Ӧ�����ڲ��ֳɽ�����������ɶ����ĳɽ��ر�������ȷ�ϡ����е�¼�˴��û��Ŀͻ��˶����յ����û��Ķ�����Ӧ
			virtual void OnOrderEvent(XTPOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) {};

			///�ɽ�֪ͨ
			///@param trade_info �ɽ��ر��ľ�����Ϣ���û�����ͨ��trade_info.order_xtp_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ����������Ͻ�����exec_id����Ψһ��ʶһ�ʳɽ���������2�ʳɽ��ر�ӵ����ͬ��exec_id���������Ϊ�˱ʽ����Գɽ��ˡ����������exec_id��Ψһ�ģ���ʱ�޴��жϻ��ơ�report_index+market�ֶο������Ψһ��ʶ��ʾ�ɽ��ر���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark �����гɽ�������ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��ĳɽ��ر�����ض���Ϊ����״̬����Ҫ�û�ͨ���ɽ��ر��ĳɽ�������ȷ����OnOrderEvent()�������Ͳ���״̬��
			virtual void OnTradeEvent(XTPTradeReport *trade_info, uint64_t session_id) {};

			///����������Ӧ
			///@param cancel_info ����������Ϣ������������order_cancel_xtp_id�ʹ�������order_xtp_id
			///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ���error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����Ӧֻ���ڳ�����������ʱ���ص�
			virtual void OnCancelOrderError(XTPOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) {};

			///�����ѯ������Ӧ
			///@param order_info ��ѯ����һ������
			///@param error_info ��ѯ����ʱ��������ʱ�����صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryOrder(XTPQueryOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��ҳ�����ѯ������Ӧ
			///@param order_info ��ѯ����һ������
			///@param req_count ��ҳ������������
			///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
			///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ���б��������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���б����Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryOrderByPage(XTPQueryOrderRsp *order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�ɽ���Ӧ
			///@param trade_info ��ѯ����һ���ɽ��ر�
			///@param error_info ��ѯ�ɽ��ر���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryTrade(XTPQueryTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��ҳ�����ѯ�ɽ���Ӧ
			///@param trade_info ��ѯ����һ���ɽ���Ϣ
			///@param req_count ��ҳ������������
			///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
			///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryTradeByPage(XTPQueryTradeRsp *trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯͶ���ֲ߳���Ӧ
			///@param position ��ѯ����һֻ��Ʊ�ĳֲ����
			///@param error_info ��ѯ�˻��ֲַ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark �����û����ܳ��ж����Ʊ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryPosition(XTPQueryStkPositionRsp *position, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�ʽ��˻���Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param asset ��ѯ�����ʽ��˻����
			///@param error_info ��ѯ�ʽ��˻���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryAsset(XTPQueryAssetRsp *asset, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�ּ�������Ϣ��Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param fund_info ��ѯ���ķּ��������
			///@param error_info ��ѯ�ּ�����������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryStructuredFund(XTPStructuredFundInfo *fund_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�ʽ𻮲�������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param fund_transfer_info ��ѯ�����ʽ��˻����
			///@param error_info ��ѯ�ʽ��˻���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�ʽ𻮲�֪ͨ
			///@param fund_transfer_info �ʽ𻮲�֪ͨ�ľ�����Ϣ���û�����ͨ��fund_transfer_info.serial_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ�����
			///@param error_info �ʽ𻮲��������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д��󡣵��ʽ𻮲�����Ϊһ�������Ľڵ�֮�仮������error_info.error_id=11000384ʱ��error_info.error_msgΪ����п����ڻ������ʽ�������Ϊ׼�����û������stringToInt��ת�����ɾݴ���д���ʵ��ʽ��ٴη��𻮲�����
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ���ʽ𻮲�������״̬�仯��ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û����ʽ𻮲�֪ͨ��
			virtual void OnFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, uint64_t session_id) {};

			///�����ѯETF�嵥�ļ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param etf_info ��ѯ����ETF�嵥�ļ����
			///@param error_info ��ѯETF�嵥�ļ���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryETF(XTPQueryETFBaseRsp *etf_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯETF��Ʊ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param etf_component_info ��ѯ����ETF��Լ����سɷֹ���Ϣ
			///@param error_info ��ѯETF��Ʊ����������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryETFBasket(XTPQueryETFComponentRsp *etf_component_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�����¹��깺��Ϣ�б����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param ipo_info ��ѯ���Ľ����¹��깺��һֻ��Ʊ��Ϣ
			///@param error_info ��ѯ�����¹��깺��Ϣ�б�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryIPOInfoList(XTPQueryIPOTickerRsp *ipo_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�û��¹��깺�����Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param quota_info ��ѯ�����û�ĳ���г��Ľ����¹��깺�����Ϣ
			///@param error_info ���ѯ�û��¹��깺�����Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryIPOQuotaInfo(XTPQueryIPOQuotaRsp *quota_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ��Ȩ��Լ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param option_info ��ѯ������Ȩ��Լ���
			///@param error_info ��ѯ��Ȩ��Լ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryOptionAuctionInfo(XTPQueryOptionAuctionInfoRsp *option_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///������ȯҵ�����ֽ�ֱ�ӻ������Ӧ
			///@param cash_repay_info �ֽ�ֱ�ӻ���֪ͨ�ľ�����Ϣ���û�����ͨ��cash_repay_info.xtp_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ�����
			///@param error_info �ֽ𻹿������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnCreditCashRepay(XTPCrdCashRepayRsp *cash_repay_info, XTPRI *error_info, uint64_t session_id) {};

			///������ȯҵ�����ֽ�Ϣ����Ӧ
			///@param cash_repay_info �ֽ�Ϣ֪ͨ�ľ�����Ϣ���û�����ͨ��cash_repay_info.xtp_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ�����
			///@param error_info �ֽ�Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnCreditCashRepayDebtInterestFee(XTPCrdCashRepayDebtInterestFeeRsp *cash_repay_info, XTPRI *error_info, uint64_t session_id) {};

			///�����ѯ������ȯҵ���е��ֽ�ֱ�ӻ��������Ӧ
			///@param cash_repay_info ��ѯ����ĳһ���ֽ�ֱ�ӻ���֪ͨ�ľ�����Ϣ
			///@param error_info ��ѯ�ֽ�ֱ�ӱ�����������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditCashRepayInfo(XTPCrdCashRepayInfo *cash_repay_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�����˻�������Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param fund_info ��ѯ���������˻�������Ϣ���
			///@param error_info ��ѯ�����˻�������Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditFundInfo(XTPCrdFundInfo *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) {};

			///�����ѯ�����˻���ծ��Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param debt_info ��ѯ���������˻���Լ��ծ���
			///@param error_info ��ѯ�����˻���ծ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditDebtInfo(XTPCrdDebtInfo *debt_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�����˻�ָ��֤ȯ��ծδ����Ϣ��Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param debt_info ��ѯ���������˻�ָ��֤ȯ��ծδ����Ϣ���
			///@param error_info ��ѯ�����˻�ָ��֤ȯ��ծδ����Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditTickerDebtInfo(XTPCrdDebtStockInfo *debt_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ�����˻������ʽ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param remain_amount ��ѯ���������˻������ʽ�
			///@param error_info ��ѯ�����˻������ʽ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditAssetDebtInfo(double remain_amount, XTPRI *error_info, int request_id, uint64_t session_id) {};

			///�����ѯ�����˻�����ȯͷ����Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param assign_info ��ѯ���������˻�����ȯͷ����Ϣ
			///@param error_info ��ѯ�����˻�����ȯͷ����Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditTickerAssignInfo(XTPClientQueryCrdPositionStkInfo *assign_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///������ȯҵ���������ѯָ����ȯ��Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param stock_info ��ѯ������ȯ��Ϣ
			///@param error_info ��ѯ�����˻���ȯ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditExcessStock(XTPClientQueryCrdSurplusStkRspInfo* stock_info, XTPRI *error_info, int request_id, uint64_t session_id) {};

			///������ȯҵ���������ѯ��ȯ��Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param stock_info ��ѯ������ȯ��Ϣ
			///@param error_info ��ѯ�����˻���ȯ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryMulCreditExcessStock(XTPClientQueryCrdSurplusStkRspInfo* stock_info, XTPRI *error_info, int request_id, uint64_t session_id, bool is_last) {};

			///������ȯҵ���и�ծ��Լչ�ڵ�֪ͨ
			///@param debt_extend_info ��ծ��Լչ��֪ͨ�ľ�����Ϣ���û�����ͨ��debt_extend_info.xtpid����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ�����
			///@param error_info ��ծ��Լչ�ڶ������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����ծ��Լչ�ڶ�����״̬�仯��ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��ĸ�ծ��Լչ��֪ͨ��
			virtual void OnCreditExtendDebtDate(XTPCreditDebtExtendNotice *debt_extend_info, XTPRI *error_info, uint64_t session_id) {};

			///��ѯ������ȯҵ���и�ծ��Լչ�ڶ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param debt_extend_info ��ѯ���ĸ�ծ��Լչ�����
			///@param error_info ��ѯ��ծ��Լչ�ڷ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д��󡣵�error_info.error_id=11000350ʱ������û�м�¼����Ϊ������0ֵʱ��������Լ�����ܵ�ʱ�Ĵ���ԭ��
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditExtendDebtDateOrders(XTPCreditDebtExtendNotice *debt_extend_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��ѯ������ȯҵ���������˻�������Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param fund_info �����˻�������Ϣ
			///@param error_info ��ѯ�����˻�������Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditFundExtraInfo(XTPCrdFundExtraInfo *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) {};

			///��ѯ������ȯҵ���������˻�ָ��֤ȯ�ĸ�����Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			///@param fund_info �����˻�ָ��֤ȯ�ĸ�����Ϣ
			///@param error_info ��ѯ�����˻�������Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnQueryCreditPositionExtraInfo(XTPCrdPositionExtraInfo *fund_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��Ȩ��ϲ��Ա���֪ͨ
			///@param order_info ������Ӧ������Ϣ���û�����ͨ��order_info.order_xtp_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ�����order_info.qty_left�ֶ��ڶ���Ϊδ�ɽ������ɡ�ȫ�ɡ��ϵ�״̬ʱ����ʾ�˶�����û�гɽ����������ڲ�����ȫ��״̬ʱ����ʾ�˶���������������order_info.order_cancel_xtp_idΪ������Ӧ�ĳ���ID����Ϊ0ʱ��ʾ�˵������ɹ�
			///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ÿ�ζ���״̬����ʱ�����ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ��ڶ���δ�ɽ���ȫ���ɽ���ȫ�����������ֳ������Ѿܾ���Щ״̬ʱ������Ӧ�����ڲ��ֳɽ�����������ɶ����ĳɽ��ر�������ȷ�ϡ����е�¼�˴��û��Ŀͻ��˶����յ����û��Ķ�����Ӧ
			virtual void OnOptionCombinedOrderEvent(XTPOptCombOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) {};

			///��Ȩ��ϲ��Գɽ�֪ͨ
			///@param trade_info �ɽ��ر��ľ�����Ϣ���û�����ͨ��trade_info.order_xtp_id����������ͨ��GetClientIDByXTPID() == client_id�������Լ��Ķ����������Ͻ�����exec_id����Ψһ��ʶһ�ʳɽ���������2�ʳɽ��ر�ӵ����ͬ��exec_id���������Ϊ�˱ʽ����Գɽ��ˡ����������exec_id��Ψһ�ģ���ʱ�޴��жϻ��ơ�report_index+market�ֶο������Ψһ��ʶ��ʾ�ɽ��ر���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark �����гɽ�������ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��ĳɽ��ر�����ض���Ϊ����״̬����Ҫ�û�ͨ���ɽ��ر��ĳɽ�������ȷ����OnOrderEvent()�������Ͳ���״̬��
			virtual void OnOptionCombinedTradeEvent(XTPOptCombTradeReport *trade_info, uint64_t session_id) {};

			///��Ȩ��ϲ��Գ���������Ӧ
			///@param cancel_info ����������Ϣ������������order_cancel_xtp_id�ʹ�������order_xtp_id
			///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ���error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����Ӧֻ���ڳ�����������ʱ���ص�
			virtual void OnCancelOptionCombinedOrderError(XTPOptCombOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) {};

			///�����ѯ��Ȩ��ϲ��Ա�����Ӧ
			///@param order_info ��ѯ����һ������
			///@param error_info ��ѯ����ʱ��������ʱ�����صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ��˶�Ӧ����������������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
			virtual void OnQueryOptionCombinedOrders(XTPQueryOptCombOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��ҳ�����ѯ��Ȩ��ϲ��Ա�����Ӧ
			///@param order_info ��ѯ����һ������
			///@param req_count ��ҳ������������
			///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
			///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ���б��������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���б����Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryOptionCombinedOrdersByPage(XTPQueryOptCombOrderRsp *order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ��Ȩ��ϲ��Գɽ���Ӧ
			///@param trade_info ��ѯ����һ���ɽ��ر�
			///@param error_info ��ѯ�ɽ��ر���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ��˶�Ӧ����������������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
			virtual void OnQueryOptionCombinedTrades(XTPQueryOptCombTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��ҳ�����ѯ��Ȩ��ϲ��Գɽ���Ӧ
			///@param trade_info ��ѯ����һ���ɽ���Ϣ
			///@param req_count ��ҳ������������
			///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
			///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryOptionCombinedTradesByPage(XTPQueryOptCombTradeRsp *trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ��Ȩ��ϲ��Գֲ���Ӧ
			///@param position_info ��ѯ����һ���ֲ���Ϣ
			///@param error_info ��ѯ�ֲַ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryOptionCombinedPosition(XTPQueryOptCombPositionRsp *position_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///�����ѯ��Ȩ��ϲ�����Ϣ��Ӧ
			///@param strategy_info ��ѯ����һ����ϲ�����Ϣ
			///@param error_info ��ѯ�ɽ��ر���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryOptionCombinedStrategyInfo(XTPQueryCombineStrategyInfoRsp *strategy_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

			///��ѯ��Ȩ��Ȩ�ϲ�ͷ�����Ӧ
			///@param position_info ��ѯ����һ����Ȩ�ϲ�ͷ����Ϣ
			///@param error_info ��ѯ�ֲַ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param request_id ����Ϣ��Ӧ������Ӧ������ID
			///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@remark һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
			virtual void OnQueryOptionCombinedExecPosition(XTPQueryOptCombExecPosRsp *position_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {};

		};
	}
}

#ifndef WINDOWS
#if __GNUC__ >= 4
#pragma GCC visibility push(default)
#endif
#endif

/*!
* \class XTP::API::TraderApi
*
* \brief ���׽ӿ���
*
* \author ��̩֤ȯ�ɷ����޹�˾
* \date ʮ�� 2015
*/
namespace XTP {
	namespace API {

		class TRADER_API_EXPORT TraderApi
		{
		public:
			///����TraderApi
			///@param client_id ���������룩�ͻ���id����������ͬһ�û��Ĳ�ͬ�ͻ��ˣ����û��Զ��壬��ͨ�û�����ʹ��1-99֮�����ֵ����������޷���¼
			///@param save_file_path ���������룩����������Ϣ�ļ���Ŀ¼�����趨һ����ʵ���ڵ��п�дȨ�޵�·��
			///@param log_level ��־�������
			///@return ��������UserApi
			///@remark ֻ�ܴ���һ�Σ����һ���˻���Ҫ�ڶ���ͻ��˵�¼����ʹ�ò�ͬ��client_id��ϵͳ����һ���˻�ͬʱ��¼����ͻ��ˣ����Ƕ���ͬһ�˻�����ͬ��client_idֻ�ܱ���һ��session���ӣ�����ĵ�¼��ǰһ��session�����ڼ䣬�޷����ӡ�ϵͳ��֧�ֹ�ҹ����ȷ��ÿ�쿪��ǰ��������
			static TraderApi *CreateTraderApi(uint8_t client_id, const char *save_file_path, XTP_LOG_LEVEL log_level = XTP_LOG_LEVEL_DEBUG);

			///ɾ���ӿڶ�����
			///@remark ����ʹ�ñ��ӿڶ���ʱ,���øú���ɾ���ӿڶ���
			virtual void Release() = 0;

			///��ȡ��ǰ������
			///@return ��ȡ���Ľ�����
			///@remark ֻ�е�¼�ɹ���,���ܵõ���ȷ�Ľ�����
			virtual const char *GetTradingDay() = 0;

			///ע��ص��ӿ�
			///@param spi �����Իص��ӿ����ʵ�������ڵ�¼֮ǰ�趨
			virtual void RegisterSpi(TraderSpi *spi) = 0;

			///��ȡAPI��ϵͳ����
			///@return ���صĴ�����Ϣ��������Login��InsertOrder��CancelOrder����ֵΪ0ʱ���ã���ȡʧ�ܵ�ԭ��
			///@remark �����ڵ���api�ӿ�ʧ��ʱ���ã�����loginʧ��ʱ
			virtual XTPRI *GetApiLastError() = 0;

			///��ȡAPI�ķ��а汾��
			///@return ����api���а汾��
			virtual const char* GetApiVersion() = 0;

			///ͨ��������xtpϵͳ�е�ID��ȡ�µ��Ŀͻ���id
			///@return ���ؿͻ���id�������ô˷��������Լ��µĶ���
			///@param order_xtp_id ������xtpϵͳ�е�ID
			///@remark ����ϵͳ����ͬһ�û��ڲ�ͬ�ͻ����ϵ�¼������ÿ���ͻ���ͨ����ͬ��client_id��������
			virtual uint8_t GetClientIDByXTPID(uint64_t order_xtp_id) = 0;

			///ͨ��������xtpϵͳ�е�ID��ȡ����ʽ��˻���
			///@return �����ʽ��˻���
			///@param order_xtp_id ������xtpϵͳ�е�ID
			///@remark ֻ���ʽ��˻���¼�ɹ���,���ܵõ���ȷ����Ϣ
			virtual const char* GetAccountByXTPID(uint64_t order_xtp_id) = 0;

			///���Ĺ�������
			///@param resume_type ��������������Ӧ���ɽ��ر����ش���ʽ  
			///        XTP_TERT_RESTART:�ӱ������տ�ʼ�ش�
			///        XTP_TERT_RESUME:(�����ֶΣ��˷�ʽ��δ֧��)���ϴ��յ�������
			///        XTP_TERT_QUICK:ֻ���͵�¼�󹫹���������
			///@remark �÷���Ҫ��Login����ǰ���á����������򲻻��յ������������ݡ�ע�����û����ߺ�������ǳ���login()�����������ķ�ʽ���������á��û�ֻ���յ����ߺ��������Ϣ�������logout()��login()����ô���������ķ�ʽ�������ã��û��յ������ݻ�����û���ѡ��ʽ������
			virtual void SubscribePublicTopic(XTP_TE_RESUME_TYPE resume_type) = 0;

			///������������汾��
			///@param version �û���������汾�ţ���api���а汾�ţ����Ȳ�����15λ����'\0'��β
			///@remark �˺���������Login֮ǰ���ã���ʶ���ǿͻ��˰汾�ţ�������API�İ汾�ţ����û��Զ���
			virtual void SetSoftwareVersion(const char* version) = 0;

			///�����������Key
			///@param key �û��������Key���û����뿪��ʱ���裬��'\0'��β
			///@remark �˺���������Login֮ǰ����
			virtual void SetSoftwareKey(const char* key) = 0;

			///�����������ʱ��������λΪ��
			///@param interval �������ʱ��������λΪ��
			///@remark �˺���������Login֮ǰ����
			virtual void SetHeartBeatInterval(uint32_t interval) = 0;

			///�û���¼����
			///@return session_id�������ʽ��˺ŵ�¼�Ƿ�ɹ�����0����ʾ��¼ʧ�ܣ����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ��¼�ɹ�����ʱ��Ҫ��¼���������ֵsession_id�����¼���ʽ��˻���Ӧ
			///@param ip ��������ַ�����ơ�127.0.0.1��
			///@param port �������˿ں�
			///@param user ��¼�û���
			///@param password ��¼����
			///@param sock_type ��1������TCP����2������UDP��Ŀǰ��ʱֻ֧��TCP
			///@param local_ip ����������ַ�����ơ�127.0.0.1��
			///@remark �˺���Ϊͬ������ʽ������Ҫ�첽�ȴ���¼�ɹ������������ؼ��ɽ��к�����������api��֧�ֶ���˻����ӣ�����ͬһ���˻�ͬһ��client_idֻ����һ��session���ӣ�����ĵ�¼��ǰһ��session�����ڼ䣬�޷�����
			virtual uint64_t Login(const char* ip, int port, const char* user, const char* password, XTP_PROTOCOL_TYPE sock_type, const char* local_ip = NULL) = 0;


			///�ǳ�����
			///@return �ǳ��Ƿ�ɹ�����0����ʾ�ǳ��ɹ�����-1����ʾ�ǳ�ʧ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			virtual int Logout(uint64_t session_id) = 0;

			///�������Ƿ�������
			///@return ��true����ʾ����������false����ʾû��������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark �˺���������Login֮�����
			virtual bool IsServerRestart(uint64_t session_id) = 0;

			///�޸��ѵ�¼�û���Ӳ����Ϣ��������Ȩϵͳʹ��
			///@return ������Ϣ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param info ��Ҫ�޸ĳɵ��û�Ӳ����Ϣ
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark �˺���������Login֮����ã��ҽ�����Ȩϵͳʹ�ã�һ��ͻ�����ʹ��
			virtual int ModifyUserTerminalInfo(const XTPUserTerminalInfoReq* info,uint64_t session_id) = 0;

			///����¼������
			///@return ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��������ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ�������ͳɹ����û���Ҫ��¼�·��ص�order_xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param order ����¼����Ϣ������order.order_client_id�ֶ����û��Զ����ֶΣ��û�����ʲôֵ��������ӦOnOrderEvent()����ʱ�ͻ����ʲôֵ�������ڱ�ע�������û��Լ���λ��������Ȼ�������ʲô�����Ҳ�ǿ��Եġ�order.order_xtp_id�ֶ������û���д��order.ticker���벻���ո���'\0'��β
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark ���������ն����󣬻��ڱ�����Ӧ����OnOrderEvent()�з��ر���δ�ɽ���״̬��֮�����еĶ���״̬�ı䣨���˲���״̬������ͨ��������Ӧ��������
			virtual uint64_t InsertOrder(XTPOrderInsertInfo *order, uint64_t session_id) = 0;

			///������������
			///@return ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��������ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ�������ͳɹ����û���Ҫ��¼�·��ص�order_cancel_xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param order_xtp_id ��Ҫ������ί�е���XTPϵͳ�е�ID
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark ��������ɹ������ڱ�����Ӧ����OnOrderEvent()�ﷵ��ԭ����������ȫ������Ϣ��������ɹ�������OnCancelOrderError()��Ӧ�����з��ش���ԭ��
			virtual uint64_t CancelOrder(const uint64_t order_xtp_id, uint64_t session_id) = 0;

			///���ݱ���ID�����ѯ����
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param order_xtp_id ��Ҫ��ѯ�ı�����xtpϵͳ�е�ID����InsertOrder()�ɹ�ʱ���ص�order_xtp_id
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) = 0;

			///�����ѯ����
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ�Ķ������ɸѡ���������к�Լ�������Ϊ�գ���Ĭ�����д��ڵĺ�Լ���룬�����Ϊ�գ��벻���ո񣬲���'\0'��β��������ʼʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0�㣬����ʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ʱ�β�ѯ�������Ʊ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����б����������ѯʱ��������и���Ʊ������صı������˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ���˺�����������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
			virtual int QueryOrders(const XTPQueryOrderReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯδ��ᱨ��
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryUnfinishedOrders(uint64_t session_id, int request_id) = 0;

			///��ҳ�����ѯ����
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ҳ��ѯ�����������������һ�β�ѯ����ôquery_param.reference��0
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ҳ��ѯ��ע���û���Ҫ��¼�����һ�ʲ�ѯ�����reference�Ա��û��´β�ѯʹ��
			virtual int QueryOrdersByPage(const XTPQueryOrderByPageReq *query_param, uint64_t session_id, int request_id) = 0;

			///����ί�б�������ѯ��سɽ�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param order_xtp_id ��Ҫ��ѯ��ί�б�ţ���InsertOrder()�ɹ�ʱ���ص�order_xtp_id
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ
			virtual int QueryTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) = 0;

			///�����ѯ�ѳɽ�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ�ĳɽ��ر�ɸѡ���������к�Լ�������Ϊ�գ���Ĭ�����д��ڵĺ�Լ���룬�����Ϊ�գ��벻���ո񣬲���'\0'��β��������ʼʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0�㣬����ʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ʱ�β�ѯ�������Ʊ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����гɽ��ر��������ѯʱ��������и���Ʊ������صĳɽ��ر����˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ���˺�����������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
			virtual int QueryTrades(XTPQueryTraderReq *query_param, uint64_t session_id, int request_id) = 0;

			///��ҳ�����ѯ�ɽ��ر�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ҳ��ѯ�ɽ��ر��������������һ�β�ѯ����ôreference��0
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ҳ��ѯ��ע���û���Ҫ��¼�����һ�ʲ�ѯ�����reference�Ա��û��´β�ѯʹ��
			virtual int QueryTradesByPage(const XTPQueryTraderByPageReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯͶ���ֲ߳�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param ticker ��Ҫ��ѯ�ֲֵĺ�Լ���룬����ΪNULL����ʾ��ѯȫ�г��������ΪNULL���벻���ո񣬲���'\0'��β��ע������marketƥ�䣬��ƥ��Ļ�����������֤ȯ���뻦��2���г����ظ��������²�ѯ��������ĳֲ�
			///@param market ��Ҫ��ѯ�ֲֵĺ�Լ�����г���Ĭ��Ϊ0�����ں�Լ���벻ΪNULL��ʱ�򣬲Ż�ʹ�á�market��ָ������Ϊ��0����������Чֵ����£���������֤ȯ���뻦��2���г����ظ��������²�ѯ��������ĳֲ֡��������ȷ��ѯָ���ֲ֣���ָ��market
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷�������û��ṩ�˺�Լ���룬����ѯ�˺�Լ�ĳֲ���Ϣ��ע����ָ��market�����marketΪ0�����ܻ��ѯ��2���г��ĳֲ֣����marketΪ��������Чֵ�����ѯ����᷵���Ҳ����ֲ֣��������Լ����Ϊ�գ���Ĭ�ϲ�ѯ���гֲ���Ϣ��
			virtual int QueryPosition(const char *ticker, uint64_t session_id, int request_id, XTP_MARKET_TYPE market = XTP_MKT_INIT) = 0;

			///�����ѯ�ʲ�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryAsset(uint64_t session_id, int request_id) = 0;

			///�����ѯ�ּ�����
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ�ķּ�����ɸѡ����������ĸ����������Ϊ�գ���Ĭ�����д��ڵ�ĸ���������Ϊ�գ��벻���ո񣬲���'\0'��β�����н����г�����Ϊ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ
			virtual int QueryStructuredFund(XTPQueryStructuredFundInfoReq *query_param, uint64_t session_id, int request_id) = 0;

			///�ʽ𻮲�����
			///@return �ʽ𻮲�������XTPϵͳ�е�ID,���Ϊ��0����ʾ��Ϣ����ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ��Ϣ���ͳɹ����û���Ҫ��¼�·��ص�serial_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param fund_transfer �ʽ𻮲���������Ϣ
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark �˺���֧��һ�������Ľڵ�֮����ʽ𻮲���ע���ʽ𻮲��ķ���
			virtual uint64_t FundTransfer(XTPFundTransferReq *fund_transfer, uint64_t session_id) = 0;

			///�����ѯ�ʽ𻮲�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ���ʽ𻮲�����ɸѡ����������serial_id����Ϊ0����Ĭ�������ʽ𻮲������������Ϊ0���������ض����ʽ𻮲�����
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryFundTransfer(XTPQueryFundTransferLogReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯETF�嵥�ļ�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ��ETF�嵥�ļ���ɸѡ���������к�Լ�������Ϊ�գ���Ĭ�����д��ڵ�ETF��Լ���룬market�ֶ�Ҳ����Ϊ��ʼֵ����Ĭ�������г���ETF��Լ
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryETF(XTPQueryETFBaseReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯETF��Ʊ��
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ��Ʊ���ĵ�ETF��Լ�����к�Լ���벻����Ϊ�գ�market�ֶ�Ҳ����ָ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryETFTickerBasket(XTPQueryETFComponentReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯ�����¹��깺��Ϣ�б�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryIPOInfoList(uint64_t session_id, int request_id) = 0;

			///�����ѯ�û��¹��깺�����Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryIPOQuotaInfo(uint64_t session_id, int request_id) = 0;

			///�����ѯ��Ȩ��Լ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ����Ȩ��Լ��ɸѡ����������ΪNULL��ΪNULL��ʾ��ѯ���е���Ȩ��Լ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryOptionAuctionInfo(XTPQueryOptionAuctionInfoReq *query_param, uint64_t session_id, int request_id) = 0;

			///������ȯҵ�����ֽ�ֱ�ӻ�������
			///@return �ֽ�ֱ�ӻ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��Ϣ����ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ��Ϣ���ͳɹ����û���Ҫ��¼�·��ص�xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param amount �ֽ𻹿�Ľ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			virtual uint64_t CreditCashRepay(double amount, uint64_t session_id) = 0;

			///������ȯҵ�����ֽ�ָ����ծ��ԼϢ������
			///@return �ֽ�Ϣ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��Ϣ����ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ��Ϣ���ͳɹ����û���Ҫ��¼�·��ص�xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param debt_id ָ���ĸ�ծ��Լ���
			///@param amount �ֽ�Ϣ�Ľ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			virtual uint64_t CreditCashRepayDebtInterestFee(const char* debt_id, double amount, uint64_t session_id) = 0;

			///������ȯҵ������ȯ��ָ����ծ��ԼϢ������
			///@return ��ȯ��Ϣ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��Ϣ����ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ��Ϣ���ͳɹ����û���Ҫ��¼�·��ص�xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param order ��ȯ�ı���¼����Ϣ������order.order_client_id�ֶ����û��Զ����ֶΣ��û�����ʲôֵ��������ӦOnOrderEvent()����ʱ�ͻ����ʲôֵ�������ڱ�ע�������û��Լ���λ��������Ȼ�������ʲô�����Ҳ�ǿ��Եġ�order.order_xtp_id�ֶ������û���д��order.ticker���벻���ո���'\0'��β
			///@param debt_id ָ���ĸ�ծ��Լ���
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			virtual uint64_t CreditSellStockRepayDebtInterestFee(XTPOrderInsertInfo* order, const char* debt_id, uint64_t session_id) = 0;

			///�����ѯ������ȯҵ���е��ֽ�ֱ�ӻ����
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditCashRepayInfo(uint64_t session_id, int request_id) = 0;


			///�����ѯ�����˻�������Ϣ�����ʽ��˻��������Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditFundInfo(uint64_t session_id, int request_id) = 0;

			///�����ѯ�����˻���ծ��Լ��Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditDebtInfo(uint64_t session_id, int request_id) = 0;

			///�����ѯָ��֤ȯ��ծδ����Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ��ָ��֤ȯ��ɸѡ������ticker����ȫ��0�������Ϊ0���벻���ո񣬲���'\0'��β
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditTickerDebtInfo(XTPClientQueryCrdDebtStockReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯ�����˻������ʽ���Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditAssetDebtInfo(uint64_t session_id, int request_id) = 0;

			///�����ѯ�����˻�����ȯͷ����Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ��֤ȯ��ɸѡ������ticker����ȫ��0�������Ϊ0���벻���ո񣬲���'\0'��β
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditTickerAssignInfo(XTPClientQueryCrdPositionStockReq *query_param, uint64_t session_id, int request_id) = 0;

			///������ȯҵ���������ѯָ��֤ȯ����ȯ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ����ȯ��Ϣ��������Ϊ�գ���Ҫ��ȷָ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷������û������ṩ��֤ȯ����������г�
			virtual int QueryCreditExcessStock(XTPClientQueryCrdSurplusStkReqInfo *query_param, uint64_t session_id, int request_id) = 0;

			///������ȯҵ���������ѯ��ȯ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ����ȯ��Ϣ���������г��͹�Ʊ���룬���ص�֧��Ʊ��Ϣ�����г�����Ϊ�գ���Ʊ����ǿգ�����Ч��ѯ������SPI�з��ش������г��͹�Ʊ�����Ϊ�գ�����ȫ�г���Ϣ�����г�����ǿգ���Ʊ����Ϊ�գ����ص��г���Ϣ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryMulCreditExcessStock(XTPClientQueryCrdSurplusStkReqInfo *query_param, uint64_t session_id, int request_id) = 0;   

			///������ȯҵ��������ծ��Լչ��
			///@return ��ծ��Լչ�ڶ�����XTPϵͳ�е�ID,���Ϊ��0����ʾ��Ϣ����ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ��Ϣ���ͳɹ����û���Ҫ��¼�·��ص�xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param debt_extend ��ծ��Լչ�ڵ�������Ϣ
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			virtual uint64_t CreditExtendDebtDate(XTPCreditDebtExtendReq *debt_extend, uint64_t session_id) = 0;

			///������ȯҵ���������ѯ��ծ��Լչ��
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param xtp_id ��Ҫ��ѯ�ĸ�ծ��Լչ�ڶ���ɸѡ������xtp_id����Ϊ0����Ĭ�����и�ծ��Լչ�ڶ����������Ϊ0���������ض��ĸ�ծ��Լչ�ڶ���
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditExtendDebtDateOrders(uint64_t xtp_id, uint64_t session_id, int request_id) = 0;

			///�����ѯ������ȯҵ�����ˑ��ĸ�����Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditFundExtraInfo(uint64_t session_id, int request_id) = 0;

			///�����ѯ������ȯҵ�����ˑ�ָ��֤ȯ�ĸ�����Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫָ����֤ȯ��ɸѡ������ticker����ȫ��0�������Ϊ0���벻���ո񣬲���'\0'��β
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryCreditPositionExtraInfo(XTPClientQueryCrdPositionStockReq *query_param, uint64_t session_id, int request_id) = 0;

			///��Ȩ��ϲ��Ա���¼������
			///@return ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��������ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ�������ͳɹ����û���Ҫ��¼�·��ص�order_xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param order ����¼����Ϣ������order.order_client_id�ֶ����û��Զ����ֶΣ��û�����ʲôֵ��������ӦOnOptionCombinedOrderEvent()����ʱ�ͻ����ʲôֵ�������ڱ�ע�������û��Լ���λ��������Ȼ�������ʲô�����Ҳ�ǿ��Եġ�order.order_xtp_id�ֶ������û���д��order.ticker���벻���ո���'\0'��β
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark ���������ն����󣬻��ڱ�����Ӧ����OnOptionCombinedOrderEvent()�з��ر���δ�ɽ���״̬��֮�����еĶ���״̬�ı䣨���˲���״̬������ͨ��������Ӧ��������
			virtual uint64_t InsertOptionCombinedOrder(XTPOptCombOrderInsertInfo *order, uint64_t session_id) = 0;




			///��Ȩ��ϲ��Ա�����������
			///@return ������XTPϵͳ�е�ID,���Ϊ��0����ʾ��������ʧ�ܣ���ʱ�û����Ե���GetApiLastError()����ȡ������룬�ǡ�0����ʾ�������ͳɹ����û���Ҫ��¼�·��ص�order_cancel_xtp_id������֤һ����������Ψһ����ͬ�Ľ����ղ���֤Ψһ��
			///@param order_xtp_id ��Ҫ��������Ȩ��ϲ���ί�е���XTPϵͳ�е�ID
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@remark ��������ɹ������ڱ�����Ӧ����OnOptionCombinedOrderEvent()�ﷵ��ԭ����������ȫ������Ϣ��������ɹ�������OnCancelOrderError()��Ӧ�����з��ش���ԭ��
			virtual uint64_t CancelOptionCombinedOrder(const uint64_t order_xtp_id, uint64_t session_id) = 0;

			///�����ѯ��Ȩ��ϲ���δ��ᱨ��
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryOptionCombinedUnfinishedOrders(uint64_t session_id, int request_id) = 0;

			///���ݱ���ID�����ѯ��Ȩ��ϲ��Ա���
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param order_xtp_id ��Ҫ��ѯ�ı�����xtpϵͳ�е�ID����InsertOrder()�ɹ�ʱ���ص�order_xtp_id
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			virtual int QueryOptionCombinedOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) = 0;

			///�����ѯ��Ȩ��ϲ��Ա���
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ�Ķ������ɸѡ���������к�Լ�������Ϊ�գ���Ĭ�����д��ڵĺ�Լ���룬�����Ϊ�գ��벻���ո񣬲���'\0'��β��������ʼʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0�㣬����ʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ʱ�β�ѯ�������Ʊ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����б����������ѯʱ��������и���Ʊ������صı������˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ���˺�����������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
			virtual int QueryOptionCombinedOrders(const XTPQueryOptCombOrderReq *query_param, uint64_t session_id, int request_id) = 0;

			///��ҳ�����ѯ��Ȩ��ϲ��Ա���
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ҳ��ѯ�����������������һ�β�ѯ����ôquery_param.reference��0
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ҳ��ѯ��ע���û���Ҫ��¼�����һ�ʲ�ѯ�����reference�Ա��û��´β�ѯʹ��
			virtual int QueryOptionCombinedOrdersByPage(const XTPQueryOptCombOrderByPageReq *query_param, uint64_t session_id, int request_id) = 0;

			///������Ȩ��ϲ���ί�б�������ѯ��سɽ�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param order_xtp_id ��Ҫ��ѯ��ί�б�ţ���InsertOrder()�ɹ�ʱ���ص�order_xtp_id
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ
			virtual int QueryOptionCombinedTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) = 0;

			///�����ѯ��Ȩ��ϲ��Եĳɽ��ر�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ�ĳɽ��ر�ɸѡ���������к�Լ�������Ϊ�գ���Ĭ�����д��ڵĺ�Լ���룬�����Ϊ�գ��벻���ո񣬲���'\0'��β��������ʼʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰ������0�㣬����ʱ���ʽΪYYYYMMDDHHMMSSsss��Ϊ0��Ĭ�ϵ�ǰʱ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ʱ�β�ѯ�������Ʊ����Ϊ�գ���Ĭ�ϲ�ѯʱ����ڵ����гɽ��ر��������ѯʱ��������и���Ʊ������صĳɽ��ر����˺�����ѯ���Ľ�����ܶ�Ӧ�����ѯ�����Ӧ���˺�����������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
			virtual int QueryOptionCombinedTrades(const XTPQueryOptCombTraderReq *query_param, uint64_t session_id, int request_id) = 0;

			///��ҳ�����ѯ��Ȩ��ϲ��Գɽ��ر�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ҳ��ѯ�ɽ��ر��������������һ�β�ѯ����ôreference��0
			///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷���֧�ַ�ҳ��ѯ��ע���û���Ҫ��¼�����һ�ʲ�ѯ�����reference�Ա��û��´β�ѯʹ��
			virtual int QueryOptionCombinedTradesByPage(const XTPQueryOptCombTraderByPageReq *query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯͶ������Ȩ��ϲ��Գֲ�
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ�ֲֵ�ɸѡ������������ϲ��Դ�����Գ�ʼ��Ϊ�գ���ʾ��ѯ���У������Ϊ�գ��벻���ո񣬲���'\0'��β��ע������marketƥ�䣬��ƥ��Ļ������ܵ��²�ѯ��������ĳֲ�
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷�������û��ṩ�˺�Լ���룬����ѯ�˺�Լ�ĳֲ���Ϣ��ע����ָ��market�����marketΪ0�����ܻ��ѯ��2���г��ĳֲ֣����marketΪ��������Чֵ�����ѯ����᷵���Ҳ����ֲ֣��������Լ����Ϊ�գ���Ĭ�ϲ�ѯ���гֲ���Ϣ��
			virtual int QueryOptionCombinedPosition(const XTPQueryOptCombPositionReq* query_param, uint64_t session_id, int request_id) = 0;

			///�����ѯ��Ȩ��ϲ�����Ϣ
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷�����֧�־�ȷ��ѯ����֧��ģ����ѯ
			virtual int QueryOptionCombinedStrategyInfo(uint64_t session_id, int request_id) = 0;

			///�����ѯ��Ȩ��Ȩ�ϲ�ͷ��
			///@return ��ѯ�Ƿ�ɹ�����0����ʾ�ɹ����ǡ�0����ʾ������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@param query_param ��Ҫ��ѯ����Ȩ�ϲ���ɸѡ����������marketΪ0��Ĭ�ϲ�ѯȫ�г����ɷֺ�Լ������Գ�ʼ��Ϊ�գ������Ϊ�գ��벻���ո񣬲���'\0'��β��ע��������д�������������ƥ��
			///@param session_id �ʽ��˻���Ӧ��session_id,��¼ʱ�õ�
			///@param request_id �����û���λ��ѯ��Ӧ��ID�����û��Զ���
			///@remark �÷������ܶ�Ӧ������Ӧ��Ϣ
			virtual int QueryOptionCombinedExecPosition(const XTPQueryOptCombExecPosReq* query_param, uint64_t session_id, int request_id) = 0;

		protected:
			~TraderApi() {};
		};

			}
}

#ifndef WINDOWS
#if __GNUC__ >= 4
#pragma GCC visibility pop
#endif
#endif


#endif
