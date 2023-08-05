import pickle
import os

def initialize():
    print('正在安装依赖库，请稍等')
    os.system('pip install -r requirements.txt')
    daily_data_file=input('请设置日频数据存放路径(请最终以斜杠结尾)：')
    minute_data_file=input('请设置分钟数据存放路径(请最终以斜杠结尾)：')
    factor_data_file=input('请设置因子数据存放路径(请最终以斜杠结尾)：')
    barra_data_file=input('请设置barra数据存放路径(请最终以斜杠结尾)：')
    save_dict={'daily_data_file':daily_data_file,'minute_data_file':minute_data_file,
               'factor_data_file':factor_data_file,'barra_data_file':barra_data_file}
    save_dict_file=open('paths.settings','wb')
    pickle.dump(save_dict,save_dict_file)
    save_dict_file.close()
    from loguru import logger
    logger.success('恭喜你，回测框架初始化完成，可以开始使用了👏')