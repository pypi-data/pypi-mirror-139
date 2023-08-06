/////////////////////////////////////////////////////////////////////////
///@author ��̩֤ȯ�ɷ����޹�˾
///@file xtp_quote_api.h
///@brief �������鶩�Ŀͻ��˽ӿ�
/////////////////////////////////////////////////////////////////////////

#ifndef _XTP_QUOTE_API_H_
#define _XTP_QUOTE_API_H_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "xtp_api_struct.h"

#if defined(ISLIB) && defined(WIN32)
#ifdef LIB_MD_API_EXPORT
#define MD_API_EXPORT __declspec(dllexport)
#else
#define MD_API_EXPORT __declspec(dllimport)
#endif
#else
#define MD_API_EXPORT 
#endif

/*!
* \class XTP::API::QuoteSpi
*
* \brief ����ص���
*
* \author ��̩֤ȯ�ɷ����޹�˾
* \date ʮ�� 2015
*/
namespace XTP {
	namespace API {
		class QuoteSpi
		{
		public:

			///���ͻ����������̨ͨ�����ӶϿ�ʱ���÷��������á�
			///@param reason ����ԭ��������������Ӧ
			///@remark api�����Զ������������߷���ʱ�����û�����ѡ����������������ڴ˺����е���Login���µ�¼��ע���û����µ�¼����Ҫ���¶�������
			virtual void OnDisconnected(int reason) {};


			///����Ӧ��
			///@param error_info ����������Ӧ��������ʱ�ľ���Ĵ������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark �˺���ֻ���ڷ�������������ʱ�Ż���ã�һ�������û�����
			virtual void OnError(XTPRI *error_info) {};

			///��������Ӧ�𣬰�����Ʊ��ָ������Ȩ
			///@param ticker ��ϸ�ĺ�Լ�������
			///@param error_info ���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ÿ�����ĵĺ�Լ����Ӧһ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) {};

			///�˶�����Ӧ�𣬰�����Ʊ��ָ������Ȩ
			///@param ticker ��ϸ�ĺ�Լȡ���������
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ÿ��ȡ�����ĵĺ�Լ����Ӧһ��ȡ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnUnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) {};

			///�������֪ͨ��������һ��һ����
			///@param market_data ��������
			///@param bid1_qty ��һ��������
			///@param bid1_count ��һ���е���Чί�б���
			///@param max_bid1_count ��һ������ί�б���
			///@param ask1_qty ��һ��������
			///@param ask1_count ��һ���е���Чί�б���
			///@param max_ask1_count ��һ������ί�б���
			///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnDepthMarketData(XTPMD *market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count, int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count) {};

			///�������鶩����Ӧ�𣬰�����Ʊ��ָ������Ȩ
			///@param ticker ��ϸ�ĺ�Լ�������
			///@param error_info ���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ÿ�����ĵĺ�Լ����Ӧһ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnSubOrderBook(XTPST *ticker, XTPRI *error_info, bool is_last) {};

			///�˶����鶩����Ӧ�𣬰�����Ʊ��ָ������Ȩ
			///@param ticker ��ϸ�ĺ�Լȡ���������
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ÿ��ȡ�����ĵĺ�Լ����Ӧһ��ȡ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnUnSubOrderBook(XTPST *ticker, XTPRI *error_info, bool is_last) {};

			///���鶩����֪ͨ��������Ʊ��ָ������Ȩ
			///@param order_book ���鶩�������ݣ���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnOrderBook(XTPOB *order_book) {};

			///�����������Ӧ�𣬰�����Ʊ��ָ������Ȩ
			///@param ticker ��ϸ�ĺ�Լ�������
			///@param error_info ���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ÿ�����ĵĺ�Լ����Ӧһ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) {};

			///�˶��������Ӧ�𣬰�����Ʊ��ָ������Ȩ
			///@param ticker ��ϸ�ĺ�Լȡ���������
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			///@remark ÿ��ȡ�����ĵĺ�Լ����Ӧһ��ȡ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnUnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) {};

			///�������֪ͨ��������Ʊ��ָ������Ȩ
			///@param tbt_data ����������ݣ��������ί�к���ʳɽ�����Ϊ���ýṹ�壬��Ҫ����type�����������ί�л�����ʳɽ�����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
			virtual void OnTickByTick(XTPTBT *tbt_data) {};

			///����ȫ�г��Ĺ�Ʊ����Ӧ��
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///�˶�ȫ�г��Ĺ�Ʊ����Ӧ��
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnUnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///����ȫ�г��Ĺ�Ʊ���鶩����Ӧ��
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///�˶�ȫ�г��Ĺ�Ʊ���鶩����Ӧ��
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnUnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///����ȫ�г��Ĺ�Ʊ�������Ӧ��
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///�˶�ȫ�г��Ĺ�Ʊ�������Ӧ��
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnUnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};


			///��ѯ��Լ���־�̬��Ϣ��Ӧ��
			///@param ticker_info ��Լ���־�̬��Ϣ
			///@param error_info ��ѯ��Լ���־�̬��Ϣʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴β�ѯ��Լ���־�̬��Ϣ�����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			virtual void OnQueryAllTickers(XTPQSI* ticker_info, XTPRI *error_info, bool is_last) {};

			///��ѯ��Լ�����¼۸���ϢӦ��
			///@param ticker_info ��Լ�����¼۸���Ϣ
			///@param error_info ��ѯ��Լ�����¼۸���Ϣʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴β�ѯ�����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			virtual void OnQueryTickersPriceInfo(XTPTPI* ticker_info, XTPRI *error_info, bool is_last) {};

			///����ȫ�г�����Ȩ����Ӧ��
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///�˶�ȫ�г�����Ȩ����Ӧ��
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnUnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///����ȫ�г�����Ȩ���鶩����Ӧ��
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///�˶�ȫ�г�����Ȩ���鶩����Ӧ��
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnUnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///����ȫ�г�����Ȩ�������Ӧ��
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///�˶�ȫ�г�����Ȩ�������Ӧ��
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@param error_info ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@remark ��Ҫ���ٷ���
			virtual void OnUnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {};

			///��ѯ��Լ������̬��Ϣ��Ӧ��
			///@param ticker_info ��Լ������̬��Ϣ
			///@param error_info ��ѯ��Լ������̬��Ϣʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
			///@param is_last �Ƿ�˴β�ѯ��Լ������̬��Ϣ�����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
			virtual void OnQueryAllTickersFullInfo(XTPQFI* ticker_info, XTPRI *error_info, bool is_last) {};
		};
	}
}

#ifndef WINDOWS
#if __GNUC__ >= 4
#pragma GCC visibility push(default)
#endif
#endif

/*!
* \class XTP::API::QuoteApi
*
* \brief ���鶩�Ľӿ���
*
* \author ��̩֤ȯ�ɷ����޹�˾
* \date ʮ�� 2015
*/
namespace XTP {
	namespace API {
		class MD_API_EXPORT QuoteApi
		{
		public:
			///����QuoteApi
			///@param client_id ���������룩��������ͬһ�û��Ĳ�ͬ�ͻ��ˣ����û��Զ���
			///@param save_file_path ���������룩����������Ϣ�ļ���Ŀ¼�����趨һ���п�дȨ�޵���ʵ���ڵ�·�������·�������ڵĻ������ܻ���Ϊд��ͻ����ɶ���
			///@param log_level ��־�������
			///@return ��������UserApi
			///@remark ���һ���˻���Ҫ�ڶ���ͻ��˵�¼����ʹ�ò�ͬ��client_id��ϵͳ����һ���˻�ͬʱ��¼����ͻ��ˣ����Ƕ���ͬһ�˻�����ͬ��client_idֻ�ܱ���һ��session���ӣ�����ĵ�¼��ǰһ��session�����ڼ䣬�޷�����
			static QuoteApi *CreateQuoteApi(uint8_t client_id, const char *save_file_path, XTP_LOG_LEVEL log_level=XTP_LOG_LEVEL_DEBUG);

			///ɾ���ӿڶ�����
			///@remark ����ʹ�ñ��ӿڶ���ʱ,���øú���ɾ���ӿڶ���
			virtual void Release() = 0;


			///��ȡ��ǰ������
			///@return ��ȡ���Ľ�����
			///@remark ֻ�е�¼�ɹ���,���ܵõ���ȷ�Ľ�����
			virtual const char *GetTradingDay() = 0;

			///��ȡAPI�ķ��а汾��
			///@return ����api���а汾��
			virtual const char* GetApiVersion() = 0;

			///��ȡAPI��ϵͳ����
			///@return ���صĴ�����Ϣ��������Login��Logout�����ġ�ȡ������ʧ��ʱ���ã���ȡʧ�ܵ�ԭ��
			///@remark �����ڵ���api�ӿ�ʧ��ʱ���ã�����loginʧ��ʱ
			virtual XTPRI *GetApiLastError() = 0;

			///���ò���UDP��ʽ����ʱ�Ľ��ջ�������С
			///@remark ��Ҫ��Login֮ǰ���ã�Ĭ�ϴ�С����С���þ�Ϊ64MB���˻����С��λΪMB��������2�Ĵη���������128MB������128��
			virtual void SetUDPBufferSize(uint32_t buff_size) = 0;


			///ע��ص��ӿ�
			///@param spi �����Իص��ӿ����ʵ�������ڵ�¼֮ǰ�趨
			virtual void RegisterSpi(QuoteSpi *spi) = 0;

			///�����������ʱ��������λΪ��
			///@param interval �������ʱ��������λΪ��
			///@remark �˺���������Login֮ǰ����
			virtual void SetHeartBeatInterval(uint32_t interval) = 0;

			///ʹ��UDP��������ʱ�����ý��������̰߳󶨵�cpu
			///@param cpu_no ���ð󶨵�cpu�������cpu 0����������0����cpu 2����������2������󶨺����cpu
			///@remark �˺����ɲ����ã���������������Login֮ǰ���ã����򲻻���Ч
			virtual void SetUDPRecvThreadAffinity(int32_t cpu_no) = 0;

			///ʹ��UDP��������ʱ�����ý��������̰߳󶨵�cpu
			///@param cpu_no ���ð󶨵�cpu�������cpu 0����������0����cpu 2����������2������󶨺����cpu
			///@remark �˺����ɲ����ã���������������Login֮ǰ���ã����򲻻���Ч
			virtual void SetUDPParseThreadAffinity(int32_t cpu_no) = 0;

			///�趨UDP������ʱ�Ƿ�����첽��־
			///@param flag �Ƿ������ʶ��Ĭ��Ϊtrue��������������udpseq����ͷ���첽��־�������ô˲���Ϊfalse
			///@remark �˺����ɲ����ã���������������Login֮ǰ���ã����򲻻���Ч
			virtual void SetUDPSeqLogOutPutFlag(bool flag = true) = 0;

			///�������飬������Ʊ��ָ������Ȩ��
			///@return ���Ľӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո� 
			///@param count Ҫ����/�˶�����ĺ�Լ����
			///@param exchange_id ����������
			///@remark ����һ���Զ���ͬһ֤ȯ�������Ķ����Լ�������û���Ϊ����������Ҫ���µ�¼���������������Ҫ���¶�������
			virtual int SubscribeMarketData(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///�˶����飬������Ʊ��ָ������Ȩ��
			///@return ȡ�����Ľӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո�  
			///@param count Ҫ����/�˶�����ĺ�Լ����
			///@param exchange_id ����������
			///@remark ����һ����ȡ������ͬһ֤ȯ�������Ķ����Լ����Ҫ�붩������ӿ�����ʹ��
			virtual int UnSubscribeMarketData(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///�������鶩������������Ʊ��ָ������Ȩ��
			///@return �������鶩�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո� 
			///@param count Ҫ����/�˶����鶩�����ĺ�Լ����
			///@param exchange_id ����������
			///@remark ����һ���Զ���ͬһ֤ȯ�������Ķ����Լ�������û���Ϊ����������Ҫ���µ�¼���������������Ҫ���¶�������(��֧�����)
			virtual int SubscribeOrderBook(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///�˶����鶩������������Ʊ��ָ������Ȩ��
			///@return ȡ���������鶩�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո�  
			///@param count Ҫ����/�˶����鶩�����ĺ�Լ����
			///@param exchange_id ����������
			///@remark ����һ����ȡ������ͬһ֤ȯ�������Ķ����Լ����Ҫ�붩�����鶩�����ӿ�����ʹ��
			virtual int UnSubscribeOrderBook(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///����������飬������Ʊ��ָ������Ȩ��
			///@return �����������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո�  
			///@param count Ҫ����/�˶����鶩�����ĺ�Լ����
			///@param exchange_id ����������
			///@remark ����һ���Զ���ͬһ֤ȯ�������Ķ����Լ�������û���Ϊ����������Ҫ���µ�¼���������������Ҫ���¶�������
			virtual int SubscribeTickByTick(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///�˶�������飬������Ʊ��ָ������Ȩ��
			///@return ȡ�������������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո�  
			///@param count Ҫ����/�˶����鶩�����ĺ�Լ����
			///@param exchange_id ����������
			///@remark ����һ����ȡ������ͬһ֤ȯ�������Ķ����Լ����Ҫ�붩���������ӿ�����ʹ��
			virtual int UnSubscribeTickByTick(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///����ȫ�г��Ĺ�Ʊ����
			///@return ����ȫ�г�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ��ȫ�г��˶�����ӿ�����ʹ��
			virtual int SubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�˶�ȫ�г��Ĺ�Ʊ����
			///@return �˶�ȫ�г�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ�붩��ȫ�г�����ӿ�����ʹ��
			virtual int UnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///����ȫ�г��Ĺ�Ʊ���鶩����
			///@return ����ȫ�г����鶩�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ��ȫ�г��˶����鶩�����ӿ�����ʹ��
			virtual int SubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�˶�ȫ�г��Ĺ�Ʊ���鶩����
			///@return �˶�ȫ�г����鶩�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ�붩��ȫ�г����鶩�����ӿ�����ʹ��
			virtual int UnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///����ȫ�г��Ĺ�Ʊ�������
			///@return ����ȫ�г��������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ��ȫ�г��˶��������ӿ�����ʹ��
			virtual int SubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�˶�ȫ�г��Ĺ�Ʊ�������
			///@return �˶�ȫ�г��������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ�붩��ȫ�г��������ӿ�����ʹ��
			virtual int UnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�û���¼����
			///@return ��¼�Ƿ�ɹ�����0����ʾ��¼�ɹ�����-1����ʾ���ӷ�����������ʱ�û����Ե���GetApiLastError()����ȡ������룬��-2����ʾ�Ѵ������ӣ��������ظ���¼�������Ҫ����������logout����-3����ʾ�����д���
			///@param ip ������ip��ַ�����ơ�127.0.0.1��
			///@param port �������˿ں�
			///@param user ��½�û���
			///@param password ��½����
			///@param sock_type ��1������TCP����2������UDP
			///@param local_ip ����������ַ�����ơ�127.0.0.1��
			///@remark �˺���Ϊͬ������ʽ������Ҫ�첽�ȴ���¼�ɹ������������ؼ��ɽ��к�����������apiֻ����һ������
			virtual int Login(const char* ip, int port, const char* user, const char* password, XTP_PROTOCOL_TYPE sock_type, const char* local_ip = NULL) = 0;


			///�ǳ�����
			///@return �ǳ��Ƿ�ɹ�����0����ʾ�ǳ��ɹ����ǡ�0����ʾ�ǳ�������ʱ�û����Ե���GetApiLastError()����ȡ�������
			///@remark �˺���Ϊͬ������ʽ������Ҫ�첽�ȴ��ǳ������������ؼ��ɽ��к�������
			virtual int Logout() = 0;

			///��ȡ��ǰ�����պ�Լ���־�̬��Ϣ
			///@return ���Ͳ�ѯ�����Ƿ�ɹ�����0����ʾ���Ͳ�ѯ����ɹ����ǡ�0����ʾ���Ͳ�ѯ���󲻳ɹ�
			///@param exchange_id ���������룬�����ṩ 1-�Ϻ� 2-����
			virtual int QueryAllTickers(XTP_EXCHANGE_TYPE exchange_id) = 0;

			///��ȡ��Լ�����¼۸���Ϣ
			///@return ���Ͳ�ѯ�����Ƿ�ɹ�����0����ʾ���Ͳ�ѯ����ɹ����ǡ�0����ʾ���Ͳ�ѯ���󲻳ɹ�
			///@param ticker ��ԼID���飬ע���Լ���������'\0'��β���������ո�  
			///@param count Ҫ��ѯ�ĺ�Լ����
			///@param exchange_id ����������
			virtual int QueryTickersPriceInfo(char *ticker[], int count, XTP_EXCHANGE_TYPE exchange_id) = 0;

			///��ȡ���к�Լ�����¼۸���Ϣ
			///@return ���Ͳ�ѯ�����Ƿ�ɹ�����0����ʾ���Ͳ�ѯ����ɹ����ǡ�0����ʾ���Ͳ�ѯ���󲻳ɹ�
			virtual int QueryAllTickersPriceInfo() = 0;

			///����ȫ�г�����Ȩ����
			///@return ����ȫ����Ȩ������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ��ȫ�г��˶���Ȩ����ӿ�����ʹ��
			virtual int SubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�˶�ȫ�г�����Ȩ����
			///@return �˶�ȫ�г���Ȩ����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ�붩��ȫ�г���Ȩ����ӿ�����ʹ��
			virtual int UnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///����ȫ�г�����Ȩ���鶩����
			///@return ����ȫ�г���Ȩ���鶩�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ��ȫ�г��˶���Ȩ���鶩�����ӿ�����ʹ��
			virtual int SubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�˶�ȫ�г�����Ȩ���鶩����
			///@return �˶�ȫ�г���Ȩ���鶩�����ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ�붩��ȫ�г���Ȩ���鶩�����ӿ�����ʹ��
			virtual int UnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///����ȫ�г�����Ȩ�������
			///@return ����ȫ�г���Ȩ�������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰȫ���ĵ��г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ��ȫ�г��˶���Ȩ�������ӿ�����ʹ��
			virtual int SubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///�˶�ȫ�г�����Ȩ�������
			///@return �˶�ȫ�г���Ȩ�������ӿڵ����Ƿ�ɹ�����0����ʾ�ӿڵ��óɹ����ǡ�0����ʾ�ӿڵ��ó���
			///@param exchange_id ��ʾ��ǰ�˶����г������ΪXTP_EXCHANGE_UNKNOWN����ʾ����ȫ�г���XTP_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���XTP_EXCHANGE_SZ��ʾΪ����ȫ�г�
			///@remark ��Ҫ�붩��ȫ�г���Ȩ�������ӿ�����ʹ��
			virtual int UnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN) = 0;

			///��ȡ���к�Լ����ϸ��̬��Ϣ������ָ���ȷǿɽ��׵�
			///@return ���Ͳ�ѯ�����Ƿ�ɹ�����0����ʾ���Ͳ�ѯ����ɹ����ǡ�0����ʾ���Ͳ�ѯ���󲻳ɹ�
			///@param exchange_id ���������룬�����ṩ 1-�Ϻ� 2-����
			virtual int QueryAllTickersFullInfo(XTP_EXCHANGE_TYPE exchange_id) = 0;


		protected:
			~QuoteApi() {};
		};
	}
}

#ifndef WINDOWS
#if __GNUC__ >= 4
#pragma GCC visibility pop
#endif
#endif


#endif
