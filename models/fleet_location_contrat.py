# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FleetLocationContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'
    _name = 'fleet.vehicle.log.contract'
    _description = 'Vehicle Contract'
    _order = 'state desc'
    # ============Information personnelles du locateire====
    nom_locataire = fields.Char("Nom ",required=True)
    km_locataire = fields.Integer("Kilometrage par locataire",required=True)
    prenom_locataire = fields.Char("Prenom ",required=True)
    date_naissance = fields.Date("Date de naissance")
    nationalite = fields.Char("Nationalite")
    adresse_maroc = fields.Char("Adresse au maroc")
    adresse_etranger = fields.Char("Adresse a l'étranger")
    tel = fields.Char("Telephone")
    #=========== CINE======
    cin_locataire = fields.Char("C.I.N.E du locataire",required=True)
    cin_locataire_debut = fields.Date("Date de dilivrance CINE",required=True)
    cin_locataire_fin = fields.Date("Date d'expiration CINE",required=True)
    #====Infos passeport ====
    passport = fields.Char("Passport N°")
    passeport_debut =fields.Date("Date de dilivrance du passeport",required=True)
    passeport_fin =fields.Date("Date d'expiration du passeport",required=True)
    #=======infos permis==========
    permis_locataire = fields.Char("Numero de Permis ",required=True)
    date_debut_permis_locataire = fields.Date("Date de dilivrance ",required=True)
    date_expiration_permis_locataire = fields.Date("Date d'exepiration ",required=True)
    ville_permis_locataire = fields.Char("Ville d'obtention",required=True)
    #====infos sur la durée de location=====
    date_depart = fields.Date('Date depart ',required=True)
    heure_depart = fields.Datetime('Heure depart ',required=True)
    date_retour = fields.Date('Date retour',required=True)
    heure_retour = fields.Datetime('Heure retour',required=True)
    nbr_jour=fields.Integer("Nombre de jours")
    nbr_jours = fields.Integer(compute='_compute_nbr_jours', string='Nombre de jours de location')
    #==================infos voiture=====
    marque = fields.Char("Marque")
    #=======Colocataire======
    nom_colocataire = fields.Char("Nom ",required=True)
    prenom_colocataire = fields.Char("Prenom ",required=True)
    date_naissance_col = fields.Date("Date de naissance")
    nationalie_col = fields.Char("Nationalite")
    cin_colocataire = fields.Char("C.I.N.E ",required=True)
    cin_colocataire_debut = fields.Date("Du ",required=True)
    cin_colocataire_fin = fields.Date("Au ",required=True)
    adresse_maroc_col = fields.Char("Adresse ")
    tel_col = fields.Char("Telephone")
    passeport_col = fields.Char("Numero de Passeport ")
    passeport_col_debut = fields.Date("Du")
    passeport_col_fin = fields.Date("Au")
    permis_colocataire = fields.Char("Numero de Permis ",required=True)
    date_debut_permis_colocataire = fields.Date("Du",required=True)
    date_expiration_permis_colocataire = fields.Date("Au",required=True)
    #=========================
    #=======Accessoire voiture======
    lavage = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Lavage')
    carte_grise = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Carte grise')
    assurance = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Assurance')
    decision = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Décision')
    vignette = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Vignette')
    visite_tech = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Visite Tech')
    gonfleur = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Gonfleur')
    triangle = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Triangle')
    gilet = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Gilet')
    
    enjoliseur = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Enjoliseur')
    radio = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Radio')
    jeux_tapis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Jeux Tapis ')
    cendrier = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Cendrier ')
    antenne = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Antenne Radio ')
    roue_secours = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Roue secours')
    cric = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Cric/Manivelle ')
    antivol = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Antivol ')
    extincteur = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Extincteur')
    #====================
    #=======prolongation et modalite de paiment ======
    duree_prol = fields.Integer("Duree ")
    date_debut_prol = fields.Date("Du ")
    date_fin_prol = fields.Date("Prolongation au ")
    nbr_jours_prol = fields.Integer(compute='_compute_nbr_jours_prol', string='Nombre de jours total après prolongation')
    prix_par_jours = fields.Float("Prix par jour")
    avance = fields.Float("Avance ")
    reste_a_payer = fields.Float(compute='_compute_reste_a_payer', string='Reste a payer')
    total_ttc = fields.Float(compute='_compute_prix_total', string='Prix total')
    #==============
    state_cont = fields.Selection([
        ('futur', 'Incoming'),
        ('open', 'In Progress'),
        ('expired', 'Expired'),
        ('closed', 'Closed')
        ], 'Status', default='open', readonly=True,
        help='Choose whether the contract is still valid or not',
        tracking=True,
        copy=False)
    
    
    # def _compute_nbr_jours(self):
        # for record in self:
            # if record.date_depart > record.date_retour:
                # raise ValidationError('Start date should not greater than end date.')
            # else:
                # record.nbr_jours = (record.date_retour - record.date_depart).days + 1
    
    @api.depends('date_depart','date_retour')
    def _compute_nbr_jours(self):
        for rec in self:
            if rec.date_depart:
                delta = rec.date_retour - rec.date_depart
                rec.nbr_jours = delta.days
            else:
                rec.nbr_jours = 0
    
    # def _compute_nbr_jours_prol(self):
        # for record in self:
                # record.nbr_jours_prol = (record.date_fin_prol - record.date_retour).days
    @api.depends('date_fin_prol','date_retour')
    def _compute_nbr_jours_prol(self):
        for rec in self:
            if rec.date_retour:
                delta = rec.date_fin_prol - rec.date_retour
                rec.nbr_jours_prol = delta.days + rec.nbr_jours
            else:
                rec.nbr_jours_prol = 0
        
    def _compute_prix_total(self):
        """prix total
        """
        for record in self:
                record.total_ttc = (record.prix_par_jours * record.nbr_jours) + (record.prix_par_jours * record.nbr_jours_prol)
    
    def _compute_reste_a_payer(self):
        """Calcul du teste a payer
        """
        for record in self:
                record.reste_a_payer = (record.total_ttc - record.avance)
                