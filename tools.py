
from langchain_core.tools import tool
@tool
def calc_math(expr:str)->float:
    """
    模拟数学计算工具,用于处理基础的加减乘除运算
    参数：expr(str)数学表达式,例如“100/4+18”
    返回:float:计算结果
    :param expr:
    :return:
    """
    print(f"[工具调用]calc_math正在计算:{expr}")
    result=eval(expr)
    return float(result)
