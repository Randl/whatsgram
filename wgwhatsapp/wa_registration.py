import logging

from yowsup.registration import WACodeRequest, WARegRequest

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def answerToStr(result):
    out = []
    for k, v in result.items():
        if v is None:
            continue
        out.append('{}: {}\n'.format(k, v))
    return ''.join(out)


def requestCodeWA(country_code, phone_num, method='sms'):
    codereq = WACodeRequest(cc=str(country_code), p_in=str(phone_num), method=method)
    result = codereq.send()
    print(answerToStr(result))
    if result["status"] != "sent":
        logger.warning('Code request for number {}{} failed. Request answer:\n{}'.format(country_code, phone_num,
                                                                                         answerToStr(result)))
    else:
        logger.warning('Code requested for number {}{}'.format(country_code, phone_num))


def registerWA(country_code, phone_num, code):
    req = WARegRequest(str(country_code), str(phone_num), str(code))
    result = req.send()
    print(answerToStr(result))
    if result["status"] == "ok":
        logger.info('Registration for number {}'.format(result['login']))
        return result['pw']
    else:
        logger.warning('Registration failed for number {}{}. Request answer: {}'.format(country_code, phone_num,
                                                                                        answerToStr(result)))
        return ''
