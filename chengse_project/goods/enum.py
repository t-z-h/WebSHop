from chengse_project.goods.models import Goods

FRUIT = 1
SNACKS = 2
ELECTRIC = 3
PROMOTION = 4

GOODS_TYPE = {
    FRUIT: "水果蔬菜",
    SNACKS: "零食",
    ELECTRIC: "家用产品",
    PROMOTION: "手机电脑"
}

GOODS_TYPE_EN = {
    FRUIT: "fruit",
    SNACKS: "snacks",
    ELECTRIC: "electric",
    PROMOTION: "promotion"
}

sort_map = {
    "default": Goods.id,
    "new": Goods.create_time.desc(),
    "price": Goods.product_price,
    "hot": Goods.product_sales
}
