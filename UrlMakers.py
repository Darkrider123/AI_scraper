class UrlMakerWeidmueller():
    def __init__(self):
        self.url = ""
    
    def make_url(self, id):
        self.url = "https://www.weidmueller.com/int/search.jsp?query=" + str(id) + "&tab=products"

class UrlMakerPhoenix():
    def __init__(self):
        self.url = ""
    
    def make_url(self, id):
        self.url = "https://www.phoenixcontact.com/online/portal/us?uri=pxc-oc-itemdetail:pid=" + str(id)  + "&library=usen&tab=1"