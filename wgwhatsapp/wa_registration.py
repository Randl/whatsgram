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


def requestCode(phone_num, country_code):
    codeReq = WACodeRequest(str(country_code), str(phone_num))
    result = codeReq.send()
    print(answerToStr(result))
    if result["status"] != "ok":
        logger.warning('Code request for number {} failed. Request answer: {}'.format(result['login'], result))
    else:
        logger.warning('Code requested for number {}'.format(result['login']))


def register(phone_num, country_code, code):
    req = WARegRequest(str(country_code), str(phone_num), str(code))
    result = req.send()
    print(answerToStr(result))
    if result["status"] == "ok":
        logger.info('Registration for number {}'.format(result['login']))
        return result['pw']
    else:
        logger.warning('Registration failed for number {}. Request answer: {}'.format(result['login'], result))
        return ''
