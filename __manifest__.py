{
    "name": "Fleet Routes",
    "summary": "Track delivery routes and fleet trucks",
    "version": "19.0.1.0.0",
    "category": "Human Resources/Fleet",
    "author": "Kenrix Marquez",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        'views/routes_views.xml',
        "views/batch_delivery_views.xml",
        'views/menu.xml',
    ],
    "depends": [
        "base",
        "fleet",
        "sale",
        'stock',              # usually required
        'sale_management',    # often needed
        'delivery',           # if delivery logic is involved
        'sale_stock',         # VERY likely where field comes from
    ],
    "installable": True,
    "application": False,
    "sequence": 1,
    "auto_install" : False
}