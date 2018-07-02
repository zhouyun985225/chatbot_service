# docker环境变量设置
默认值均为production情况下的值

## CHATBOT\_LISTENING\_PORT

监听端口设置，应设置为容器暴露的端口,默认8082

## IR\_SERVICE\_URL

IR Service的地址，默认 <https://trueview.natappvip.cc/android?q=>

## WECHAT\_TOKEN

微信公众号的Token,默认 trueai

## WECHAT\_APP\_ID

微信公众号的App ID,默认 wx63efb6f9efadb72b

## WECHAT\_APP\_SECRET

微信公众号的App Secret,默认 45a4a1cdd8bd13e44e9ce26e763d931e

## ENVIRONMENT

运行环境，可选 development 和 production, 默认 development

## TULING\_ENABLE

是否启用图灵api, 默认 True

## TULING\_KEY

图灵api的AppKey, 默认 302e70feb15347a9a497dc1d5d405bec

## TULING\_URL

图灵api的URL, 默认 <http://www.tuling123.com/openapi/api>

## REDIS\_HOST

Redis 服务器的地址，默认 r-uf6de3a867308ef4.redis.rds.aliyuncs.com

## REDIS\_PORT

Redis 服务器的端口，默认6379

## REDIS\_PASSWORD

Redis 服务器的端口，默认为空

## REDIS\_EXPIRE\_TIME

Redis 服务器缓存数据的过期时间，默认7200

## TRUEVIEW\_CHATBOT\_MAX\_DIALOG\_COUNT

Redis 缓存对话的轮数，默认为 5
