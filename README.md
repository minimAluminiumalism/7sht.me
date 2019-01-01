#Crawler for 7sht.me

##7sht.me.ChineseSubtitle.py
This script is only created for **Chinese subtitle branch** in 7sht.me and can run nomally in it.

##7sht.me_Asian.py
This script is only for **Asian Censored Branch**, which add the function to import basic information including title, magnet and actress to MongoDB, the style of text mode is like following

`
{
    "_id" : ObjectId("5c2b8aabb520d9f2e319af5d"),
    "title" : "vgd-197 AV女優の裏側リポート かたりたがーる ひなた澪",
    "magnet" : "magnet:?xt=urn:btih:0D58AD10154A344F69118C771F8B1BD747402801",
    "Actress" : "ひなた澪"
}

/* 2 */
{
    "_id" : ObjectId("5c2b8aaeb520d9f2e319af5e"),
    "title" : "tsp-413 いじめられっこ超絶パシリの逆襲計画 学校女子たちに買",
    "magnet" : "magnet:?xt=urn:btih:01CE32E1A9AB712E530A3E10E6E53D5848596D7F",
    "Actress" : "----"
}

/* 3 */
{
    "_id" : ObjectId("5c2b8aafb520d9f2e319af5f"),
    "title" : "oyc-226 スポーツジムのロッカーでインストラクターにセクハラを",
    "magnet" : "magnet:?xt=urn:btih:F95E22BA4D4C33828A7033E4FAD21903D756F1DD",
    "Actress" : "----"
}
`
###Notification

Movies' preview image will also be saved in your current directory.

###Requirements

You should already installed MongoDB, and start Mongo service first, then modify the **config.py** before run the **7sht.me_Asian.py**.
