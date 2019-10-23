
class RETCODE:
    OK = "0"  # 成功
    IMAGECODEERR = "4001"  # 验证码错误
    THROTTLINGERR = "4002"  # 短信发送频繁
    NECESSARYPARAMERR = "4003"  # 缺少必须的参数
    USERERR = "4004"  # 用户错误
    PWDERR = "4005"  # 密码错误
    CPWDERR = "4006"  # 确认密码错误
    MOBILEERR = "4007"  # 手机号错误
    SMSCODERR = "4008"  # 短信验证码错误
    ALLOWERR = "4009"  # 未同意协议错误
    SESSIONERR = "4101"  # 未登录
    DBERR = "5000"  # 数据库错误
    EMAILERR = "5001"  # 邮箱错误
    TELERR = "5002"  # 电话错误
    NODATAERR = "5003"  # 无匹配数据
    NEWPWDERR = "5004"  # 新密码错误
    OPENIDERR = "5005"  # 第三方认证错误
    PARAMERR = "5006"  # 参数错误
    STOCKERR = "5007"  # 库存不足