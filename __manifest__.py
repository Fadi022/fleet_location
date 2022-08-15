{
'name': 'Location des Véhicules',
'summary': "Gestion d’une agence de location de Véhicules",
'sequence':1,
'description': """
        Gestion d’une agence de location de véhicules
        ==============
        Description relative à la gestion d’une agence de véhicule .
        """,
  'author': "Equipe AZIMATEK",
  'website': "https.azimatek.com",
  'category': 'Uncategorized',
  'version': '1.0',
  'sequence':0,
   'depends': [
   'fleet',
   ],
   'data': [
        'views/fleet_location_contrat_view.xml',
        'reports/fleet_location_contrat_repport.xml',
        ],
   'demo': [],
   'installable': True,
   'application': True,
   'license': 'LGPL-3',
}