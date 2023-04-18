import logging

logging.basicConfig(filename="FundooLog.log", encoding="utf-8", level=logging.DEBUG, format='%(asctime)s %(message)s', )

logger = logging.getLogger()