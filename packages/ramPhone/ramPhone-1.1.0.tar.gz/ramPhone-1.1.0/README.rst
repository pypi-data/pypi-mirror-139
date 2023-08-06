一个生成随机手机号的插件
========================



1、不带任何参数的随机生成
~~~~~~~~~~~~~~~~~~~~

    ramPhone.toPhone() \**\* 默认的号段为3、5、8、9。

2、带号段生成(手机号号段是第二位)
~~~~~~~~~~~~~~~~~~~~

   ramPhone.toPhoneSegment(Segment) \**\*
   此参数为类型list，会从传递的list数组中随机生成手机号的第二位数字。

3、带地区区号生成，(一般指手机号4~7位)，类型为str
~~~~~~~~~~~~~~~~~~~~
   ramPhone.toPhoneAreaCode(AreaCode) \**\* 此参数为类型str，需要四位数

4、带号段和地区区号生成，类型为list和str
~~~~~~~~~~~~~~~~~~~~

    ramPhone.toPhoneSegmentAndAreaCode(Segment, AreaCode)
