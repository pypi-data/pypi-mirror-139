class Strain:
    def __init__(self, score, name, slug, review_avg, review_count, strain_type,
                consumption_time, thc_min, thc_max, cbd_min, cbd_max, uses, effects,
                logo_url, strain_id):

        self.score = score
        self.name = name
        self.slug = slug
        self.review_avg = review_avg
        self.review_count = review_count
        self.strain_type = strain_type
        self.consumption_time = consumption_time
        self.thc_min = thc_min
        self.thc_max = thc_max
        self.cbd_min = cbd_min
        self.cbd_max = cbd_max
        self.uses = uses
        self.effects = effects
        self.logo_url = logo_url
        self.strain_id = strain_id