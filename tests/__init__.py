import logging

FORMAT = "[%(asctime)s  - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='debug_out.log', format=FORMAT, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())