from jsonmodels import models, fields

__author__ = "ckopanos"


class GnomADCoverage(models.Base):
    version = fields.StringField(help_text="Version")
    coverage_mean = fields.ListField(help_text="Mean coverage",
                                     items_types=(float, type(None)), required=False, nullable=True)
    coverage_median = fields.ListField(help_text="Median coverage",
                                       items_types=(float, type(None)), required=False, nullable=True)
    coverage_20_frequency = fields.ListField(help_text="Proportion of samples with over 20x",
                                             items_types=(float, type(None)),
                                             required=False, nullable=True)


class GnomAD(models.Base):
    version = fields.StringField(help_text="Version")
    ac = fields.IntField(help_text="Allele Count", required=False, nullable=True)
    an = fields.IntField(help_text="Allele Number", required=False, nullable=True)
    ac_adj = fields.FloatField(help_text="Allele Count", required=False, nullable=True)
    an_adj = fields.FloatField(help_text="Allele Number", required=False, nullable=True)
    af = fields.FloatField(help_text="Allele Frequency", required=False, nullable=True)
    ac_afr = fields.IntField(help_text="Allele Count African", required=False, nullable=True)
    ac_amr = fields.IntField(help_text="Allele Count American", required=False, nullable=True)
    ac_asj = fields.IntField(help_text="Allele Count Ashkenazi Jewish", required=False, nullable=True)
    ac_eas = fields.IntField(help_text="Allele Count East Asian", required=False, nullable=True)
    ac_fin = fields.IntField(help_text="Allele Count European (Finnish)", required=False, nullable=True)
    ac_nfe = fields.IntField(help_text="Allele Count European (Non-Finnish)", required=False, nullable=True)
    ac_oth = fields.IntField(help_text="Allele Count Other", required=False, nullable=True)
    ac_male = fields.IntField(help_text="Allele Count Male", required=False, nullable=True)
    ac_female = fields.IntField(help_text="Allele Count Female", required=False, nullable=True)
    hom = fields.IntField(help_text="Number of Homozygotes", required=False, nullable=True)
    hemi = fields.IntField(help_text="Number of Hemizygotes", required=False, nullable=True)
    ac_hom = fields.FloatField(help_text="Number of Homozygotes", required=False, nullable=True)
    ac_hemi = fields.FloatField(help_text="Number of Hemizygotes", required=False, nullable=True)
    an_afr = fields.IntField(help_text="Allele Number African", required=False, nullable=True)
    an_amr = fields.IntField(help_text="Allele Number American", required=False, nullable=True)
    an_asj = fields.IntField(help_text="Allele Number Ashkenazi Jewish", required=False, nullable=True)
    an_eas = fields.IntField(help_text="Allele Number East Asian", required=False, nullable=True)
    an_fin = fields.IntField(help_text="Allele Number European (Finnish)", required=False, nullable=True)
    an_nfe = fields.IntField(help_text="Allele Number European (Non-Finnish)", required=False, nullable=True)
    an_oth = fields.IntField(help_text="Allele Number Other", required=False, nullable=True)
    an_male = fields.IntField(help_text="Allele Number Male", required=False, nullable=True)
    an_female = fields.IntField(help_text="Allele Number Female", required=False, nullable=True)
    hom_afr = fields.IntField(help_text="Number of Homozygotes African", required=False, nullable=True)
    hom_amr = fields.IntField(help_text="Number of Homozygotes American", required=False, nullable=True)
    hom_asj = fields.IntField(help_text="Number of Homozygotes Ashkenazi Jewish", required=False, nullable=True)
    hom_eas = fields.IntField(help_text="Number of Homozygotes East Asian", required=False, nullable=True)
    hom_fin = fields.IntField(help_text="Number of Homozygotes European (Finnish)", required=False, nullable=True)
    hom_nfe = fields.IntField(help_text="Number of Homozygotes European (Non-Finnish)", required=False, nullable=True)
    hom_oth = fields.IntField(help_text="Number of Homozygotes Other", required=False, nullable=True)
    hom_male = fields.IntField(help_text="Number of Homozygotes Male", required=False, nullable=True)
    hom_female = fields.IntField(help_text="Number of Homozygotes Female", required=False, nullable=True)
    af_afr = fields.FloatField(help_text="Allele Frequency African", required=False, nullable=True)
    af_amr = fields.FloatField(help_text="Allele Frequency American", required=False, nullable=True)
    af_asj = fields.FloatField(help_text="Allele Frequency Ashkenazi Jewish", required=False, nullable=True)
    af_eas = fields.FloatField(help_text="Allele Frequency East Asian", required=False, nullable=True)
    af_fin = fields.FloatField(help_text="Allele Frequency European (Finnish)", required=False, nullable=True)
    af_nfe = fields.FloatField(help_text="Allele Frequency European (Non-Finnish)", required=False, nullable=True)
    af_oth = fields.FloatField(help_text="Allele Frequency Other", required=False, nullable=True)
    af_male = fields.FloatField(help_text="Allele Frequency Male", required=False, nullable=True)
    af_female = fields.FloatField(help_text="Allele Frequency Female", required=False, nullable=True)
    main_data = fields.StringField(help_text="Main data point", required=False, nullable=True)