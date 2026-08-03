{
    "name": "Fleet Routes",
    "summary": "Track delivery routes and fleet trucks",
    "version": "19.0.1.0.0",
    "category": "Human Resources/Fleet",
    "author": "Kenrix Marquez",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        'views/routes_views.xml',
        'views/menu.xml',
    ],
    "depends": [
        "base",
        "fleet",
    ],
    "installable": True,
    "application": False,
    "sequence": -100,
    "auto_install" : False
}